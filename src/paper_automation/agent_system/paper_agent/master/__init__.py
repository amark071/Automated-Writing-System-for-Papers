"""总代理模块

此模块实现了论文代理系统的总代理功能，负责协调各个子代理的工作。
"""

from .master_agent import (
    MasterAgent,
    DirectionPrediction,
    PatternAnalysis
)

__all__ = [
    "MasterAgent",
    "DirectionPrediction",
    "PatternAnalysis"
] 