from typing import Dict, List, Any, Optional
import logging
from .introduction.introduction_agent import IntroductionAgent
from .literature.literature_review_agent import LiteratureReviewAgent
from .theory.theory_agent import TheoryAgent
from .method.method_agent import MethodAgent
from src.paper_automation.agent_system.paper_agent.content.empirical.empirical_agent import EmpiricalAgent
from src.paper_automation.agent_system.paper_agent.content.discussion.discussion_agent import DiscussionAgent
from src.paper_automation.agent_system.paper_agent.content.conclusion.conclusion_agent import ConclusionAgent

class ContentAgent:
    """内容主协调代理，负责协调各个专门代理生成论文内容"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.status = "initialized"
        self.knowledge_graph = None
        self.style_rules = {}
        self.topic = ""
        self.discipline = "economics"  # 默认为经济学
        self.research_position = None
        
        # 初始化各个专门代理
        self.introduction_agent = IntroductionAgent()
        self.literature_agent = LiteratureReviewAgent()
        self.theory_agent = TheoryAgent()
        self.method_agent = MethodAgent()
        self.empirical_agent = EmpiricalAgent()
        self.discussion_agent = DiscussionAgent()
        self.conclusion_agent = ConclusionAgent()
        # TODO: 初始化其他专门代理
        
    def initialize(self, topic: str, discipline: str = "economics", 
                  knowledge_graph: Optional[Dict[str, Any]] = None,
                  style_rules: Optional[Dict[str, Any]] = None,
                  research_position: Optional[Dict[str, Any]] = None) -> bool:
        """初始化内容代理
        
        Args:
            topic: 研究主题
            discipline: 学科领域，默认为经济学
            knowledge_graph: 知识图谱
            style_rules: 风格规则
            research_position: 研究定位
            
        Returns:
            初始化是否成功
        """
        try:
            self.topic = topic
            self.discipline = discipline
            self.knowledge_graph = knowledge_graph
            self.style_rules = style_rules or {}
            self.research_position = research_position
            
            # 初始化引言代理
            if not self.introduction_agent.initialize(
                topic=topic,
                discipline=discipline,
                knowledge_graph=knowledge_graph,
                style_rules=style_rules,
                research_position=research_position
            ):
                self.logger.warning("引言代理初始化失败")
            
            # 初始化文献综述代理
            if not self.literature_agent.initialize(
                topic=topic,
                discipline=discipline,
                knowledge_graph=knowledge_graph,
                style_rules=style_rules
            ):
                self.logger.warning("文献综述代理初始化失败")
            
            # 初始化理论框架代理
            research_gaps = []  # 这里应该从文献综述代理中获取研究差距
            if not self.theory_agent.initialize(
                topic=topic,
                discipline=discipline,
                knowledge_graph=knowledge_graph,
                style_rules=style_rules,
                research_gaps=research_gaps
            ):
                self.logger.warning("理论框架代理初始化失败")
            
            # 初始化研究方法代理
            hypotheses = []  # 这里应该从理论框架代理中获取假设
            if not self.method_agent.initialize(
                topic=topic,
                discipline=discipline,
                knowledge_graph=knowledge_graph,
                style_rules=style_rules,
                hypotheses=hypotheses
            ):
                self.logger.warning("研究方法代理初始化失败")
            
            # TODO: 初始化其他专门代理
            
            self.status = "ready"
            return True
        except Exception as e:
            self.logger.error(f"初始化内容代理失败: {str(e)}")
            return False
            
    def generate_section_content(self, section_name: str, context: Dict[str, Any] = None) -> str:
        """生成指定章节的内容
        
        Args:
            section_name: 章节名称
            context: 上下文信息
            
        Returns:
            生成的章节内容
        """
        try:
            context = context or {}
            
            # 根据章节名称选择相应的专门代理生成内容
            if section_name == "引言" or section_name == "introduction":
                return self.introduction_agent.generate_full_introduction()
            elif section_name == "文献综述" or section_name == "literature_review":
                return self.literature_agent.generate_full_literature_review()
            elif section_name == "理论框架" or section_name == "theoretical_framework":
                return self.theory_agent.generate_theoretical_framework()
            elif section_name == "研究设计" or section_name == "method" or section_name == "research_design":
                return self.method_agent.generate_research_method()
            elif section_name == "实证分析" or section_name == "empirical_analysis":
                return self.empirical_agent.generate_empirical_analysis(context)
            elif section_name == "讨论" or section_name == "discussion":
                return self.discussion_agent.generate_discussion(context)
            elif section_name == "结论" or section_name == "conclusion":
                return self.conclusion_agent.generate_conclusion(context)
            else:
                self.logger.warning(f"未知章节名称: {section_name}")
                return f"暂不支持生成 {section_name} 章节的内容"
        except Exception as e:
            self.logger.error(f"生成章节内容失败: {str(e)}")
            return ""
    
    def generate_block_content(self, section_name: str, block_name: str, context: Dict[str, Any] = None) -> str:
        """生成指定板块的内容
        
        Args:
            section_name: 章节名称
            block_name: 板块名称
            context: 上下文信息
            
        Returns:
            生成的板块内容
        """
        try:
            context = context or {}
            
            # 引言章节的板块
            if section_name == "引言" or section_name == "introduction":
                if block_name == "研究背景" or block_name == "background":
                    return self.introduction_agent.generate_research_background()
                elif block_name == "研究问题" or block_name == "research_questions":
                    questions = self.introduction_agent.generate_research_questions()
                    return self.introduction_agent._format_questions(questions)
                elif block_name == "研究方法" or block_name == "approach":
                    return self.introduction_agent.generate_research_approach()
                elif block_name == "论文结构" or block_name == "structure":
                    return self.introduction_agent.generate_paper_structure()
            
            # 文献综述章节的板块
            elif section_name == "文献综述" or section_name == "literature_review":
                if block_name == "理论基础" or block_name == "theoretical_foundation":
                    return self.literature_agent.generate_theoretical_foundation()
                elif block_name == "研究现状" or block_name == "research_status":
                    return self.literature_agent.generate_research_status()
                elif block_name == "研究差距" or block_name == "research_gaps":
                    return self.literature_agent.generate_research_gaps()
                elif block_name == "文献评价" or block_name == "literature_summary":
                    return self.literature_agent.generate_literature_summary()
            
            # 理论框架章节的板块
            elif section_name == "理论框架" or section_name == "theoretical_framework":
                if block_name == "概念界定" or block_name == "concepts":
                    return self.theory_agent.generate_concept_definitions()
                elif block_name == "模型构建" or block_name == "model":
                    return self.theory_agent.generate_model_construction()
                elif block_name == "研究假设" or block_name == "hypotheses":
                    return self.theory_agent.generate_hypotheses()
                elif block_name == "理论推导" or block_name == "derivation":
                    return self.theory_agent.generate_theoretical_derivation()
            
            # 研究方法章节的板块
            elif section_name == "研究设计" or section_name == "method" or section_name == "research_design":
                if block_name == "研究设计" or block_name == "design":
                    return self.method_agent.generate_research_design()
                elif block_name == "数据来源" or block_name == "data":
                    return self.method_agent.generate_data_sources()
                elif block_name == "变量定义" or block_name == "variables":
                    return self.method_agent.generate_variable_definitions()
                elif block_name == "分析方法" or block_name == "analysis":
                    return self.method_agent.generate_analytical_methods()
            
            # 实证分析章节的板块
            elif section_name == "实证分析" or section_name == "empirical_analysis":
                if block_name == "数据收集" or block_name == "data_collection":
                    return self.empirical_agent.generate_data_collection(context)
                elif block_name == "变量定义" or block_name == "variable_definition":
                    return self.empirical_agent.generate_variable_definition(context)
                elif block_name == "描述性统计" or block_name == "descriptive_statistics":
                    return self.empirical_agent.generate_descriptive_statistics(context)
                elif block_name == "实证结果" or block_name == "empirical_results":
                    return self.empirical_agent.generate_empirical_results(context)
                elif block_name == "稳健性检验" or block_name == "robustness_tests":
                    return self.empirical_agent.generate_robustness_tests(context)
            
            # 讨论章节的板块
            elif section_name == "讨论" or section_name == "discussion":
                if block_name == "主要发现" or block_name == "main_findings":
                    return self.discussion_agent.generate_main_findings(context)
                elif block_name == "理论贡献" or block_name == "theoretical_contributions":
                    return self.discussion_agent.generate_theoretical_contributions(context)
                elif block_name == "实践意义" or block_name == "practical_implications":
                    return self.discussion_agent.generate_practical_implications(context)
                elif block_name == "研究局限性" or block_name == "limitations":
                    return self.discussion_agent.generate_limitations(context)
                elif block_name == "未来研究" or block_name == "future_research":
                    return self.discussion_agent.generate_future_research(context)
            
            # 结论章节的板块
            elif section_name == "结论" or section_name == "conclusion":
                if block_name == "研究问题回顾" or block_name == "question_review":
                    return self.conclusion_agent.generate_research_question_review(context)
                elif block_name == "主要发现摘要" or block_name == "findings_summary":
                    return self.conclusion_agent.generate_findings_summary(context)
                elif block_name == "研究贡献" or block_name == "contributions_summary":
                    return self.conclusion_agent.generate_contributions_summary(context)
                elif block_name == "研究意义" or block_name == "significance":
                    return self.conclusion_agent.generate_significance(context)
                elif block_name == "结束语" or block_name == "closing_statement":
                    return self.conclusion_agent.generate_closing_statement(context)
            
            self.logger.warning(f"未知章节或板块名称: {section_name} - {block_name}")
            return f"暂不支持生成 {section_name} 章节下 {block_name} 板块的内容"
        except Exception as e:
            self.logger.error(f"生成板块内容失败: {str(e)}")
            return ""
    
    def generate_full_paper(self, template: Dict[str, Any] = None) -> Dict[str, str]:
        """生成完整论文内容
        
        Args:
            template: 论文模板
            
        Returns:
            各章节内容的字典
        """
        try:
            template = template or self._get_default_template()
            
            paper_content = {}
            for section in template.get("sections", []):
                section_name = section.get("name", "")
                paper_content[section_name] = self.generate_section_content(section_name)
                
            return paper_content
        except Exception as e:
            self.logger.error(f"生成完整论文失败: {str(e)}")
            return {}
    
    def _get_default_template(self) -> Dict[str, Any]:
        """获取默认的论文模板"""
        if self.discipline == "economics":
            return {
                "title": f"{self.topic}研究",
                "sections": [
                    {"name": "引言", "required": True},
                    {"name": "文献综述", "required": True},
                    {"name": "理论框架", "required": True},
                    {"name": "研究设计", "required": True},
                    {"name": "实证分析", "required": True},
                    {"name": "结论与启示", "required": True}
                ]
            }
        else:
            # 其他学科的默认模板
            return {
                "title": f"{self.topic}研究",
                "sections": [
                    {"name": "引言", "required": True},
                    {"name": "文献综述", "required": True},
                    {"name": "方法", "required": True},
                    {"name": "结果", "required": True},
                    {"name": "讨论", "required": True},
                    {"name": "结论", "required": True}
                ]
            }
    
    def ensure_content_consistency(self, content: Dict[str, str]) -> Dict[str, str]:
        """确保内容一致性
        
        Args:
            content: 各章节内容的字典
            
        Returns:
            处理后的内容字典
        """
        try:
            # 简单实现，实际应用中应更复杂
            # 确保各章节之间的引用、术语、概念一致
            return content
        except Exception as e:
            self.logger.error(f"确保内容一致性失败: {str(e)}")
            return content
            
    def generate_full_content(self, paper_info: Dict[str, Any]) -> str:
        """生成完整的论文内容。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            完整的论文内容
        """
        # 分别生成各部分内容
        introduction = self.introduction_agent.generate_full_introduction()
        literature = self.literature_agent.generate_full_literature_review()
        theory = self.theory_agent.generate_theoretical_framework(paper_info)
        method = self.method_agent.generate_research_method(paper_info)
        empirical = self.empirical_agent.generate_empirical_analysis(paper_info)
        discussion = self.discussion_agent.generate_discussion(paper_info)
        conclusion = self.conclusion_agent.generate_conclusion(paper_info)
        
        # 整合所有内容
        content = f"""
{introduction}

{literature}

{theory}

{method}

{empirical}

{discussion}

{conclusion}
"""
        
        return content 