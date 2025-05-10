"""学科知识图谱模块

该模块提供了三种不同类型的知识图谱实现：
1. 特征图谱 (FeatureGraph) - 用于管理和分析特征之间的关系
2. 关系图谱 (RelationGraph) - 用于管理和分析概念之间的关系
3. 演化图谱 (EvolutionGraph) - 用于管理和分析概念随时间的演化
"""

from .feature_graph import FeatureGraph
from .relation_graph import RelationGraph
from .evolution_graph import EvolutionGraph

__all__ = [
    "FeatureGraph",
    "RelationGraph",
    "EvolutionGraph"
] 