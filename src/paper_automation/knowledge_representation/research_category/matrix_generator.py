"""研究范畴矩阵生成器模块"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from scipy import sparse
from .base_representation import ResearchCategoryBaseRepresentation
from .advanced_representation import ResearchCategoryAdvancedRepresentation

class ResearchCategoryMatrixGenerator:
    """研究范畴矩阵生成器类"""
    
    def __init__(self):
        """初始化矩阵生成器"""
        self.dimensions = []  # 维度配置
        self.features = {}    # 特征配置
        self.relations = {}   # 关系配置
        
    def set_dimensions(self, dimensions: List[int]) -> None:
        """设置维度配置
        
        Args:
            dimensions: 维度列表
            
        Raises:
            ValueError: 如果维度列表为空或包含非正数
        """
        if not dimensions:
            raise ValueError('维度列表不能为空')
            
        if any(d <= 0 for d in dimensions):
            raise ValueError('维度必须为正数')
            
        self.dimensions = dimensions
        
    def add_feature_config(self, feature_id: str, feature_type: str, feature_params: Dict) -> None:
        """添加特征配置
        
        Args:
            feature_id: 特征ID
            feature_type: 特征类型
            feature_params: 特征参数
            
        Raises:
            ValueError: 如果特征ID或类型为空
        """
        if not feature_id or not feature_type:
            raise ValueError('特征ID和类型不能为空')
            
        self.features[feature_id] = {
            'type': feature_type,
            'params': feature_params
        }
        
    def add_relation_config(self, source_id: str, target_id: str, relation_type: str, relation_params: Dict) -> None:
        """添加关系配置
        
        Args:
            source_id: 源ID
            target_id: 目标ID
            relation_type: 关系类型
            relation_params: 关系参数
            
        Raises:
            ValueError: 如果源ID、目标ID或关系类型为空
        """
        if not source_id or not target_id or not relation_type:
            raise ValueError('源ID、目标ID和关系类型不能为空')
            
        if source_id not in self.relations:
            self.relations[source_id] = {}
            
        self.relations[source_id][target_id] = {
            'type': relation_type,
            'params': relation_params
        }
        
    def generate_base_matrix(self) -> ResearchCategoryBaseRepresentation:
        """生成基础矩阵
        
        Returns:
            基础研究范畴矩阵
            
        Raises:
            ValueError: 如果维度未配置
        """
        if not self.dimensions:
            raise ValueError('请先配置维度')
            
        return ResearchCategoryBaseRepresentation(self.dimensions)
        
    def generate_advanced_matrix(self) -> ResearchCategoryAdvancedRepresentation:
        """生成高级矩阵
        
        Returns:
            高级研究范畴矩阵
            
        Raises:
            ValueError: 如果维度未配置
        """
        if not self.dimensions:
            raise ValueError('请先配置维度')
            
        matrix = ResearchCategoryAdvancedRepresentation(self.dimensions)
        
        # 添加特征
        for feature_id, feature_config in self.features.items():
            feature_data = self._generate_feature_data(feature_config)
            matrix.add_feature(feature_id, feature_data)
            
        # 添加关系
        for source_id, target_relations in self.relations.items():
            for target_id, relation_config in target_relations.items():
                matrix.add_relation(source_id, target_id, relation_config['type'])
                
        return matrix
        
    def _generate_feature_data(self, feature_config: Dict) -> np.ndarray:
        """生成特征数据
        
        Args:
            feature_config: 特征配置
            
        Returns:
            特征数据矩阵
            
        Raises:
            ValueError: 如果特征类型不支持
        """
        feature_type = feature_config['type']
        params = feature_config['params']
        
        if feature_type == 'random':
            return np.random.random(self.dimensions)
        elif feature_type == 'uniform':
            return np.ones(self.dimensions)
        elif feature_type == 'gaussian':
            mean = params.get('mean', 0)
            std = params.get('std', 1)
            return np.random.normal(mean, std, self.dimensions)
        else:
            raise ValueError(f'不支持的特征类型: {feature_type}')
            
    def clear_config(self) -> None:
        """清除所有配置"""
        self.dimensions = []
        self.features = {}
        self.relations = {} 