"""知识矩阵模块

该模块提供了知识矩阵的基础表示、高级表示、生成、操作和分析功能。
"""

from .base_representation import KnowledgeMatrixBaseRepresentation
from .advanced_representation import KnowledgeMatrixAdvancedRepresentation
from .matrix_generator import KnowledgeMatrixGenerator
from .matrix_operations import KnowledgeMatrixOperations
from .matrix_analysis import KnowledgeMatrixAnalysis

__all__ = [
    'KnowledgeMatrixBaseRepresentation',
    'KnowledgeMatrixAdvancedRepresentation',
    'KnowledgeMatrixGenerator',
    'KnowledgeMatrixOperations',
    'KnowledgeMatrixAnalysis'
] 