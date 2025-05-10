from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime
import pandas as pd
import numpy as np
from statsmodels.regression.linear_model import OLS
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_white
from statsmodels.stats.stattools import jarque_bera
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import linear_reset
import scipy.stats as stats
import logging
import traceback
import io

from routes.auth import get_current_user, User

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/empirical", tags=["实证分析"])

# 数据模型
class EmpiricalAnalysisRequest(BaseModel):
    data: List[Dict[str, Any]]
    dependentVar: str
    independentVars: List[str]
    controlVars: Optional[List[str]] = []
    groupVars: Optional[List[str]] = []

class EmpiricalAnalysisResult(BaseModel):
    regressionResults: List[Dict[str, Any]]
    heterogeneityResults: List[Dict[str, Any]]
    diagnosticTests: List[Dict[str, Any]]
    robustnessTests: List[Dict[str, Any]]
    selectedMethods: List[str]

# 模拟数据库
analysis_results_db = {}

def run_regression_diagnostics(model, X):
    """运行回归诊断检验"""
    try:
        # White异方差检验
        white_test = het_white(model.resid, X)
        
        # Jarque-Bera正态性检验
        jb_test = jarque_bera(model.resid)
        
        # VIF多重共线性检验
        vif_data = pd.DataFrame()
        vif_data["Variable"] = X.columns
        vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        
        # Ramsey RESET检验
        reset_test = linear_reset(model)
        
        diagnostics = [
            {
                'test': 'White异方差检验',
                'statistic': float(white_test[0]),
                'pValue': float(white_test[1]),
                'conclusion': '存在异方差性' if white_test[1] < 0.05 else '不存在异方差性'
            },
            {
                'test': 'Jarque-Bera正态性检验',
                'statistic': float(jb_test[0]),
                'pValue': float(jb_test[1]),
                'conclusion': '残差不服从正态分布' if jb_test[1] < 0.05 else '残差服从正态分布'
            },
            {
                'test': 'Ramsey RESET检验',
                'statistic': float(reset_test.statistic),
                'pValue': float(reset_test.pvalue),
                'conclusion': '模型设定存在问题' if reset_test.pvalue < 0.05 else '模型设定合理'
            }
        ]
        
        # 添加VIF检验结果
        for _, row in vif_data.iterrows():
            if row['Variable'] != 'const':  # 跳过常数项
                diagnostics.append({
                    'test': f'VIF检验 ({row["Variable"]})',
                    'statistic': float(row['VIF']),
                    'pValue': None,
                    'conclusion': '存在严重多重共线性' if row['VIF'] > 10 else '多重共线性在可接受范围'
                })
        
        return diagnostics
    except Exception as e:
        logger.error(f"运行诊断检验时发生错误: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        return [{
            'test': '诊断检验',
            'statistic': None,
            'pValue': None,
            'conclusion': f'运行诊断检验时发生错误: {str(e)}'
        }]

def get_regression_results(model, group_name="全样本"):
    """获取回归结果"""
    return {
        'group': group_name,
        'coefficients': [{
            'variable': var,
            'estimate': float(model.params[var]),
            'stdError': float(model.bse[var]),
            'tValue': float(model.tvalues[var]),
            'pValue': float(model.pvalues[var])
        } for var in model.model.exog_names],
        'modelStats': {
            'rSquared': float(model.rsquared),
            'adjRSquared': float(model.rsquared_adj),
            'fStatistic': float(model.fvalue),
            'fPvalue': float(model.f_pvalue),
            'observations': int(model.nobs)
        }
    }

@router.post("/analyze")
async def analyze_data(
    request: EmpiricalAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        logger.info(f"接收到实证分析请求: dependentVar={request.dependentVar}, "
                   f"independentVars={request.independentVars}, "
                   f"controlVars={request.controlVars}, "
                   f"groupVars={request.groupVars}")
        
        # 将数据转换为DataFrame
        df = pd.DataFrame(request.data)
        logger.info(f"数据形状: {df.shape}")
        
        # 数据验证
        if df.empty:
            raise ValueError("数据为空")
            
        # 检查变量是否存在于数据中
        missing_vars = []
        if request.dependentVar not in df.columns:
            missing_vars.append(request.dependentVar)
        for var in request.independentVars:
            if var not in df.columns:
                missing_vars.append(var)
        for var in request.controlVars:
            if var not in df.columns:
                missing_vars.append(var)
        for var in request.groupVars:
            if var not in df.columns:
                missing_vars.append(var)
                
        if missing_vars:
            raise ValueError(f"以下变量在数据中不存在: {', '.join(missing_vars)}")
        
        # 检查数据类型并尝试转换为数值
        numeric_vars = [request.dependentVar] + request.independentVars + request.controlVars
        for var in numeric_vars:
            try:
                df[var] = pd.to_numeric(df[var], errors='coerce')
                nan_count = df[var].isna().sum()
                if nan_count > 0:
                    logger.warning(f"变量 {var} 有 {nan_count} 个值无法转换为数值，这些值将被移除")
                    df = df.dropna(subset=[var])
                if df.empty:
                    raise ValueError(f"转换 {var} 为数值后没有剩余有效数据")
                logger.info(f"变量 {var} 的数值范围: 最小值={df[var].min()}, 最大值={df[var].max()}")
            except Exception as e:
                logger.error(f"转换变量 {var} 时发生错误: {str(e)}")
                raise ValueError(f"变量 {var} 无法转换为数值类型: {str(e)}")
        
        logger.info(f"数据清理后的形状: {df.shape}")
        
        # 准备变量
        y = df[request.dependentVar]
        X_vars = request.independentVars + request.controlVars
        X = df[X_vars]
        X = sm.add_constant(X)
        
        logger.info(f"因变量形状: {y.shape}")
        logger.info(f"自变量形状: {X.shape}")
        
        # 运行基准回归
        base_model = OLS(y, X).fit()
        base_results = get_regression_results(base_model)
        logger.info("基准回归完成")
        
        # 运行诊断检验
        diagnostics = run_regression_diagnostics(base_model, X)
        logger.info("诊断检验完成")
        
        # 进行分组回归（异质性分析）
        group_results = []
        if request.groupVars:
            for group_var in request.groupVars:
                unique_groups = df[group_var].unique()
                logger.info(f"分组变量 {group_var} 的唯一值: {unique_groups}")
                
                for group in unique_groups:
                    group_df = df[df[group_var] == group]
                    logger.info(f"组 {group} 的样本量: {len(group_df)}")
                    
                    if len(group_df) > len(X.columns):
                        group_y = group_df[request.dependentVar]
                        group_X = group_df[X_vars]
                        group_X = sm.add_constant(group_X)
                        
                        group_model = OLS(group_y, group_X).fit()
                        group_results.append(
                            get_regression_results(group_model, f'{group_var}={group}')
                        )
                        logger.info(f"组 {group} 的回归完成")
                    else:
                        logger.warning(f"组 {group} 的样本量不足，跳过回归")
        
        # 计算组间差异显著性
        group_differences = []
        if len(group_results) > 1:
            logger.info("开始计算组间差异")
            for i in range(len(group_results)):
                for j in range(i + 1, len(group_results)):
                    group1 = group_results[i]
                    group2 = group_results[j]
                    
                    for coef1 in group1['coefficients']:
                        coef2 = next(c for c in group2['coefficients'] if c['variable'] == coef1['variable'])
                        if coef1['variable'] != 'const':
                            diff = abs(coef1['estimate'] - coef2['estimate'])
                            pooled_se = np.sqrt(coef1['stdError']**2 + coef2['stdError']**2)
                            t_stat = diff / pooled_se if pooled_se != 0 else 0
                            p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=base_model.df_resid))
                            
                            group_differences.append({
                                'group1': group1['group'],
                                'group2': group2['group'],
                                'variable': coef1['variable'],
                                'difference': float(diff),
                                'tStatistic': float(t_stat),
                                'pValue': float(p_value),
                                'isSignificant': bool(p_value < 0.05)
                            })
            logger.info("组间差异计算完成")
        
        # 准备响应数据
        response_data = {
            'baseResults': base_results,
            'groupResults': group_results,
            'groupDifferences': group_differences,
            'diagnostics': diagnostics
        }
        
        logger.info("分析完成，返回结果")
        return {
            'success': True,
            'data': response_data,
            'message': '分析完成'
        }
        
    except Exception as e:
        logger.error(f"发生错误: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        return {
            'success': False,
            'data': None,
            'message': str(e)
        }

@router.post("/upload")
async def upload_data_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    try:
        logger.info(f"接收到文件上传请求: filename={file.filename}")
        
        # 读取文件内容
        contents = await file.read()
        
        # 根据文件类型处理数据
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="不支持的文件格式")
        
        # 生成数据预览
        preview = df.head().to_dict('records')
        
        # 准备变量信息
        variables = []
        for col in df.columns:
            var_info = {
                'name': col,
                'type': 'numeric' if pd.api.types.is_numeric_dtype(df[col]) else 'categorical',
                'stats': {}
            }
            
            if var_info['type'] == 'numeric':
                var_info['stats'] = {
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max())
                }
            else:
                value_counts = df[col].value_counts()
                var_info['stats'] = {
                    'categories': value_counts.index.tolist(),
                    'frequencies': value_counts.values.tolist()
                }
            
            variables.append(var_info)
        
        logger.info("文件处理完成")
        return {
            'success': True,
            'data': {
                'preview': preview,
                'variables': variables,
                'totalRows': len(df),
                'totalColumns': len(df.columns)
            }
        }
        
    except Exception as e:
        logger.error(f"处理文件上传时发生错误: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) 