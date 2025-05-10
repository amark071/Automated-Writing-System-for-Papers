"""知识表示模块

该模块提供了三种知识表示接口：
1. 知识矩阵接口 (MatrixInterface)
2. 知识谱系接口 (SpectrumInterface)
3. 知识映射接口 (MappingInterface)
"""

from .matrix_interface import MatrixInterface
from .spectrum_interface import SpectrumInterface
from .mapping_interface import MappingInterface

__all__ = [
    'MatrixInterface',
    'SpectrumInterface',
    'MappingInterface'
] 