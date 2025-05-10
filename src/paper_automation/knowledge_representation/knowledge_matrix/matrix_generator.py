"""知识矩阵生成器模块
"""

from typing import Dict, List, Optional, Any
import numpy as np
from .base_representation import KnowledgeMatrixBaseRepresentation
from .advanced_representation import KnowledgeMatrixAdvancedRepresentation

class KnowledgeMatrixGenerator:
    """知识矩阵生成器类"""
    
    def __init__(self):
        """初始化"""
        self.dimensions = []
        self.config = {}
        
    def set_dimensions(self, dimensions: List[int]) -> None:
        """设置维度
        
        Args:
            dimensions: 维度列表
            
        Raises:
            ValueError: 当维度列表为空时
            ValueError: 当维度包含非正数时
        """
        if not dimensions:
            raise ValueError("Dimensions list cannot be empty")
        if any(d <= 0 for d in dimensions):
            raise ValueError("Dimensions must be positive")
        self.dimensions = dimensions
        
    def initialize_data(self, method: str = 'zeros') -> np.ndarray:
        """初始化数据
        
        Args:
            method: 初始化方法，可选值：zeros, ones, random
            
        Returns:
            初始化的数据
            
        Raises:
            ValueError: 当维度未设置时
            ValueError: 当初始化方法无效时
        """
        if not self.dimensions:
            raise ValueError("Dimensions not set")
            
        if method == 'zeros':
            return np.zeros(self.dimensions)
        elif method == 'ones':
            return np.ones(self.dimensions)
        elif method == 'random':
            return np.random.rand(*self.dimensions)
        else:
            raise ValueError(f"Invalid initialization method: {method}")
            
    def generate_base_matrix(self, data: Optional[np.ndarray] = None) -> KnowledgeMatrixBaseRepresentation:
        """生成基础矩阵
        
        Args:
            data: 可选的初始数据
            
        Returns:
            基础矩阵
            
        Raises:
            ValueError: 当维度未设置时
        """
        if not self.dimensions:
            raise ValueError("Dimensions not set")
            
        if data is None:
            data = self.initialize_data()
        return KnowledgeMatrixBaseRepresentation(self.dimensions, data)
        
    def generate_advanced_matrix(self, data: Optional[np.ndarray] = None,
                               features: Optional[Dict[str, np.ndarray]] = None,
                               relations: Optional[Dict[str, Dict[str, str]]] = None) -> KnowledgeMatrixAdvancedRepresentation:
        """生成高级矩阵
        
        Args:
            data: 可选的初始数据
            features: 可选的特征字典
            relations: 可选的关系字典
            
        Returns:
            高级矩阵
            
        Raises:
            ValueError: 当维度未设置时
        """
        if not self.dimensions:
            raise ValueError("Dimensions not set")
            
        if data is None:
            data = self.initialize_data()
        matrix = KnowledgeMatrixAdvancedRepresentation(self.dimensions, data)
        
        if features:
            for feature_id, feature_data in features.items():
                matrix.add_feature(feature_id, feature_data)
                
        if relations:
            for source_id, target_relations in relations.items():
                for target_id, relation_type in target_relations.items():
                    matrix.add_relation(source_id, target_id, relation_type)
                    
        return matrix 