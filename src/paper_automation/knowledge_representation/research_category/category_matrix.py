"""研究范畴矩阵模块
"""

from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from scipy import sparse
from .base_representation import ResearchCategoryBaseRepresentation
from .advanced_representation import ResearchCategoryAdvancedRepresentation

class ResearchCategoryMatrix:
    """研究范畴矩阵类"""
    
    def __init__(self, dimensions: List[int], data: Optional[np.ndarray] = None):
        """
        初始化研究范畴矩阵
        
        Args:
            dimensions: 维度列表
            data: 可选的初始数据
        """
        self.base = ResearchCategoryBaseRepresentation(dimensions, data)
        self.advanced = ResearchCategoryAdvancedRepresentation(dimensions, data)
        self.categories = {}  # 范畴字典
        self.relations = {}  # 关系字典
        
    def add_category(self, category_id: str, attributes: Dict[str, Any]) -> None:
        """添加研究范畴
        
        Args:
            category_id: 范畴ID
            attributes: 范畴属性
        """
        if not category_id:
            raise ValueError("Category ID cannot be empty")
        if category_id in self.categories:
            raise ValueError(f"Category {category_id} already exists")
        self.categories[category_id] = attributes
        
    def remove_category(self, category_id: str) -> None:
        """移除研究范畴
        
        Args:
            category_id: 范畴ID
        """
        if category_id not in self.categories:
            raise ValueError(f"Category {category_id} not found")
        del self.categories[category_id]
        # 移除相关的关系
        if category_id in self.relations:
            del self.relations[category_id]
        for relations in self.relations.values():
            if category_id in relations:
                del relations[category_id]
                
    def update_category(self, category_id: str, attributes: Dict[str, Any]) -> None:
        """更新研究范畴
        
        Args:
            category_id: 范畴ID
            attributes: 新的范畴属性
        """
        if category_id not in self.categories:
            raise ValueError(f"Category {category_id} not found")
        self.categories[category_id].update(attributes)
        
    def add_relation(self, source_id: str, target_id: str, relation_type: str) -> None:
        """添加范畴关系
        
        Args:
            source_id: 源范畴ID
            target_id: 目标范畴ID
            relation_type: 关系类型
        """
        if not source_id or not target_id or not relation_type:
            raise ValueError("Source ID, target ID and relation type cannot be empty")
        if source_id not in self.categories:
            raise ValueError(f"Source category {source_id} not found")
        if target_id not in self.categories:
            raise ValueError(f"Target category {target_id} not found")
        if source_id not in self.relations:
            self.relations[source_id] = {}
        self.relations[source_id][target_id] = relation_type
        
    def remove_relation(self, source_id: str, target_id: str) -> None:
        """移除范畴关系
        
        Args:
            source_id: 源范畴ID
            target_id: 目标范畴ID
        """
        if source_id not in self.relations:
            raise ValueError(f"Source category {source_id} not found")
        if target_id not in self.relations[source_id]:
            raise ValueError(f"Relation from {source_id} to {target_id} not found")
        del self.relations[source_id][target_id]
        if not self.relations[source_id]:
            del self.relations[source_id]
            
    def update_relation(self, source_id: str, target_id: str, relation_type: str) -> None:
        """更新范畴关系
        
        Args:
            source_id: 源范畴ID
            target_id: 目标范畴ID
            relation_type: 新的关系类型
        """
        if source_id not in self.relations or target_id not in self.relations[source_id]:
            raise ValueError(f"Relation from {source_id} to {target_id} not found")
        if not relation_type:
            raise ValueError("Relation type cannot be empty")
        self.relations[source_id][target_id] = relation_type
        
    def get_category(self, category_id: str) -> Optional[Dict[str, Any]]:
        """获取研究范畴
        
        Args:
            category_id: 范畴ID
            
        Returns:
            范畴属性，如果不存在则返回None
        """
        return self.categories.get(category_id)
        
    def get_relations(self, source_id: str) -> Dict[str, str]:
        """获取范畴关系
        
        Args:
            source_id: 源范畴ID
            
        Returns:
            关系字典
        """
        return self.relations.get(source_id, {})
        
    def to_sparse(self) -> sparse.csr_matrix:
        """转换为稀疏矩阵
        
        Returns:
            稀疏矩阵
        """
        return self.base.to_sparse()
        
    def from_sparse(self, sparse_matrix: sparse.csr_matrix) -> None:
        """从稀疏矩阵加载
        
        Args:
            sparse_matrix: 稀疏矩阵
        """
        self.base.from_sparse(sparse_matrix)
        self.advanced.from_sparse(sparse_matrix)
        
    def analyze(self) -> Dict[str, Any]:
        """分析研究范畴矩阵
        
        Returns:
            分析结果字典
        """
        return {
            'categories': len(self.categories),
            'relations': sum(len(relations) for relations in self.relations.values()),
            'shape': self.base.shape
        } 