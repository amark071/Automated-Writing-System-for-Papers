"""论文内容生成模块，包含各部分内容的生成代理。"""

from src.paper_automation.agent_system.paper_agent.content.content_agent import ContentAgent
from src.paper_automation.agent_system.paper_agent.content.introduction import IntroductionAgent
from src.paper_automation.agent_system.paper_agent.content.literature import LiteratureAgent
from src.paper_automation.agent_system.paper_agent.content.theory import TheoryAgent
from src.paper_automation.agent_system.paper_agent.content.method import MethodAgent
from src.paper_automation.agent_system.paper_agent.content.empirical import EmpiricalAgent
from src.paper_automation.agent_system.paper_agent.content.discussion import DiscussionAgent
from src.paper_automation.agent_system.paper_agent.content.conclusion import ConclusionAgent

__all__ = [
    "ContentAgent",
    "IntroductionAgent",
    "LiteratureAgent",
    "TheoryAgent",
    "MethodAgent",
    "EmpiricalAgent",
    "DiscussionAgent",
    "ConclusionAgent"
] 