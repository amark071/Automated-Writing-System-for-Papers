"""实证分析Agent，负责生成论文的实证分析部分。"""

import os
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from statsmodels.regression.linear_model import OLS
from statsmodels.regression.panel import PanelOLS
from statsmodels.tsa.api import VAR
from statsmodels.stats.diagnostic import het_white, acorr_ljungbox
from statsmodels.stats.stattools import jarque_bera
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import linear_reset
from statsmodels.tsa.stattools import adfuller, kpss
import statsmodels.api as sm
import json

from src.paper_automation.agent_system.paper_agent.base_agent import BaseAgent
from src.paper_automation.agent_system.paper_agent.style.style_rules import StyleRules


class EmpiricalAgent(BaseAgent):
    """实证分析Agent类，负责生成论文中的实证分析部分。
    
    实证分析部分包括：
    1. 数据收集与处理
    2. 变量定义与测量
    3. 描述性统计
    4. 实证结果分析
    5. 稳健性检验
    """
    
    def __init__(self, agent_config: Dict[str, Any], style_rules: Optional[StyleRules] = None):
        """初始化实证分析Agent。
        
        Args:
            agent_config: Agent配置信息
            style_rules: 文体规则对象
        """
        super().__init__(agent_config, style_rules)
        self.name = "实证分析Agent"
        self.data = None
        self.model = None
        self.results = None
        self.analysis_config = None
        
    def generate_data_collection(self, paper_info: Dict[str, Any]) -> str:
        """生成数据收集与处理部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            数据收集与处理部分内容
        """
        data_collection_prompt = self._create_prompt(
            task="生成数据收集与处理部分",
            paper_info=paper_info,
            requirements=[
                "详细说明数据来源",
                "描述数据的收集过程",
                "解释数据的筛选和清洗步骤",
                "说明样本选择标准",
                "提供最终样本的基本情况"
            ]
        )
        
        return self._call_llm(data_collection_prompt)
        
    def generate_variable_definition(self, paper_info: Dict[str, Any]) -> str:
        """生成变量定义与测量部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            变量定义与测量部分内容
        """
        variable_prompt = self._create_prompt(
            task="生成变量定义与测量部分",
            paper_info=paper_info,
            requirements=[
                "定义并解释因变量",
                "定义并解释自变量",
                "定义并解释控制变量",
                "详细说明各变量的测量方法",
                "解释变量选择的理论依据"
            ]
        )
        
        return self._call_llm(variable_prompt)
        
    def generate_descriptive_statistics(self, paper_info: Dict[str, Any]) -> str:
        """生成描述性统计部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            描述性统计部分内容
        """
        statistics_prompt = self._create_prompt(
            task="生成描述性统计部分",
            paper_info=paper_info,
            requirements=[
                "提供样本的基本统计数据",
                "分析变量的分布特征",
                "说明各变量间的相关性",
                "展示关键统计表格说明",
                "对异常值或特殊现象进行解释"
            ]
        )
        
        return self._call_llm(statistics_prompt)
        
    def generate_empirical_results(self, paper_info: Dict[str, Any]) -> str:
        """生成实证结果分析部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            实证结果分析部分内容
        """
        results_prompt = self._create_prompt(
            task="生成实证结果分析部分",
            paper_info=paper_info,
            requirements=[
                "详细呈现主要回归结果",
                "解释结果与理论假设的关系",
                "分析各变量的显著性及影响程度",
                "提供结果的经济学解释",
                "说明结果的理论和实践意义"
            ]
        )
        
        return self._call_llm(results_prompt)
        
    def generate_robustness_tests(self, paper_info: Dict[str, Any]) -> str:
        """生成稳健性检验部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            稳健性检验部分内容
        """
        robustness_prompt = self._create_prompt(
            task="生成稳健性检验部分",
            paper_info=paper_info,
            requirements=[
                "提供多种稳健性检验方法",
                "使用替代变量进行检验",
                "解决潜在的内生性问题",
                "处理可能的样本选择偏差",
                "确认结果在不同条件下的一致性"
            ]
        )
        
        return self._call_llm(robustness_prompt)
        
    def generate_empirical_analysis(self, paper_info: Dict[str, Any]) -> str:
        """生成完整的实证分析部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            完整的实证分析部分内容
        """
        data_collection = self.generate_data_collection(paper_info)
        variable_definition = self.generate_variable_definition(paper_info)
        descriptive_statistics = self.generate_descriptive_statistics(paper_info)
        empirical_results = self.generate_empirical_results(paper_info)
        robustness_tests = self.generate_robustness_tests(paper_info)
        
        empirical_content = f"""
# 实证分析

## 数据收集与处理
{data_collection}

## 变量定义与测量
{variable_definition}

## 描述性统计
{descriptive_statistics}

## 实证结果分析
{empirical_results}

## 稳健性检验
{robustness_tests}
"""
        
        return empirical_content
        
    def load_data(self, data: pd.DataFrame) -> None:
        """加载数据"""
        self.data = data
        
    def configure_analysis(self, config: Dict) -> None:
        """配置分析参数
        
        Args:
            config: 包含以下键的字典：
                - data_type: 数据类型 ('cross_section'|'panel'|'time_series')
                - dependent_vars: 被解释变量列表
                - independent_vars: 解释变量列表
                - control_vars: 控制变量列表
                - method: 分析方法
        """
        self.analysis_config = config
        
    def preprocess_data(self) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """数据预处理"""
        if self.data is None or self.analysis_config is None:
            raise ValueError("请先加载数据并配置分析参数")
            
        # 获取所有变量
        all_vars = (self.analysis_config['dependent_vars'] + 
                   self.analysis_config['independent_vars'] + 
                   self.analysis_config.get('control_vars', []))
                   
        # 处理缺失值
        clean_data = self.data[all_vars].dropna()
        
        # 计算基本统计量
        stats = {
            'n_obs': len(clean_data),
            'missing_rate': (1 - len(clean_data)/len(self.data)) * 100,
            'descriptive_stats': clean_data.describe()
        }
        
        return clean_data, stats
        
    def run_analysis(self) -> Dict[str, Any]:
        """运行实证分析"""
        if self.analysis_config is None:
            raise ValueError("请先配置分析参数")
            
        clean_data, preprocessing_stats = self.preprocess_data()
        
        results = {
            'preprocessing': preprocessing_stats,
            'main_results': {},
            'diagnostic_tests': {},
            'robustness_checks': {},
            'text_summary': {}
        }
        
        # 根据数据类型选择分析方法
        if self.analysis_config['data_type'] == 'cross_section':
            results.update(self._run_cross_section_analysis(clean_data))
        elif self.analysis_config['data_type'] == 'panel':
            results.update(self._run_panel_analysis(clean_data))
        elif self.analysis_config['data_type'] == 'time_series':
            results.update(self._run_time_series_analysis(clean_data))
            
        # 生成结果描述
        results['text_summary'] = self._generate_results_description(results)
        
        return results
        
    def _run_cross_section_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """运行截面数据分析"""
        results = {}
        
        # 准备变量
        y = data[self.analysis_config['dependent_vars']]
        X = data[self.analysis_config['independent_vars'] + 
                 self.analysis_config.get('control_vars', [])]
        X = sm.add_constant(X)
        
        # 主回归
        model = OLS(y, X)
        results['main_results'] = model.fit()
        
        # 诊断性检验
        results['diagnostic_tests'] = {
            'white_test': het_white(results['main_results'].resid, X),
            'jb_test': jarque_bera(results['main_results'].resid),
            'vif': self._calculate_vif(X),
            'reset_test': linear_reset(results['main_results'])
        }
        
        return results
        
    def _run_panel_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """运行面板数据分析"""
        results = {}
        
        # TODO: 实现面板数据分析
        # 1. 构建面板数据结构
        # 2. 进行固定效应/随机效应检验
        # 3. 运行面板回归
        # 4. 进行相关诊断性检验
        
        return results
        
    def _run_time_series_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """运行时间序列分析"""
        results = {}
        
        # TODO: 实现时间序列分析
        # 1. 进行平稳性检验
        # 2. 进行协整检验
        # 3. 建立时间序列模型
        # 4. 进行诊断性检验
        
        return results
        
    def _calculate_vif(self, X: pd.DataFrame) -> Dict[str, float]:
        """计算方差膨胀因子"""
        vif_data = pd.DataFrame()
        vif_data["Variable"] = X.columns
        vif_data["VIF"] = [variance_inflation_factor(X.values, i)
                          for i in range(X.shape[1])]
        return vif_data.set_index('Variable')['VIF'].to_dict()
        
    def _generate_results_description(self, results: Dict[str, Any]) -> Dict[str, str]:
        """生成结果描述"""
        descriptions = {
            'preprocessing': self._describe_preprocessing(results['preprocessing']),
            'main_results': self._describe_main_results(results['main_results']),
            'diagnostic_tests': self._describe_diagnostic_tests(results['diagnostic_tests']),
            'robustness_checks': self._describe_robustness_checks(results.get('robustness_checks', {}))
        }
        return descriptions
        
    def _describe_preprocessing(self, stats: Dict) -> str:
        """生成数据预处理描述"""
        return f"""
        本研究使用的样本包含{stats['n_obs']}个观测值。
        在数据预处理过程中，对存在缺失值的观测进行了删除处理，
        缺失值处理比例为{stats['missing_rate']:.2f}%。
        """
        
    def _describe_main_results(self, results) -> str:
        """生成主要结果描述"""
        if results is None:
            return "未获得有效的回归结果。"
            
        description = "回归分析结果显示："
        
        # 添加R方和调整R方的描述
        description += f"""
        模型的R平方为{results.rsquared:.4f}，
        调整R平方为{results.rsquared_adj:.4f}，
        表明模型具有较好的解释力。
        """
        
        # 添加系数显著性的描述
        significant_vars = []
        for var, pval in results.pvalues.items():
            if var != 'const' and pval < 0.05:
                coef = results.params[var]
                significant_vars.append(
                    f"{var}({coef:+.4f}, p<{0.01 if pval<0.01 else 0.05})"
                )
        
        if significant_vars:
            description += f"""
            研究发现以下变量对因变量有显著影响：
            {', '.join(significant_vars)}。
            """
            
        return description
        
    def _describe_diagnostic_tests(self, tests: Dict) -> str:
        """生成诊断性检验描述"""
        if not tests:
            return "未进行诊断性检验。"
            
        description = "模型诊断结果显示："
        
        # White异方差检验
        if 'white_test' in tests:
            white_stat, white_p = tests['white_test']
            description += f"""
            White异方差检验的p值为{white_p:.4f}，
            {
                '表明存在异方差性问题' if white_p < 0.05
                else '未发现显著的异方差性问题'
            }。
            """
            
        # JB正态性检验
        if 'jb_test' in tests:
            jb_stat, jb_p = tests['jb_test']
            description += f"""
            Jarque-Bera检验的p值为{jb_p:.4f}，
            {
                '表明残差项不服从正态分布' if jb_p < 0.05
                else '未拒绝残差项服从正态分布的原假设'
            }。
            """
            
        # VIF多重共线性检验
        if 'vif' in tests:
            max_vif = max(tests['vif'].values())
            description += f"""
            最大方差膨胀因子(VIF)为{max_vif:.2f}，
            {
                '表明存在较严重的多重共线性问题' if max_vif > 10
                else '未发现严重的多重共线性问题'
            }。
            """
            
        return description
        
    def _describe_robustness_checks(self, checks: Dict) -> str:
        """生成稳健性检验描述"""
        if not checks:
            return "未进行稳健性检验。"
            
        # TODO: 实现稳健性检验描述的生成
        return "稳健性检验结果将在后续补充。" 