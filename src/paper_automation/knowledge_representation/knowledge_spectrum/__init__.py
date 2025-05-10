"""知识谱系模块

该模块提供了知识谱系的基础表示、高级表示和完整功能实现。
"""

from .base_representation import KnowledgeSpectrumBaseRepresentation
from .advanced_representation import KnowledgeSpectrumAdvancedRepresentation
from .knowledge_spectrum import KnowledgeSpectrum

__all__ = [
    'KnowledgeSpectrumBaseRepresentation',
    'KnowledgeSpectrumAdvancedRepresentation',
    'KnowledgeSpectrum'
] 