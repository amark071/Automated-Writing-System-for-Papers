"""知识谱系的基础表示模块
"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np

class KnowledgeSpectrumBaseRepresentation:
    """知识谱系的基础表示类"""
    
    def __init__(self, dimensions: List[int], data: Optional[np.ndarray] = None):
        """
        初始化知识谱系的基础表示
        
        Args:
            dimensions: 维度列表
            data: 可选的初始数据
            
        Raises:
            ValueError: 当维度列表为空或包含非正数时
            ValueError: 当数据形状与指定维度不匹配时
        """
        if not dimensions:
            raise ValueError("维度列表不能为空")
        if any(d <= 0 for d in dimensions):
            raise ValueError("维度必须为正数")
            
        self.dimensions = dimensions
        if data is None:
            self.data = np.zeros(dimensions)
        else:
            if not isinstance(data, np.ndarray):
                raise ValueError("数据必须是numpy数组")
            if list(data.shape) != dimensions:
                raise ValueError(f"数据形状 {data.shape} 与指定维度 {dimensions} 不匹配")
            self.data = data.copy()
            
    @property
    def shape(self) -> Tuple[int, ...]:
        """获取数据形状"""
        return self.data.shape
        
    def __getitem__(self, indices: Tuple[int, ...]) -> float:
        """获取数据元素
        
        Args:
            indices: 索引元组
            
        Returns:
            数据元素值
        """
        return self.data[indices]
        
    def __setitem__(self, indices: Tuple[int, ...], value: float) -> None:
        """设置数据元素
        
        Args:
            indices: 索引元组
            value: 要设置的值
        """
        self.data[indices] = value
        
    def __str__(self) -> str:
        """字符串表示"""
        return f"KnowledgeSpectrumBaseRepresentation(shape={self.shape})\n{self.data}"
        
    def __repr__(self) -> str:
        """详细字符串表示"""
        return self.__str__()
        
    def __add__(self, other: Union['KnowledgeSpectrumBaseRepresentation', np.ndarray]) -> 'KnowledgeSpectrumBaseRepresentation':
        """加法运算
        
        Args:
            other: 另一个知识谱系或numpy数组
            
        Returns:
            新的知识谱系
            
        Raises:
            ValueError: 当操作数类型不支持时
            ValueError: 当形状不匹配时
        """
        if isinstance(other, KnowledgeSpectrumBaseRepresentation):
            if self.shape != other.shape:
                raise ValueError(f"形状不匹配: {self.shape} vs {other.shape}")
            return KnowledgeSpectrumBaseRepresentation(self.dimensions, self.data + other.data)
        elif isinstance(other, np.ndarray):
            if self.shape != other.shape:
                raise ValueError(f"形状不匹配: {self.shape} vs {other.shape}")
            return KnowledgeSpectrumBaseRepresentation(self.dimensions, self.data + other)
        else:
            raise ValueError(f"不支持的操作数类型: {type(other)}")
            
    def __sub__(self, other: Union['KnowledgeSpectrumBaseRepresentation', np.ndarray]) -> 'KnowledgeSpectrumBaseRepresentation':
        """减法运算
        
        Args:
            other: 另一个知识谱系或numpy数组
            
        Returns:
            新的知识谱系
            
        Raises:
            ValueError: 当操作数类型不支持时
            ValueError: 当形状不匹配时
        """
        if isinstance(other, KnowledgeSpectrumBaseRepresentation):
            if self.shape != other.shape:
                raise ValueError(f"形状不匹配: {self.shape} vs {other.shape}")
            return KnowledgeSpectrumBaseRepresentation(self.dimensions, self.data - other.data)
        elif isinstance(other, np.ndarray):
            if self.shape != other.shape:
                raise ValueError(f"形状不匹配: {self.shape} vs {other.shape}")
            return KnowledgeSpectrumBaseRepresentation(self.dimensions, self.data - other)
        else:
            raise ValueError(f"不支持的操作数类型: {type(other)}")
            
    def __mul__(self, other: Union['KnowledgeSpectrumBaseRepresentation', np.ndarray, float, int]) -> 'KnowledgeSpectrumBaseRepresentation':
        """乘法运算
        
        Args:
            other: 另一个知识谱系、numpy数组或标量
            
        Returns:
            新的知识谱系
            
        Raises:
            ValueError: 当操作数类型不支持时
            ValueError: 当形状不匹配时
        """
        if isinstance(other, (float, int)):
            return KnowledgeSpectrumBaseRepresentation(self.dimensions, self.data * other)
        elif isinstance(other, KnowledgeSpectrumBaseRepresentation):
            if self.shape != other.shape:
                raise ValueError(f"形状不匹配: {self.shape} vs {other.shape}")
            return KnowledgeSpectrumBaseRepresentation(self.dimensions, self.data * other.data)
        elif isinstance(other, np.ndarray):
            if self.shape != other.shape:
                raise ValueError(f"形状不匹配: {self.shape} vs {other.shape}")
            return KnowledgeSpectrumBaseRepresentation(self.dimensions, self.data * other)
        else:
            raise ValueError(f"不支持的操作数类型: {type(other)}")
            
    def __rmul__(self, other: Union[float, int]) -> 'KnowledgeSpectrumBaseRepresentation':
        """反向乘法运算
        
        Args:
            other: 标量
            
        Returns:
            新的知识谱系
            
        Raises:
            ValueError: 当操作数类型不支持时
        """
        if isinstance(other, (float, int)):
            return KnowledgeSpectrumBaseRepresentation(self.dimensions, other * self.data)
        else:
            raise ValueError(f"不支持的操作数类型: {type(other)}")
            
    def __truediv__(self, other: Union['KnowledgeSpectrumBaseRepresentation', np.ndarray, float, int]) -> 'KnowledgeSpectrumBaseRepresentation':
        """除法运算
        
        Args:
            other: 另一个知识谱系、numpy数组或标量
            
        Returns:
            新的知识谱系
            
        Raises:
            ValueError: 当操作数类型不支持时
            ValueError: 当形状不匹配时
            ZeroDivisionError: 当除数为零时
        """
        if isinstance(other, (float, int)):
            if other == 0:
                raise ZeroDivisionError("除数不能为零")
            return KnowledgeSpectrumBaseRepresentation(self.dimensions, self.data / other)
        elif isinstance(other, KnowledgeSpectrumBaseRepresentation):
            if self.shape != other.shape:
                raise ValueError(f"形状不匹配: {self.shape} vs {other.shape}")
            if np.any(other.data == 0):
                raise ZeroDivisionError("除数不能为零")
            return KnowledgeSpectrumBaseRepresentation(self.dimensions, self.data / other.data)
        elif isinstance(other, np.ndarray):
            if self.shape != other.shape:
                raise ValueError(f"形状不匹配: {self.shape} vs {other.shape}")
            if np.any(other == 0):
                raise ZeroDivisionError("除数不能为零")
            return KnowledgeSpectrumBaseRepresentation(self.dimensions, self.data / other)
        else:
            raise ValueError(f"不支持的操作数类型: {type(other)}")
            
    def __neg__(self) -> 'KnowledgeSpectrumBaseRepresentation':
        """负号运算
        
        Returns:
            新的知识谱系
        """
        return KnowledgeSpectrumBaseRepresentation(self.dimensions, -self.data)
        
    def __pos__(self) -> 'KnowledgeSpectrumBaseRepresentation':
        """正号运算
        
        Returns:
            新的知识谱系
        """
        return KnowledgeSpectrumBaseRepresentation(self.dimensions, +self.data)
        
    def __eq__(self, other: object) -> bool:
        """相等比较
        
        Args:
            other: 另一个对象
            
        Returns:
            是否相等
        """
        if not isinstance(other, KnowledgeSpectrumBaseRepresentation):
            return False
        return np.array_equal(self.data, other.data) and self.dimensions == other.dimensions 