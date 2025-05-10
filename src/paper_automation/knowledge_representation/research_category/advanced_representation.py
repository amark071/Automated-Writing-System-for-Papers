"""研究范畴矩阵的高级表示模块
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
from scipy import sparse
from .base_representation import ResearchCategoryBaseRepresentation

class ResearchCategoryAdvancedRepresentation(ResearchCategoryBaseRepresentation):
    """研究范畴矩阵的高级表示类"""
    
    def __init__(self, dimensions: List[int], data: Optional[np.ndarray] = None):
        """
        初始化研究范畴矩阵的高级表示
        
        Args:
            dimensions: 维度列表
            data: 可选的初始数据
        """
        super().__init__(dimensions, data)
        self.features = {}  # 特征字典
        self.relations = {}  # 关系字典
        
    def add_feature(self, feature_id: str, feature_data: np.ndarray) -> None:
        """添加特征
        
        Args:
            feature_id: 特征ID
            feature_data: 特征数据
        """
        if not isinstance(feature_data, np.ndarray):
            raise ValueError("Feature data must be a numpy array")
        if feature_data.shape != self.shape:
            raise ValueError(f"Feature data shape {feature_data.shape} does not match matrix shape {self.shape}")
        self.features[feature_id] = feature_data
        
    def remove_feature(self, feature_id: str) -> None:
        """移除特征
        
        Args:
            feature_id: 特征ID
        """
        if feature_id not in self.features:
            raise ValueError(f"Feature {feature_id} not found")
        del self.features[feature_id]
        
    def update_feature(self, feature_id: str, feature_data: np.ndarray) -> None:
        """更新特征
        
        Args:
            feature_id: 特征ID
            feature_data: 新的特征数据
        """
        if feature_id not in self.features:
            raise ValueError(f"Feature {feature_id} not found")
        if not isinstance(feature_data, np.ndarray):
            raise ValueError("Feature data must be a numpy array")
        if feature_data.shape != self.shape:
            raise ValueError(f"Feature data shape {feature_data.shape} does not match matrix shape {self.shape}")
        self.features[feature_id] = feature_data
        
    def add_relation(self, source_id: str, target_id: str, relation_type: str) -> None:
        """添加关系
        
        Args:
            source_id: 源ID
            target_id: 目标ID
            relation_type: 关系类型
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
        """
        if source_id not in self.relations or target_id not in self.relations[source_id]:
            raise ValueError(f"Relation from {source_id} to {target_id} not found")
        if not relation_type:
            raise ValueError("Relation type cannot be empty")
        self.relations[source_id][target_id] = relation_type
        
    def get_feature(self, feature_id: str) -> Optional[np.ndarray]:
        """获取特征
        
        Args:
            feature_id: 特征ID
            
        Returns:
            特征数据，如果不存在则返回None
        """
        return self.features.get(feature_id)
        
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