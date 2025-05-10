"""结论Agent，负责生成论文的结论部分。"""

import os
from typing import Dict, List, Any, Optional

from src.paper_automation.agent_system.paper_agent.base_agent import BaseAgent
from src.paper_automation.agent_system.paper_agent.style.style_rules import StyleRules


class ConclusionAgent(BaseAgent):
    """结论Agent类，负责生成论文中的结论部分。
    
    结论部分包括：
    1. 研究问题回顾
    2. 主要发现摘要
    3. 研究贡献总结
    4. 研究意义阐述
    5. 结束语
    """
    
    def __init__(self, agent_config: Dict[str, Any], style_rules: Optional[StyleRules] = None):
        """初始化结论Agent。
        
        Args:
            agent_config: Agent配置信息
            style_rules: 文体规则对象
        """
        super().__init__(agent_config, style_rules)
        self.name = "结论Agent"
        
    def generate_research_question_review(self, paper_info: Dict[str, Any]) -> str:
        """生成研究问题回顾部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            研究问题回顾部分内容
        """
        question_prompt = self._create_prompt(
            task="生成研究问题回顾部分",
            paper_info=paper_info,
            requirements=[
                "简明重述研究的主要问题或目标",
                "回顾研究的背景和动机",
                "强调研究问题的重要性",
                "不引入新的问题或概念",
                "为结论的其余部分奠定基础"
            ]
        )
        
        return self._call_llm(question_prompt)
        
    def generate_findings_summary(self, paper_info: Dict[str, Any]) -> str:
        """生成主要发现摘要部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            主要发现摘要部分内容
        """
        findings_prompt = self._create_prompt(
            task="生成主要发现摘要部分",
            paper_info=paper_info,
            requirements=[
                "简洁总结研究的核心发现",
                "强调与研究问题直接相关的结果",
                "按重要性顺序呈现发现",
                "避免引入讨论部分未提及的结果",
                "确保与论文其他部分保持一致"
            ]
        )
        
        return self._call_llm(findings_prompt)
        
    def generate_contributions_summary(self, paper_info: Dict[str, Any]) -> str:
        """生成研究贡献总结部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            研究贡献总结部分内容
        """
        contributions_prompt = self._create_prompt(
            task="生成研究贡献总结部分",
            paper_info=paper_info,
            requirements=[
                "总结研究对学术领域的主要贡献",
                "强调研究的创新点和独特价值",
                "简要回顾理论和实践贡献",
                "与现有研究的关系",
                "避免过度夸大研究成果"
            ]
        )
        
        return self._call_llm(contributions_prompt)
        
    def generate_significance(self, paper_info: Dict[str, Any]) -> str:
        """生成研究意义阐述部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            研究意义阐述部分内容
        """
        significance_prompt = self._create_prompt(
            task="生成研究意义阐述部分",
            paper_info=paper_info,
            requirements=[
                "阐述研究的更广泛意义",
                "解释研究对学科发展的影响",
                "说明研究对实际应用的价值",
                "讨论研究对未来工作的启示",
                "将研究置于更大的学术背景中"
            ]
        )
        
        return self._call_llm(significance_prompt)
        
    def generate_closing_statement(self, paper_info: Dict[str, Any]) -> str:
        """生成结束语部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            结束语部分内容
        """
        closing_prompt = self._create_prompt(
            task="生成结束语部分",
            paper_info=paper_info,
            requirements=[
                "提供有力的收尾语句",
                "强调研究的长期意义",
                "留下对读者的深刻印象",
                "避免引入全新的内容",
                "使用引人深思的方式结束论文"
            ]
        )
        
        return self._call_llm(closing_prompt)
        
    def generate_conclusion(self, paper_info: Dict[str, Any]) -> str:
        """生成完整的结论部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            完整的结论部分内容
        """
        question_review = self.generate_research_question_review(paper_info)
        findings_summary = self.generate_findings_summary(paper_info)
        contributions_summary = self.generate_contributions_summary(paper_info)
        significance = self.generate_significance(paper_info)
        closing_statement = self.generate_closing_statement(paper_info)
        
        conclusion_content = f"""
# 结论

{question_review}

{findings_summary}

{contributions_summary}

{significance}

{closing_statement}
"""
        
        return conclusion_content 