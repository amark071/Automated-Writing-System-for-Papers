"""知识谱系模块"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from scipy import sparse
from .advanced_representation import KnowledgeSpectrumAdvancedRepresentation

class KnowledgeSpectrum:
    """知识谱系类"""
    
    def __init__(self):
        """初始化知识谱系"""
        self.spectrum = KnowledgeSpectrumAdvancedRepresentation([1, 1])
        self.research_matrix = None
        self.classification_systems = {}
        self.mapping_relations = {}
        self.hierarchy_levels = {}
        
    def integrate_research_matrix(self, matrix: np.ndarray) -> None:
        """集成研究矩阵
        
        Args:
            matrix: 研究矩阵
            
        Raises:
            ValueError: 如果矩阵不是numpy数组
        """
        if not isinstance(matrix, np.ndarray):
            raise ValueError('研究矩阵必须是numpy数组')
            
        self.research_matrix = matrix.copy()
        
    def add_classification_system(self, system_id: str, system_info: Dict) -> None:
        """添加分类系统
        
        Args:
            system_id: 系统ID
            system_info: 系统信息
            
        Raises:
            ValueError: 如果系统ID已存在
        """
        if system_id in self.classification_systems:
            raise ValueError(f'分类系统 {system_id} 已存在')
            
        self.classification_systems[system_id] = system_info
        
    def remove_classification_system(self, system_id: str) -> None:
        """移除分类系统
        
        Args:
            system_id: 系统ID
            
        Raises:
            ValueError: 如果系统不存在
        """
        if system_id not in self.classification_systems:
            raise ValueError(f'分类系统 {system_id} 不存在')
            
        del self.classification_systems[system_id]
        
    def add_mapping_relation(self, source_system: str, target_system: str,
                           source_node: str, target_node: str, confidence: float = 1.0) -> None:
        """添加映射关系
        
        Args:
            source_system: 源系统ID
            target_system: 目标系统ID
            source_node: 源节点ID
            target_node: 目标节点ID
            confidence: 置信度
            
        Raises:
            ValueError: 如果系统不存在
        """
        if source_system not in self.classification_systems:
            raise ValueError(f'源系统 {source_system} 不存在')
            
        if target_system not in self.classification_systems:
            raise ValueError(f'目标系统 {target_system} 不存在')
            
        if source_system not in self.mapping_relations:
            self.mapping_relations[source_system] = {}
            
        if target_system not in self.mapping_relations[source_system]:
            self.mapping_relations[source_system][target_system] = {}
            
        if source_node not in self.mapping_relations[source_system][target_system]:
            self.mapping_relations[source_system][target_system][source_node] = []
            
        self.mapping_relations[source_system][target_system][source_node].append({
            'target': target_node,
            'confidence': confidence
        })
        
    def remove_mapping_relation(self, source_system: str, target_system: str,
                              source_node: str, target_node: str) -> None:
        """移除映射关系
        
        Args:
            source_system: 源系统ID
            target_system: 目标系统ID
            source_node: 源节点ID
            target_node: 目标节点ID
            
        Raises:
            ValueError: 如果关系不存在
        """
        if (source_system not in self.mapping_relations or
            target_system not in self.mapping_relations[source_system] or
            source_node not in self.mapping_relations[source_system][target_system]):
            raise ValueError('映射关系不存在')
            
        mappings = self.mapping_relations[source_system][target_system][source_node]
        for i, mapping in enumerate(mappings):
            if mapping['target'] == target_node:
                del mappings[i]
                break
                
        if not mappings:
            del self.mapping_relations[source_system][target_system][source_node]
            
    def set_hierarchy_level(self, node_id: str, level: int) -> None:
        """设置层次级别
        
        Args:
            node_id: 节点ID
            level: 级别
            
        Raises:
            ValueError: 如果级别为负数
        """
        if level < 0:
            raise ValueError('级别不能为负数')
            
        self.hierarchy_levels[node_id] = level
        
    def get_hierarchy_level(self, node_id: str) -> Optional[int]:
        """获取层次级别
        
        Args:
            node_id: 节点ID
            
        Returns:
            级别，如果不存在则返回None
        """
        return self.hierarchy_levels.get(node_id)
        
    def generate_spectrum_matrix(self) -> np.ndarray:
        """生成谱系矩阵
        
        Returns:
            谱系矩阵
        """
        # 清空现有谱系
        self.spectrum = KnowledgeSpectrumAdvancedRepresentation([1, 1])
        
        # 添加分类系统节点
        for system_id, system_info in self.classification_systems.items():
            self.spectrum.add_node(system_id, {
                'type': 'classification_system',
                'info': system_info
            })
            
        # 添加映射关系
        for source_system, target_systems in self.mapping_relations.items():
            for target_system, node_mappings in target_systems.items():
                for source_node, mappings in node_mappings.items():
                    for mapping in mappings:
                        self.spectrum.add_relation(
                            source_system,
                            target_system,
                            'mapping',
                            mapping['confidence']
                        )
                        
        # 设置层次级别
        for node_id, level in self.hierarchy_levels.items():
            node_info = self.spectrum.get_node(node_id)
            if node_info:
                node_info['level'] = level
                
        # 生成谱系矩阵
        return self.spectrum.generate_spectrum()
        
    def find_node(self, node_id: str) -> Optional[Dict]:
        """查找节点
        
        Args:
            node_id: 节点ID
            
        Returns:
            节点信息，如果不存在则返回None
        """
        return self.spectrum.get_node(node_id)
        
    def normalize_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """归一化矩阵
        
        Args:
            matrix: 输入矩阵
            
        Returns:
            归一化后的矩阵
        """
        return self.spectrum._normalize_matrix(matrix)
        
    def get_spectrum_analysis(self) -> Dict[str, float]:
        """获取谱系分析结果
        
        Returns:
            分析结果字典
        """
        return self.spectrum.analyze_spectrum()
        
    def verify_completeness(self) -> float:
        """验证完整性
        
        Returns:
            完整性得分
        """
        return self.spectrum.verify_relation_completeness()
        
    def check_consistency(self) -> float:
        """检查一致性
        
        Returns:
            一致性得分
        """
        return self.spectrum.check_relation_consistency() 