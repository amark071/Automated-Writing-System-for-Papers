"""
数据分析模块，提供数据结构识别、变量分析和实证策略生成功能
"""

from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import numpy as np
from scipy import stats
import logging
import os

class DataAnalyzer:
    """数据分析器，负责数据结构识别、变量分析和实证策略生成"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data = None
        self.data_structure = None
        self.variables = None
        self.hypotheses = []
        self.file_info = {}
        
    def load_data(self, file_path: str) -> bool:
        """加载数据文件，支持多种格式
        
        Args:
            file_path: 数据文件路径
            
        Returns:
            bool: 是否成功加载数据
        """
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.csv':
                self.data = pd.read_csv(file_path)
            elif file_ext in ['.xls', '.xlsx']:
                self.data = pd.read_excel(file_path)
            elif file_ext == '.dta':  # Stata文件
                self.data = pd.read_stata(file_path)
            elif file_ext == '.sas7bdat':  # SAS文件
                self.data = pd.read_sas(file_path)
            else:
                raise ValueError(f"不支持的文件格式: {file_ext}")
            
            # 记录文件信息
            self.file_info = {
                "format": file_ext,
                "rows": len(self.data),
                "columns": len(self.data.columns),
                "size": os.path.getsize(file_path)
            }
            
            return True
        except Exception as e:
            self.logger.error(f"加载数据失败: {str(e)}")
            return False
    
    def get_data_preview(self, rows: int = 5) -> Dict[str, Any]:
        """获取数据预览
        
        Args:
            rows: 预览行数
            
        Returns:
            Dict: 包含数据预览信息的字典
        """
        if self.data is None:
            return {}
            
        return {
            "head": self.data.head(rows).to_dict(),
            "dtypes": self.data.dtypes.to_dict(),
            "file_info": self.file_info
        }
    
    def get_variable_options(self) -> Dict[str, List[str]]:
        """获取变量选项
        
        Returns:
            Dict: 按类型分类的变量列表
        """
        if self.data is None:
            return {}
            
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns.tolist()
        date_cols = [col for col in self.data.columns 
                    if pd.api.types.is_datetime64_any_dtype(self.data[col])]
        
        return {
            "numeric": numeric_cols,
            "categorical": categorical_cols,
            "date": date_cols,
            "all": self.data.columns.tolist()
        }
            
    def identify_data_structure(self) -> Dict[str, Any]:
        """识别数据结构类型
        
        Returns:
            Dict: 包含数据结构信息的字典
        """
        try:
            if self.data is None:
                raise ValueError("未加载数据")
                
            # 检查是否有时间列
            time_cols = [col for col in self.data.columns 
                        if pd.api.types.is_datetime64_any_dtype(self.data[col]) or 
                        'year' in col.lower() or 
                        'date' in col.lower()]
            
            # 检查是否有ID列
            id_cols = [col for col in self.data.columns 
                      if 'id' in col.lower() or 
                      'code' in col.lower() or 
                      'symbol' in col.lower()]
            
            if time_cols and id_cols:
                structure = "面板数据"
                details = {
                    "time_cols": time_cols,
                    "id_cols": id_cols,
                    "time_periods": len(self.data[time_cols[0]].unique()),
                    "entities": len(self.data[id_cols[0]].unique())
                }
            elif time_cols:
                structure = "时间序列数据"
                details = {
                    "time_cols": time_cols,
                    "periods": len(self.data[time_cols[0]].unique()),
                    "frequency": self._identify_time_frequency(time_cols[0])
                }
            else:
                structure = "截面数据"
                details = {
                    "observations": len(self.data)
                }
            
            self.data_structure = {
                "type": structure,
                "details": details
            }
            
            return self.data_structure
            
        except Exception as e:
            self.logger.error(f"识别数据结构失败: {str(e)}")
            return {}
            
    def analyze_variables(self) -> Dict[str, Any]:
        """分析变量特征
        
        Returns:
            Dict: 包含变量分析结果的字典
        """
        try:
            if self.data is None:
                raise ValueError("未加载数据")
                
            analysis = {}
            
            # 基础统计描述
            analysis["descriptive"] = self.data.describe()
            
            # 变量类型识别
            analysis["types"] = self.data.dtypes.to_dict()
            
            # 缺失值分析
            missing = self.data.isnull().sum()
            analysis["missing"] = {
                "counts": missing.to_dict(),
                "percentages": (missing / len(self.data) * 100).to_dict()
            }
            
            # 相关性分析
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                analysis["correlations"] = {
                    "pearson": self.data[numeric_cols].corr(method='pearson').to_dict(),
                    "spearman": self.data[numeric_cols].corr(method='spearman').to_dict()
                }
            
            # 变量分布特征
            analysis["distribution"] = {}
            for col in numeric_cols:
                data = self.data[col].dropna()
                if len(data) > 0:
                    analysis["distribution"][col] = {
                        "skewness": stats.skew(data),
                        "kurtosis": stats.kurtosis(data),
                        "normality": stats.normaltest(data)[1] if len(data) >= 8 else None,
                        "quartiles": data.quantile([0.25, 0.5, 0.75]).to_dict(),
                        "outliers": self._detect_outliers(data)
                    }
            
            # 分类变量分析
            categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns
            analysis["categorical"] = {}
            for col in categorical_cols:
                value_counts = self.data[col].value_counts()
                analysis["categorical"][col] = {
                    "unique_values": len(value_counts),
                    "top_categories": value_counts.head().to_dict(),
                    "category_percentages": (value_counts / len(self.data) * 100).head().to_dict()
                }
            
            self.variables = analysis
            return analysis
            
        except Exception as e:
            self.logger.error(f"分析变量特征失败: {str(e)}")
            return {}
            
    def generate_empirical_strategy(self, hypotheses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成实证策略
        
        Args:
            hypotheses: 研究假设列表
            
        Returns:
            Dict: 包含实证策略的字典
        """
        try:
            if self.data_structure is None:
                self.identify_data_structure()
                
            if self.variables is None:
                self.analyze_variables()
                
            strategy = {
                "main_methods": self._get_main_methods(),
                "robustness": self._get_robustness_methods(),
                "additional": self._get_additional_methods(hypotheses)
            }
            
            return strategy
            
        except Exception as e:
            self.logger.error(f"生成实证策略失败: {str(e)}")
            return {}
    
    def _identify_time_frequency(self, time_col: str) -> str:
        """识别时间序列频率"""
        try:
            dates = pd.to_datetime(self.data[time_col])
            diff = dates.diff().dropna().mode()[0]
            
            if diff.days == 1:
                return "日度"
            elif 7 <= diff.days <= 7:
                return "周度"
            elif 28 <= diff.days <= 31:
                return "月度"
            elif 88 <= diff.days <= 92:
                return "季度"
            elif 180 <= diff.days <= 186:
                return "半年度"
            else:
                return "年度"
        except:
            return "未知"
    
    def _get_main_methods(self) -> List[Dict[str, Any]]:
        """获取主要分析方法"""
        if self.data_structure["type"] == "面板数据":
            return [
                {
                    "name": "固定效应模型",
                    "package": "statsmodels.regression.linear_model",
                    "function": "PanelOLS",
                    "params": {
                        "entity_effects": True,
                        "time_effects": True
                    }
                },
                {
                    "name": "随机效应模型",
                    "package": "statsmodels.regression.linear_model",
                    "function": "RandomEffects",
                    "params": {}
                }
            ]
        elif self.data_structure["type"] == "时间序列数据":
            return [
                {
                    "name": "ARIMA模型",
                    "package": "statsmodels.tsa.arima.model",
                    "function": "ARIMA",
                    "params": {}
                },
                {
                    "name": "VAR模型",
                    "package": "statsmodels.tsa.vector_ar.var_model",
                    "function": "VAR",
                    "params": {}
                }
            ]
        else:  # 截面数据
            return [
                {
                    "name": "OLS回归",
                    "package": "statsmodels.regression.linear_model",
                    "function": "OLS",
                    "params": {}
                },
                {
                    "name": "2SLS回归",
                    "package": "statsmodels.regression.linear_model",
                    "function": "IV2SLS",
                    "params": {}
                }
            ]
    
    def _get_robustness_methods(self) -> List[Dict[str, Any]]:
        """获取稳健性检验方法"""
        return [
            {
                "name": "Winsorize处理",
                "package": "scipy.stats",
                "function": "mstats.winsorize",
                "params": {
                    "limits": [0.01, 0.01]
                }
            },
            {
                "name": "异常值处理",
                "package": "scipy.stats",
                "function": "zscore",
                "params": {}
            },
            {
                "name": "Bootstrap",
                "package": "sklearn.utils",
                "function": "resample",
                "params": {
                    "n_samples": 1000
                }
            }
        ]
    
    def _get_additional_methods(self, hypotheses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """根据研究假设获取额外分析方法"""
        methods = []
        
        # 检查是否需要中介效应分析
        if any("中介" in h.get("type", "") for h in hypotheses):
            methods.append({
                "name": "中介效应分析",
                "package": "statsmodels.stats.mediation",
                "function": "Mediation",
                "params": {}
            })
        
        # 检查是否需要调节效应分析
        if any("调节" in h.get("type", "") for h in hypotheses):
            methods.append({
                "name": "调节效应分析",
                "package": "statsmodels.stats.contingency",
                "function": "interaction_plot",
                "params": {}
            })
        
        return methods 
    
    def _detect_outliers(self, data: pd.Series) -> Dict[str, Any]:
        """检测异常值
        
        Args:
            data: 数据序列
            
        Returns:
            Dict: 异常值信息
        """
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = data[(data < lower_bound) | (data > upper_bound)]
        
        return {
            "count": len(outliers),
            "percentage": len(outliers) / len(data) * 100,
            "bounds": {
                "lower": lower_bound,
                "upper": upper_bound
            }
        } 