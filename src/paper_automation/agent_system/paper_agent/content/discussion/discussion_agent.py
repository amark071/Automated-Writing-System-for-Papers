"""讨论Agent，负责生成论文的讨论部分。"""

import os
from typing import Dict, List, Any, Optional

from src.paper_automation.agent_system.paper_agent.base_agent import BaseAgent
from src.paper_automation.agent_system.paper_agent.style.style_rules import StyleRules


class DiscussionAgent(BaseAgent):
    """讨论Agent类，负责生成论文中的讨论部分。
    
    讨论部分包括：
    1. 主要发现总结
    2. 理论贡献分析
    3. 实践意义分析
    4. 研究局限性分析
    5. 未来研究方向建议
    """
    
    def __init__(self, agent_config: Dict[str, Any], style_rules: Optional[StyleRules] = None):
        """初始化讨论Agent。
        
        Args:
            agent_config: Agent配置信息
            style_rules: 文体规则对象
        """
        super().__init__(agent_config, style_rules)
        self.name = "讨论Agent"
        
    def generate_main_findings(self, paper_info: Dict[str, Any]) -> str:
        """生成主要发现总结部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            主要发现总结部分内容
        """
        findings_prompt = self._create_prompt(
            task="生成主要发现总结部分",
            paper_info=paper_info,
            requirements=[
                "简明扼要地总结研究的核心发现",
                "将发现与研究问题和目标关联起来",
                "强调最重要和最有创新性的发现",
                "解释发现之间的关系",
                "避免引入新的结果"
            ]
        )
        
        return self._call_llm(findings_prompt)
        
    def generate_theoretical_contributions(self, paper_info: Dict[str, Any]) -> str:
        """生成理论贡献分析部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            理论贡献分析部分内容
        """
        contributions_prompt = self._create_prompt(
            task="生成理论贡献分析部分",
            paper_info=paper_info,
            requirements=[
                "详细分析研究对现有理论的贡献",
                "说明如何扩展或挑战现有理论",
                "解释研究如何填补文献空白",
                "分析研究如何推进学术理解",
                "与现有理论框架进行对比"
            ]
        )
        
        return self._call_llm(contributions_prompt)
        
    def generate_practical_implications(self, paper_info: Dict[str, Any]) -> str:
        """生成实践意义分析部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            实践意义分析部分内容
        """
        implications_prompt = self._create_prompt(
            task="生成实践意义分析部分",
            paper_info=paper_info,
            requirements=[
                "分析研究对实际应用的价值",
                "提供具体的应用建议",
                "说明研究对相关政策的启示",
                "分析对行业实践的指导意义",
                "讨论实施建议的可行性"
            ]
        )
        
        return self._call_llm(implications_prompt)
        
    def generate_limitations(self, paper_info: Dict[str, Any]) -> str:
        """生成研究局限性分析部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            研究局限性分析部分内容
        """
        limitations_prompt = self._create_prompt(
            task="生成研究局限性分析部分",
            paper_info=paper_info,
            requirements=[
                "坦诚分析研究的主要局限性",
                "解释如何减轻这些局限性的影响",
                "讨论研究方法的潜在缺陷",
                "分析数据或样本的限制",
                "评估结果的泛化能力"
            ]
        )
        
        return self._call_llm(limitations_prompt)
        
    def generate_future_research(self, paper_info: Dict[str, Any]) -> str:
        """生成未来研究方向建议部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            未来研究方向建议部分内容
        """
        future_prompt = self._create_prompt(
            task="生成未来研究方向建议部分",
            paper_info=paper_info,
            requirements=[
                "提出有价值的后续研究方向",
                "建议解决当前研究局限性的方法",
                "推荐拓展研究范围的途径",
                "提出可以深入探索的相关问题",
                "讨论可能的方法论创新"
            ]
        )
        
        return self._call_llm(future_prompt)
        
    def generate_discussion(self, paper_info: Dict[str, Any]) -> str:
        """生成完整的讨论部分。
        
        Args:
            paper_info: 论文信息
            
        Returns:
            完整的讨论部分内容
        """
        main_findings = self.generate_main_findings(paper_info)
        theoretical_contributions = self.generate_theoretical_contributions(paper_info)
        practical_implications = self.generate_practical_implications(paper_info)
        limitations = self.generate_limitations(paper_info)
        future_research = self.generate_future_research(paper_info)
        
        discussion_content = f"""
# 讨论

## 主要发现总结
{main_findings}

## 理论贡献
{theoretical_contributions}

## 实践意义
{practical_implications}

## 研究局限性
{limitations}

## 未来研究方向
{future_research}
"""
        
        return discussion_content 