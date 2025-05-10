"""
论文写作系统后端API
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
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
import os
import json
from pathlib import Path
import io

from routes import auth, writing, agent, empirical

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="论文写作系统",
    description="提供论文写作的API接口",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# 包含路由
app.include_router(auth.router)
app.include_router(writing.router)
app.include_router(agent.router)
app.include_router(empirical.router)

class EmpiricalAnalysisRequest(BaseModel):
    data: List[Dict[str, Any]]
    dependentVar: str
    independentVars: List[str]
    controlVars: Optional[List[str]] = []
    groupVars: Optional[List[str]] = []

class LiteratureRequest(BaseModel):
    mainTitle: str
    subTitle: Optional[str] = None
    reviewMethod: Optional[str] = None
    researchGap: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "论文写作系统API服务正在运行"}

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
        # 返回一个基本的诊断结果
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

@app.post("/api/empirical-analysis")
async def empirical_analysis(request: EmpiricalAnalysisRequest):
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
                # 直接使用 pd.to_numeric，不进行字符串处理
                df[var] = pd.to_numeric(df[var], errors='coerce')
                # 检查是否有任何 NaN 值
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
                    # 获取分组数据
                    group_df = df[df[group_var] == group]
                    logger.info(f"组 {group} 的样本量: {len(group_df)}")
                    
                    if len(group_df) > len(X.columns):  # 确保样本量足够
                        group_y = group_df[request.dependentVar]
                        group_X = group_df[X_vars]
                        group_X = sm.add_constant(group_X)
                        
                        # 运行分组回归
                        group_model = OLS(group_y, group_X).fit()
                        group_results.append(
                            get_regression_results(group_model, f'{group_var}={group}')
                        )
                        logger.info(f"组 {group} 的回归完成")
                    else:
                        logger.warning(f"组 {group} 的样本量不足，跳过回归")
        
        # 计算组间差异显著性（如果有分组结果）
        group_differences = []
        if len(group_results) > 1:
            logger.info("开始计算组间差异")
            for i in range(len(group_results)):
                for j in range(i + 1, len(group_results)):
                    group1 = group_results[i]
                    group2 = group_results[j]
                    
                    # 计算系数差异的t统计量和p值
                    for coef1 in group1['coefficients']:
                        coef2 = next(c for c in group2['coefficients'] if c['variable'] == coef1['variable'])
                        if coef1['variable'] != 'const':  # 跳过常数项
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

def load_cnki_papers(directory: str) -> List[Dict[str, str]]:
    """加载CNKI文献数据"""
    papers = []
    try:
        # 确保目录存在
        if not os.path.exists(directory):
            logger.error(f"目录不存在: {directory}")
            return papers

        # 遍历目录中的所有文件
        for file_name in os.listdir(directory):
            if not file_name.endswith('.txt'):
                continue

            file_path = os.path.join(directory, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    papers.append({
                        'title': content.split('标题：')[1].split('\n')[0] if '标题：' in content else '',
                        'authors': content.split('作者：')[1].split('\n')[0] if '作者：' in content else '',
                        'abstract': content.split('摘要：')[1].split('\n')[0] if '摘要：' in content else '',
                        'keywords': content.split('关键词：')[1].split('\n')[0] if '关键词：' in content else '',
                        'year': content.split('年份：')[1].split('\n')[0] if '年份：' in content else ''
                    })
            except Exception as e:
                logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
                continue

        return papers
    except Exception as e:
        logger.error(f"加载CNKI文献数据时出错: {str(e)}")
        return papers

@app.post("/api/generate/literature")
async def generate_literature(request: LiteratureRequest):
    try:
        logger.info(f"接收到文献综述生成请求: mainTitle={request.mainTitle}, "
                   f"subTitle={request.subTitle}, "
                   f"reviewMethod={request.reviewMethod}")
        
        # 加载CNKI文献数据
        papers = load_cnki_papers("data/raw/cnki")
        
        # 调用LiteratureReviewAgent生成文献综述
        from paper_automation.agent_system.paper_agent.content.literature.literature_review_agent import LiteratureReviewAgent
        agent = LiteratureReviewAgent()
        review = agent.generate_literature_review(
            papers=papers,
            main_title=request.mainTitle,
            sub_title=request.subTitle,
            review_method=request.reviewMethod
        )
        
        return review
        
    except Exception as e:
        logger.error(f"生成文献综述时发生错误: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

def detect_data_type(df):
    """检测数据类型（截面数据、面板数据或时间序列数据）"""
    try:
        # 检查是否有时间相关的列
        time_columns = df.select_dtypes(include=['datetime64']).columns
        date_like_columns = [col for col in df.columns if any(x in col.lower() for x in ['year', 'month', 'date', 'time', 'period'])]
        
        # 检查是否有ID相关的列
        id_like_columns = [col for col in df.columns if any(x in col.lower() for x in ['id', 'code', 'number', 'no'])]
        
        # 如果有时间列和ID列，可能是面板数据
        if (len(time_columns) > 0 or len(date_like_columns) > 0) and len(id_like_columns) > 0:
            return {
                'type': 'panel',
                'confidence': 0.9
            }
        # 如果只有时间列，可能是时间序列数据
        elif len(time_columns) > 0 or len(date_like_columns) > 0:
            return {
                'type': 'time',
                'confidence': 0.8
            }
        # 如果只有ID列或者都没有，可能是截面数据
        else:
            return {
                'type': 'cross',
                'confidence': 0.7
            }
    except Exception as e:
        logger.error(f"检测数据类型时发生错误: {str(e)}")
        return {
            'type': 'cross',
            'confidence': 0.5
        }

@app.options("/api/writing/{writing_id}/sections/{section_id}/data-analysis/upload")
async def upload_data_file_options():
    return {}

@app.post("/api/writing/{writing_id}/sections/{section_id}/data-analysis/upload")
async def upload_data_file(
    writing_id: str,
    section_id: str,
    file: UploadFile = File(...)
):
    try:
        logger.info(f"接收到文件上传请求: writing_id={writing_id}, section_id={section_id}, filename={file.filename}")
        
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
        preview = df.to_string()
        
        # 检测数据类型
        detected_data_type = detect_data_type(df)
        
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
        
        # 准备响应数据
        response_data = {
            'processedData': {
                'variables': variables,
                'rawData': df.values.tolist()
            },
            'preview': preview,
            'detectedDataType': detected_data_type
        }
        
        logger.info("文件处理完成")
        return response_data
        
    except Exception as e:
        logger.error(f"处理文件上传时发生错误: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/writing/{writing_id}/sections/{section_id}/empirical-analysis/start")
async def start_empirical_analysis(
    writing_id: str,
    section_id: str,
    request: dict
):
    try:
        logger.info(f"开始实证分析: writing_id={writing_id}, section_id={section_id}")
        logger.info(f"分析配置: {request}")
        
        # 这里应该实现实证分析的逻辑
        # 暂时返回成功响应
        return {
            "success": True,
            "message": "实证分析已启动",
            "data": {
                "writingId": writing_id,
                "sectionId": section_id,
                "status": "processing"
            }
        }
    except Exception as e:
        logger.error(f"启动实证分析时发生错误: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"启动实证分析失败: {str(e)}"
        )

@app.get("/api/writing/{writing_id}/sections/{section_id}/empirical-analysis/results")
async def get_empirical_analysis_results(
    writing_id: str,
    section_id: str
):
    try:
        logger.info(f"获取实证分析结果: writing_id={writing_id}, section_id={section_id}")
        
        # 返回示例数据
        return {
            "success": True,
            "data": {
                "regressionResults": [
                    {
                        "variable": "EC",
                        "coefficient": 0.3245,
                        "standardError": 0.0856,
                        "tStat": 3.7910,
                        "pValue": 0.0002,
                        "significance": "***"
                    },
                    {
                        "variable": "TC",
                        "coefficient": 0.1523,
                        "standardError": 0.0654,
                        "tStat": 2.3287,
                        "pValue": 0.0214,
                        "significance": "**"
                    }
                ],
                "heterogeneityResults": [
                    {
                        "variable": "EC_东部",
                        "coefficient": 0.4123,
                        "standardError": 0.0923,
                        "tStat": 4.4669,
                        "pValue": 0.0000,
                        "significance": "***"
                    },
                    {
                        "variable": "EC_中部",
                        "coefficient": 0.2876,
                        "standardError": 0.0845,
                        "tStat": 3.4036,
                        "pValue": 0.0008,
                        "significance": "***"
                    },
                    {
                        "variable": "EC_西部",
                        "coefficient": 0.1987,
                        "standardError": 0.0912,
                        "tStat": 2.1789,
                        "pValue": 0.0312,
                        "significance": "**"
                    }
                ],
                "diagnosticTests": [
                    {
                        "testName": "Hausman检验",
                        "result": "Chi2(2) = 15.23, p值 = 0.0005",
                        "suggestion": "建议使用固定效应模型",
                        "status": "success"
                    },
                    {
                        "testName": "异方差检验",
                        "result": "Chi2(1) = 8.45, p值 = 0.0037",
                        "suggestion": "存在异方差问题，建议使用稳健标准误",
                        "status": "warning"
                    },
                    {
                        "testName": "序列相关检验",
                        "result": "F(1, 299) = 1.23, p值 = 0.2678",
                        "suggestion": "不存在序列相关问题",
                        "status": "success"
                    }
                ],
                "robustnessTests": [
                    {
                        "testName": "替换核心解释变量",
                        "description": "使用替代指标进行回归",
                        "result": "系数符号和显著性保持一致",
                        "conclusion": "结果具有稳健性"
                    },
                    {
                        "testName": "剔除异常值",
                        "description": "剔除首尾1%的极端值",
                        "result": "主要结论保持不变",
                        "conclusion": "结果不受异常值影响"
                    }
                ],
                "selectedMethods": ["固定效应模型", "异质性分析", "稳健性检验"]
            }
        }
    except Exception as e:
        logger.error(f"获取实证分析结果时发生错误: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"获取实证分析结果失败: {str(e)}"
        )

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"全局异常: {str(exc)}")
    logger.error(f"错误堆栈: {traceback.format_exc()}")
    return {
        "success": False,
        "message": "服务器内部错误",
        "detail": str(exc)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)