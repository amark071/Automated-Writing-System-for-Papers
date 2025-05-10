"""
论文代理系统，负责生成完整的学术论文。

主要组件：
- ContentAgent: 内容代理，负责协调各个章节代理生成论文内容
- IntroductionAgent: 引言代理，负责生成论文的引言部分
- LiteratureAgent: 文献综述代理，负责生成论文的文献综述部分
- TheoryAgent: 理论框架代理，负责生成论文的理论框架部分
- MethodAgent: 研究方法代理，负责生成论文的研究方法部分
- EmpiricalAgent: 实证分析代理，负责生成论文的实证分析部分
- DiscussionAgent: 讨论代理，负责生成论文的讨论部分
- ConclusionAgent: 结论代理，负责生成论文的结论部分
"""

from .content import ContentAgent
from .content.introduction import IntroductionAgent
from .content.literature import LiteratureAgent
from .content.theory import TheoryAgent
from .content.method import MethodAgent
from .content.empirical import EmpiricalAgent
from .content.discussion import DiscussionAgent
from .content.conclusion import ConclusionAgent

__all__ = [
    'ContentAgent',
    'IntroductionAgent',
    'LiteratureAgent',
    'TheoryAgent',
    'MethodAgent',
    'EmpiricalAgent',
    'DiscussionAgent',
    'ConclusionAgent'
] 