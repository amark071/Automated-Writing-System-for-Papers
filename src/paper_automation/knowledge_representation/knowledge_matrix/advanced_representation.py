"""知识矩阵的高级表示模块
"""

from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from scipy import sparse
from .base_representation import KnowledgeMatrixBaseRepresentation

class KnowledgeMatrixAdvancedRepresentation(KnowledgeMatrixBaseRepresentation):
    """知识矩阵的高级表示类"""
    
    def __init__(self, dimensions: List[int], data: Optional[np.ndarray] = None):
        """
        初始化知识矩阵的高级表示
        
        Args:
            dimensions: 维度列表
            data: 可选的初始数据
        """
        super().__init__(dimensions, data)
        self.features: Dict[str, np.ndarray] = {}
        self.relations: Dict[str, Dict[str, str]] = {}
        
    def add_feature(self, feature_id: str, feature_data: np.ndarray) -> None:
        """添加特征
        
        Args:
            feature_id: 特征ID
            feature_data: 特征数据。可以是一维向量或二维矩阵
            
        Raises:
            ValueError: 当特征ID为空时
            ValueError: 当特征数据维度不匹配时
        """
        if not feature_id:
            raise ValueError("Feature ID cannot be empty")
            
        # 如果是一维向量,将其转换为对角矩阵
        if len(feature_data.shape) == 1:
            if feature_data.shape[0] != self.shape[0]:
                raise ValueError(f"Feature vector length {feature_data.shape[0]} does not match matrix dimension {self.shape[0]}")
            feature_matrix = np.zeros(self.shape)
            np.fill_diagonal(feature_matrix, feature_data)
            self.features[feature_id] = feature_matrix
        else:
            # 如果是二维矩阵,检查维度是否匹配
            if feature_data.shape != self.shape:
                raise ValueError(f"Feature matrix shape {feature_data.shape} does not match matrix shape {self.shape}")
            self.features[feature_id] = feature_data
        
    def remove_feature(self, feature_id: str) -> None:
        """移除特征
        
        Args:
            feature_id: 特征ID
            
        Raises:
            ValueError: 当特征不存在时
        """
        if feature_id not in self.features:
            raise ValueError(f"Feature {feature_id} not found")
        del self.features[feature_id]
        
    def update_feature(self, feature_id: str, feature_data: np.ndarray) -> None:
        """更新特征
        
        Args:
            feature_id: 特征ID
            feature_data: 新的特征数据
            
        Raises:
            ValueError: 当特征不存在时
            ValueError: 当特征数据形状不匹配时
        """
        if feature_id not in self.features:
            raise ValueError(f"Feature {feature_id} not found")
        if feature_data.shape != self.shape:
            raise ValueError(f"Feature data shape {feature_data.shape} does not match matrix shape {self.shape}")
        self.features[feature_id] = feature_data
        
    def add_relation(self, source_id: str, target_id: str, relation_type: str) -> None:
        """添加关系
        
        Args:
            source_id: 源ID
            target_id: 目标ID
            relation_type: 关系类型
            
        Raises:
            ValueError: 当任何参数为空时
        """
        if not source_id or not target_id or not relation_type:
            raise ValueError("Source ID, target ID and relation type cannot be empty")
        if source_id not in self.relations:
            self.relations[source_id] = {}
        self.relations[source_id][target_id] = relation_type
        
    def remove_relation(self, source_id: str, target_id: str) -> None:
        """移除关系
        
        Args:
            source_id: 源ID
            target_id: 目标ID
            
        Raises:
            ValueError: 当关系不存在时
        """
        if source_id not in self.relations:
            raise ValueError(f"Source {source_id} not found")
        if target_id not in self.relations[source_id]:
            raise ValueError(f"Relation from {source_id} to {target_id} not found")
        del self.relations[source_id][target_id]
        if not self.relations[source_id]:
            del self.relations[source_id]
            
    def update_relation(self, source_id: str, target_id: str, relation_type: str) -> None:
        """更新关系
        
        Args:
            source_id: 源ID
            target_id: 目标ID
            relation_type: 新的关系类型
            
        Raises:
            ValueError: 当关系不存在时
            ValueError: 当关系类型为空时
        """
        if source_id not in self.relations or target_id not in self.relations[source_id]:
            raise ValueError(f"Relation from {source_id} to {target_id} not found")
        if not relation_type:
            raise ValueError("Relation type cannot be empty")
        self.relations[source_id][target_id] = relation_type
        
    def get_feature(self, feature_id: str) -> np.ndarray:
        """获取特征
        
        Args:
            feature_id: 特征ID
            
        Returns:
            特征数据
            
        Raises:
            ValueError: 当特征不存在时
        """
        if feature_id not in self.features:
            raise ValueError(f"Feature {feature_id} not found")
        return self.features[feature_id]
        
    def get_relations(self, source_id: str) -> Dict[str, str]:
        """获取关系
        
        Args:
            source_id: 源ID
            
        Returns:
            关系字典
        """
        return self.relations.get(source_id, {})
        
    def to_sparse(self) -> sparse.csr_matrix:
        """转换为稀疏矩阵
        
        Returns:
            稀疏矩阵
        """
        return sparse.csr_matrix(self.data)
        
    def from_sparse(self, sparse_matrix: sparse.csr_matrix) -> None:
        """从稀疏矩阵加载
        
        Args:
            sparse_matrix: 稀疏矩阵
        """
        self.data = sparse_matrix.toarray()

    def transform(self, method: str = 'standard') -> np.ndarray:
        """
        转换知识表示
        
        Args:
            method: 转换方法，可选 'standard', 'normalized'
            
        Returns:
            转换后的数组
        """
        if method == 'standard':
            return (self.data - np.mean(self.data)) / np.std(self.data)
        elif method == 'normalized':
            return (self.data - np.min(self.data)) / (np.max(self.data) - np.min(self.data))
        else:
            raise ValueError(f"不支持的转换方法: {method}")
            
    def analyze(self) -> Dict[str, Any]:
        """分析矩阵
        
        Returns:
            分析结果
        """
        return {
            'features': len(self.features),
            'relations': sum(len(relations) for relations in self.relations.values()),
            'shape': self.shape
        } 