"""知识表示层

该层提供了知识矩阵和知识谱系的表示和管理功能。
"""

from .knowledge_matrix import (
    KnowledgeMatrixBaseRepresentation,
    KnowledgeMatrixAdvancedRepresentation,
    KnowledgeMatrixGenerator,
    KnowledgeMatrixOperations,
    KnowledgeMatrixAnalysis
)

from .knowledge_spectrum import (
    KnowledgeSpectrumBaseRepresentation,
    KnowledgeSpectrumAdvancedRepresentation,
    KnowledgeSpectrum
)

__all__ = [
    # 知识矩阵
    'KnowledgeMatrixBaseRepresentation',
    'KnowledgeMatrixAdvancedRepresentation',
    'KnowledgeMatrixGenerator',
    'KnowledgeMatrixOperations',
    'KnowledgeMatrixAnalysis',
    
    # 知识谱系
    'KnowledgeSpectrumBaseRepresentation',
    'KnowledgeSpectrumAdvancedRepresentation',
    'KnowledgeSpectrum'
] 