"""知识矩阵基础表示模块
"""

from typing import List, Optional, Tuple, Union
import numpy as np

class KnowledgeMatrixBaseRepresentation:
    """知识矩阵基础表示类"""
    
    def __init__(self, dimensions: List[int], data: Optional[np.ndarray] = None):
        """初始化
        
        Args:
            dimensions: 维度列表
            data: 可选的初始数据
            
        Raises:
            ValueError: 当维度列表为空时
            ValueError: 当维度包含非正数时
            ValueError: 当数据形状不匹配时
        """
        if not dimensions:
            raise ValueError("Dimensions list cannot be empty")
        if any(d <= 0 for d in dimensions):
            raise ValueError("Dimensions must be positive")
            
        self.dimensions = dimensions
        if data is None:
            self.data = np.zeros(dimensions)
        else:
            if not isinstance(data, np.ndarray):
                raise ValueError("Data must be a numpy array")
            if list(data.shape) != dimensions:
                raise ValueError(f"Data shape {data.shape} does not match dimensions {dimensions}")
            self.data = data.copy()
            
    @property
    def shape(self) -> Tuple[int, ...]:
        """获取形状
        
        Returns:
            形状元组
        """
        return self.data.shape
        
    def __getitem__(self, key):
        """获取元素
        
        Args:
            key: 索引
            
        Returns:
            元素值
        """
        return self.data[key]
        
    def __setitem__(self, key, value):
        """设置元素
        
        Args:
            key: 索引
            value: 值
        """
        self.data[key] = value
        
    def __add__(self, other: Union['KnowledgeMatrixBaseRepresentation', np.ndarray]) -> 'KnowledgeMatrixBaseRepresentation':
        """加法运算
        
        Args:
            other: 另一个矩阵或数组
            
        Returns:
            新的矩阵
            
        Raises:
            ValueError: 当操作数类型不支持时
            ValueError: 当形状不匹配时
        """
        if isinstance(other, KnowledgeMatrixBaseRepresentation):
            if self.shape != other.shape:
                raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
            return KnowledgeMatrixBaseRepresentation(self.dimensions, self.data + other.data)
        elif isinstance(other, np.ndarray):
            if self.shape != other.shape:
                raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
            return KnowledgeMatrixBaseRepresentation(self.dimensions, self.data + other)
        else:
            raise ValueError(f"Unsupported operand type: {type(other)}")
            
    def __sub__(self, other: Union['KnowledgeMatrixBaseRepresentation', np.ndarray]) -> 'KnowledgeMatrixBaseRepresentation':
        """减法运算
        
        Args:
            other: 另一个矩阵或数组
            
        Returns:
            新的矩阵
            
        Raises:
            ValueError: 当操作数类型不支持时
            ValueError: 当形状不匹配时
        """
        if isinstance(other, KnowledgeMatrixBaseRepresentation):
            if self.shape != other.shape:
                raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
            return KnowledgeMatrixBaseRepresentation(self.dimensions, self.data - other.data)
        elif isinstance(other, np.ndarray):
            if self.shape != other.shape:
                raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
            return KnowledgeMatrixBaseRepresentation(self.dimensions, self.data - other)
        else:
            raise ValueError(f"Unsupported operand type: {type(other)}")
            
    def __mul__(self, other: Union['KnowledgeMatrixBaseRepresentation', np.ndarray, float, int]) -> 'KnowledgeMatrixBaseRepresentation':
        """乘法运算
        
        Args:
            other: 另一个矩阵、数组或标量
            
        Returns:
            新的矩阵
            
        Raises:
            ValueError: 当操作数类型不支持时
            ValueError: 当形状不匹配时
        """
        if isinstance(other, (float, int)):
            return KnowledgeMatrixBaseRepresentation(self.dimensions, self.data * other)
        elif isinstance(other, KnowledgeMatrixBaseRepresentation):
            if self.shape != other.shape:
                raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
            return KnowledgeMatrixBaseRepresentation(self.dimensions, self.data * other.data)
        elif isinstance(other, np.ndarray):
            if self.shape != other.shape:
                raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
            return KnowledgeMatrixBaseRepresentation(self.dimensions, self.data * other)
        else:
            raise ValueError(f"Unsupported operand type: {type(other)}")
            
    def __truediv__(self, other: Union['KnowledgeMatrixBaseRepresentation', np.ndarray, float, int]) -> 'KnowledgeMatrixBaseRepresentation':
        """除法运算
        
        Args:
            other: 另一个矩阵、数组或标量
            
        Returns:
            新的矩阵
            
        Raises:
            ValueError: 当操作数类型不支持时
            ValueError: 当形状不匹配时
            ZeroDivisionError: 当除数为零时
        """
        if isinstance(other, (float, int)):
            if other == 0:
                raise ZeroDivisionError("Division by zero")
            return KnowledgeMatrixBaseRepresentation(self.dimensions, self.data / other)
        elif isinstance(other, KnowledgeMatrixBaseRepresentation):
            if self.shape != other.shape:
                raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
            if np.any(other.data == 0):
                raise ZeroDivisionError("Division by zero")
            return KnowledgeMatrixBaseRepresentation(self.dimensions, self.data / other.data)
        elif isinstance(other, np.ndarray):
            if self.shape != other.shape:
                raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")
            if np.any(other == 0):
                raise ZeroDivisionError("Division by zero")
            return KnowledgeMatrixBaseRepresentation(self.dimensions, self.data / other)
        else:
            raise ValueError(f"Unsupported operand type: {type(other)}")
            
    def __neg__(self) -> 'KnowledgeMatrixBaseRepresentation':
        """负号运算
        
        Returns:
            新的矩阵
        """
        return KnowledgeMatrixBaseRepresentation(self.dimensions, -self.data)
        
    def __pos__(self) -> 'KnowledgeMatrixBaseRepresentation':
        """正号运算
        
        Returns:
            新的矩阵
        """
        return KnowledgeMatrixBaseRepresentation(self.dimensions, +self.data)
        
    def __eq__(self, other: object) -> bool:
        """相等比较
        
        Args:
            other: 另一个对象
            
        Returns:
            是否相等
        """
        if not isinstance(other, KnowledgeMatrixBaseRepresentation):
            return False
        return np.array_equal(self.data, other.data) and self.dimensions == other.dimensions