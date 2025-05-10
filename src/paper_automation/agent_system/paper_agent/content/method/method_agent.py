from typing import Dict, List, Any, Optional
import logging
import numpy as np
from ...knowledge_management.knowledge_graph.base.knowledge_graph_analyzer import KnowledgeGraphAnalyzer
from .data_analysis import DataAnalyzer

class MethodAgent:
    """负责生成论文研究方法部分的专门代理"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.status = "initialized"
        self.knowledge_graph = None
        self.style_rules = {}
        self.topic = ""
        self.discipline = "economics"  # 默认为经济学
        self.analyzer = KnowledgeGraphAnalyzer()
        self.hypotheses = []
        self.data_analyzer = DataAnalyzer()  # 添加数据分析器
        
    def initialize(self, topic: str, discipline: str = "economics", 
                   knowledge_graph: Optional[Dict[str, Any]] = None,
                   style_rules: Optional[Dict[str, Any]] = None,
                   hypotheses: Optional[List[Dict[str, Any]]] = None,
                   data_path: Optional[str] = None) -> bool:  # 添加data_path参数
        """初始化研究方法代理
        
        Args:
            topic: 研究主题
            discipline: 学科领域，默认为经济学
            knowledge_graph: 知识图谱
            style_rules: 风格规则
            hypotheses: 研究假设
            data_path: 数据文件路径
        
        Returns:
            初始化是否成功
        """
        try:
            self.topic = topic
            self.discipline = discipline
            
            # 设置知识图谱
            self.knowledge_graph = knowledge_graph
            if not self.knowledge_graph:
                self.logger.warning("未提供知识图谱，研究方法生成可能受限")
            
            # 加载风格规则
            self.style_rules = style_rules or self._get_default_style_rules()
            
            # 设置研究假设
            self.hypotheses = hypotheses or []
            
            # 加载数据（如果提供了数据路径）
            if data_path:
                if not self.data_analyzer.load_data(data_path):
                    self.logger.warning("加载数据失败，部分功能可能受限")
                    return False
            
            self.status = "ready"
            return True
        except Exception as e:
            self.logger.error(f"初始化研究方法代理失败: {str(e)}")
            return False
    
    def _get_default_style_rules(self) -> Dict[str, Any]:
        """获取默认的风格规则"""
        if self.discipline == "economics":
            return {
                "formality": "high",
                "precision": "high",
                "detail_level": "high",
                "table_usage": "high",
                "statistical_rigor": "high",
                "replicability_focus": "high"
            }
        else:
            # 其他学科的默认规则
            return {
                "formality": "medium",
                "precision": "medium",
                "detail_level": "medium",
                "table_usage": "medium",
                "statistical_rigor": "medium",
                "replicability_focus": "medium"
            }
    
    def generate_research_design(self) -> str:
        """生成研究设计部分
        
        Returns:
            生成的研究设计文本
        """
        try:
            # 1. 确定研究设计
            design = self._determine_research_design()
            
            # 2. 组织研究设计内容
            design_content = self._compose_design_content(design)
            
            # 3. 应用学科风格
            design_content = self._apply_style(design_content)
            
            return design_content
        except Exception as e:
            self.logger.error(f"生成研究设计失败: {str(e)}")
            return ""
    
    def generate_data_sources(self) -> str:
        """生成数据来源部分
        
        Returns:
            生成的数据来源文本
        """
        try:
            # 1. 确定数据来源
            data_sources = self._determine_data_sources()
            
            # 2. 组织数据来源内容
            data_content = self._compose_data_content(data_sources)
            
            # 3. 应用学科风格
            data_content = self._apply_style(data_content)
            
            return data_content
        except Exception as e:
            self.logger.error(f"生成数据来源失败: {str(e)}")
            return ""
    
    def generate_variable_definitions(self) -> str:
        """生成变量定义部分
        
        Returns:
            生成的变量定义文本
        """
        try:
            # 1. 确定变量定义
            variables = self._define_variables()
            
            # 2. 组织变量定义内容
            variable_content = self._compose_variable_content(variables)
            
            # 3. 应用学科风格
            variable_content = self._apply_style(variable_content)
            
            return variable_content
        except Exception as e:
            self.logger.error(f"生成变量定义失败: {str(e)}")
            return ""
    
    def generate_analytical_methods(self) -> str:
        """生成分析方法部分
        
        Returns:
            生成的分析方法文本
        """
        try:
            # 1. 确定分析方法
            methods = self._determine_analytical_methods()
            
            # 2. 组织分析方法内容
            method_content = self._compose_method_content(methods)
            
            # 3. 应用学科风格
            method_content = self._apply_style(method_content)
            
            return method_content
        except Exception as e:
            self.logger.error(f"生成分析方法失败: {str(e)}")
            return ""
    
    def generate_full_method_section(self) -> str:
        """生成完整的研究方法部分
        
        Returns:
            完整的研究方法文本
        """
        try:
            # 1. 生成研究设计
            design = self.generate_research_design()
            
            # 2. 生成数据来源
            data = self.generate_data_sources()
            
            # 3. 生成变量定义
            variables = self.generate_variable_definitions()
            
            # 4. 生成分析方法
            methods = self.generate_analytical_methods()
            
            # 5. 组合所有部分
            method_section = f"{design}\n\n{data}\n\n{variables}\n\n{methods}"
            
            # 6. 最终调整和润色
            method_section = self._polish_text(method_section)
            
            return method_section
        except Exception as e:
            self.logger.error(f"生成完整研究方法失败: {str(e)}")
            return ""
    
    def _determine_research_design(self) -> Dict[str, Any]:
        """确定研究设计"""
        # 实际实现中，应基于研究主题和假设确定合适的设计
        # 这里用占位符实现
        return {
            "type": "实证研究",
            "approach": "量化研究",
            "design": "面板数据分析",
            "time_period": "2010-2020年",
            "unit_of_analysis": "上市公司",
            "sample_scope": "沪深A股上市公司",
            "selection_criteria": [
                "剔除金融保险行业样本",
                "剔除ST、*ST公司",
                "剔除数据缺失样本",
                "剔除极端值样本"
            ],
            "rationale": f"面板数据分析有助于考察{self.topic}随时间变化的效应，控制个体固定效应"
        }
    
    def _determine_data_sources(self) -> Dict[str, Any]:
        """确定数据来源"""
        # 实际实现中，应基于研究设计确定合适的数据来源
        # 这里用占位符实现
        return {
            "primary_sources": [
                {"name": "CSMAR数据库", "content": "财务数据、公司治理数据", "time_period": "2010-2020年"},
                {"name": "WIND数据库", "content": "宏观经济数据、行业数据", "time_period": "2010-2020年"}
            ],
            "secondary_sources": [
                {"name": "国家统计局", "content": "地区经济发展数据", "time_period": "2010-2020年"},
                {"name": "中国工商银行经济研究所", "content": f"{self.topic}相关指标", "time_period": "2010-2020年"}
            ],
            "data_processing": [
                "使用Stata 16.0进行数据清洗",
                "使用R 4.1.0进行统计分析",
                "使用Python 3.8进行数据可视化"
            ],
            "sample_size": {
                "initial": "3,216家",
                "final": "2,845家",
                "firm_year": "28,450个"
            }
        }
    
    def _define_variables(self) -> Dict[str, List[Dict[str, Any]]]:
        """定义变量"""
        # 实际实现中，应基于假设和研究设计定义变量
        # 这里用占位符实现
        return {
            "dependent": [
                {
                    "name": "ROA",
                    "full_name": "资产收益率",
                    "definition": "净利润/总资产",
                    "calculation": "年末净利润/年末总资产",
                    "unit": "百分比",
                    "source": "CSMAR数据库",
                    "hypothesis": ["H1", "H2"]
                },
                {
                    "name": "TobinQ",
                    "full_name": "托宾Q值",
                    "definition": "公司市场价值/资产重置成本",
                    "calculation": "公司市值/总资产",
                    "unit": "比率",
                    "source": "CSMAR数据库",
                    "hypothesis": ["H1", "H3"]
                }
            ],
            "independent": [
                {
                    "name": f"{self.topic}指数",
                    "full_name": f"{self.topic}水平指标",
                    "definition": f"衡量企业{self.topic}水平的综合指标",
                    "calculation": "基于多维度指标构建的综合评分",
                    "unit": "指数值",
                    "source": "中国工商银行经济研究所",
                    "hypothesis": ["H1", "H2", "H3"]
                }
            ],
            "moderating": [
                {
                    "name": "制度环境",
                    "full_name": "地区制度环境质量",
                    "definition": "地区市场化和法治环境水平",
                    "calculation": "基于王小鲁市场化指数",
                    "unit": "指数值",
                    "source": "《中国分省市场化指数报告》",
                    "hypothesis": ["H2"]
                }
            ],
            "control": [
                {
                    "name": "公司规模",
                    "full_name": "企业资产规模",
                    "definition": "企业总资产的自然对数",
                    "calculation": "ln(总资产)",
                    "unit": "对数值",
                    "source": "CSMAR数据库",
                    "hypothesis": ["H1", "H2", "H3"]
                },
                {
                    "name": "资产负债率",
                    "full_name": "企业负债水平",
                    "definition": "总负债/总资产",
                    "calculation": "年末总负债/年末总资产",
                    "unit": "百分比",
                    "source": "CSMAR数据库",
                    "hypothesis": ["H1", "H2", "H3"]
                },
                {
                    "name": "公司年龄",
                    "full_name": "企业存续时间",
                    "definition": "企业成立至今的年数",
                    "calculation": "观测年份-成立年份",
                    "unit": "年",
                    "source": "CSMAR数据库",
                    "hypothesis": ["H1", "H3"]
                }
            ]
        }
    
    def _determine_analytical_methods(self) -> List[Dict[str, Any]]:
        """确定分析方法"""
        # 实际实现中，应基于假设和变量确定合适的分析方法
        # 这里用占位符实现
        return [
            {
                "name": "描述性统计",
                "purpose": "了解各变量的基本统计特征",
                "tools": ["均值", "标准差", "最小值", "最大值", "相关系数"],
                "software": "Stata 16.0",
                "presentation": "表格形式展示"
            },
            {
                "name": "面板数据回归",
                "purpose": "检验假设H1和H2",
                "model": "Yit = α + β1Xit + β2Zit + β3Xit·Zit + ∑βnControlsit + μi + λt + εit",
                "estimation": "固定效应模型",
                "robustness": [
                    "替换因变量",
                    "替换估计方法（随机效应模型）",
                    "工具变量法处理内生性",
                    "倾向得分匹配法"
                ],
                "software": "Stata 16.0",
                "presentation": "回归表格展示"
            },
            {
                "name": "分组回归",
                "purpose": "检验假设H3",
                "model": "按不同维度分组进行回归分析",
                "groups": ["按行业分组", "按企业规模分组"],
                "estimation": "固定效应模型",
                "software": "Stata 16.0",
                "presentation": "分组回归表格展示"
            },
            {
                "name": "中介效应分析",
                "purpose": "深入探索作用机制",
                "model": "Bootstrap法检验中介效应",
                "steps": ["总效应分析", "直接效应分析", "间接效应分析", "Sobel检验"],
                "software": "R 4.1.0 (mediation包)",
                "presentation": "中介效应分析表格展示"
            }
        ]
    
    def _compose_design_content(self, design: Dict[str, Any]) -> str:
        """组合研究设计内容"""
        content = f"## 4.1 研究设计\n\n本研究采用{design['type']}方法，基于{design['approach']}视角，使用{design['design']}研究{self.topic}与企业绩效的关系。研究聚焦于{design['time_period']}期间的{design['unit_of_analysis']}，样本来源为{design['sample_scope']}。\n\n"
        
        content += "在样本筛选过程中，本研究采用以下标准：\n\n"
        for i, criterion in enumerate(design["selection_criteria"]):
            content += f"（{i+1}）{criterion}；\n"
        
        content += f"\n选择{design['design']}作为主要研究方法的理由是：{design['rationale']}。这一方法有利于控制不随时间变化的个体特征和随时间变化但对个体一致的时间效应，从而获得更为可靠的估计结果。\n\n"
        
        return content
    
    def _compose_data_content(self, data_sources: Dict[str, Any]) -> str:
        """组合数据来源内容"""
        content = f"## 4.2 数据来源与样本\n\n"
        
        # 主要数据来源
        content += "### 4.2.1 数据来源\n\n本研究的数据主要来源于以下数据库：\n\n"
        for source in data_sources["primary_sources"]:
            content += f"（1）{source['name']}：提供{source['content']}，覆盖{source['time_period']}；\n"
        
        for source in data_sources["secondary_sources"]:
            content += f"（2）{source['name']}：提供{source['content']}，覆盖{source['time_period']}；\n"
        
        # 数据处理
        content += "\n### 4.2.2 数据处理\n\n本研究的数据处理过程如下：\n\n"
        for i, process in enumerate(data_sources["data_processing"]):
            content += f"（{i+1}）{process}；\n"
        
        # 样本描述
        content += f"\n### 4.2.3 样本描述\n\n经过上述数据处理，本研究最初获取的样本包含{data_sources['sample_size']['initial']}家上市公司，经过筛选和数据清洗后，最终得到{data_sources['sample_size']['final']}家有效样本公司，共计{data_sources['sample_size']['firm_year']}个企业-年度观测值。\n\n"
        
        return content
    
    def _compose_variable_content(self, variables: Dict[str, List[Dict[str, Any]]]) -> str:
        """组合变量定义内容"""
        content = f"## 4.3 变量定义与度量\n\n"
        
        # 因变量
        content += "### 4.3.1 因变量\n\n本研究的因变量为企业绩效，采用以下指标进行测量：\n\n"
        for var in variables["dependent"]:
            hyp_str = "、".join(var["hypothesis"])
            content += f"（1）{var['full_name']}（{var['name']}）：{var['definition']}，计算方法为{var['calculation']}，数据来源于{var['source']}，用于检验{hyp_str}；\n"
        
        # 自变量
        content += "\n### 4.3.2 自变量\n\n本研究的自变量为：\n\n"
        for var in variables["independent"]:
            hyp_str = "、".join(var["hypothesis"])
            content += f"{var['full_name']}（{var['name']}）：{var['definition']}，计算方法为{var['calculation']}，数据来源于{var['source']}，用于检验{hyp_str}。\n\n"
        
        # 调节变量
        content += "### 4.3.3 调节变量\n\n本研究的调节变量为：\n\n"
        for var in variables["moderating"]:
            hyp_str = "、".join(var["hypothesis"])
            content += f"{var['full_name']}（{var['name']}）：{var['definition']}，计算方法为{var['calculation']}，数据来源于{var['source']}，用于检验{hyp_str}。\n\n"
        
        # 控制变量
        content += "### 4.3.4 控制变量\n\n为控制其他因素的影响，本研究引入以下控制变量：\n\n"
        for var in variables["control"]:
            content += f"（{variables['control'].index(var) + 1}）{var['full_name']}（{var['name']}）：{var['definition']}，计算方法为{var['calculation']}，数据来源于{var['source']}；\n"
        
        # 变量说明表
        content += "\n所有变量的定义和计算方法见表4-1。\n\n"
        content += "表4-1 变量定义及计算方法\n\n"
        
        return content
    
    def _compose_method_content(self, methods: List[Dict[str, Any]]) -> str:
        """组合分析方法内容"""
        content = f"## 4.4 分析方法\n\n本研究采用以下分析方法来检验研究假设：\n\n"
        
        for method in methods:
            content += f"### 4.4.{methods.index(method) + 1} {method['name']}\n\n"
            content += f"本研究使用{method['name']}进行分析，目的是{method['purpose']}。"
            
            if method["name"] == "描述性统计":
                tools_str = "、".join(method["tools"])
                content += f"分析包括计算所有变量的{tools_str}等统计量，使用{method['software']}进行处理，结果以{method['presentation']}。\n\n"
            
            elif method["name"] == "面板数据回归":
                robust_str = "、".join(method["robustness"])
                content += f"主要回归模型设定如下：\n\n```\n{method['model']}\n```\n\n"
                content += f"其中，Y表示因变量（企业绩效），X表示自变量（{self.topic}指数），Z表示调节变量（制度环境），Controls表示控制变量，μi表示个体固定效应，λt表示时间固定效应，εit表示随机误差项。\n\n"
                content += f"本研究主要采用{method['estimation']}进行估计。为确保结果的稳健性，还将采用{robust_str}等方法进行稳健性检验。所有分析使用{method['software']}进行，结果以{method['presentation']}。\n\n"
            
            elif method["name"] == "分组回归":
                groups_str = "、".join(method["groups"])
                content += f"为检验{self.topic}对不同维度企业绩效的影响差异，本研究采用{groups_str}的方法进行分组回归分析，使用{method['estimation']}进行估计，所有分析使用{method['software']}进行，结果以{method['presentation']}。\n\n"
            
            elif method["name"] == "中介效应分析":
                steps_str = "、".join(method["steps"])
                content += f"为深入探索{self.topic}影响企业绩效的作用机制，本研究采用中介效应分析方法，具体包括{steps_str}等步骤，使用{method['software']}进行分析，结果以{method['presentation']}。\n\n"
        
        return content
    
    def _apply_style(self, text: str) -> str:
        """应用学科风格规则到文本"""
        # 简化实现，实际应用中应更复杂
        if self.style_rules.get("formality") == "high":
            # 提高正式性
            text = text.replace("我们", "本研究").replace("使用", "采用").replace("看", "观察")
        
        if self.style_rules.get("precision") == "high":
            # 提高精确性
            text = text.replace("很多", "大量").replace("一些", "部分").replace("非常", "极其")
        
        return text
    
    def _polish_text(self, text: str) -> str:
        """最终润色文本"""
        # 简化实现
        return text

    def analyze_data(self) -> Dict[str, Any]:
        """分析数据结构和变量特征
        
        Returns:
            Dict: 包含数据分析结果的字典
        """
        try:
            results = {}
            
            # 识别数据结构
            data_structure = self.data_analyzer.identify_data_structure()
            if data_structure:
                results["data_structure"] = data_structure
            
            # 分析变量特征
            variable_analysis = self.data_analyzer.analyze_variables()
            if variable_analysis:
                results["variable_analysis"] = variable_analysis
            
            # 生成实证策略
            empirical_strategy = self.data_analyzer.generate_empirical_strategy(self.hypotheses)
            if empirical_strategy:
                results["empirical_strategy"] = empirical_strategy
            
            return results
        except Exception as e:
            self.logger.error(f"分析数据失败: {str(e)}")
            return {} 