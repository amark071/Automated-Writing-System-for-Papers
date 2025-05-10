"""
知识谱系的实现
基于研究范畴矩阵和分类法
"""

from typing import Dict, List, Set, Tuple, Any, Optional
import numpy as np
from scipy import sparse
from ..research_category.category_matrix import ResearchCategoryMatrix
from .base_representation import KnowledgeSpectrumBaseRepresentation

class Taxonomy:
    """分类法类"""
    
    def __init__(self):
        self.nodes: Dict[str, Dict] = {}
        self.edges: Dict[str, Dict[str, str]] = {}
        
    def add_node(self, node_id: str, attributes: Dict) -> None:
        """添加节点"""
        if not node_id:
            raise ValueError("Node ID cannot be empty")
        if node_id in self.nodes:
            raise ValueError(f"Node {node_id} already exists")
        self.nodes[node_id] = attributes
        self.edges[node_id] = {}
        
    def add_edge(self, source_id: str, target_id: str, edge_type: str) -> None:
        """添加边"""
        if not source_id or not target_id or not edge_type:
            raise ValueError("Source ID, target ID and edge type cannot be empty")
        if source_id not in self.nodes:
            raise ValueError(f"Source node {source_id} not found")
        if target_id not in self.nodes:
            raise ValueError(f"Target node {target_id} not found")
        self.edges[source_id][target_id] = edge_type
        
    def remove_edge(self, source_id: str, target_id: str) -> None:
        """移除边"""
        if source_id in self.edges and target_id in self.edges[source_id]:
            del self.edges[source_id][target_id]
            
    def get_node(self, node_id: str) -> Dict:
        """获取节点"""
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")
        return self.nodes[node_id]
        
    def get_children(self, node_id: str) -> Dict[str, str]:
        """获取子节点"""
        if node_id not in self.edges:
            return {}
        return self.edges[node_id]
        
    def get_relations(self, node_id: str, edge_type: Optional[str] = None) -> Dict[str, str]:
        """获取关系"""
        if node_id not in self.edges:
            return {}
        if edge_type is None:
            return self.edges[node_id]
        return {target: type_ for target, type_ in self.edges[node_id].items() if type_ == edge_type}
        
    def remove_node(self, node_id: str) -> None:
        """移除节点"""
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")
        del self.nodes[node_id]
        del self.edges[node_id]
        for edges in self.edges.values():
            if node_id in edges:
                del edges[node_id]
                
    def update_node(self, node_id: str, attributes: Dict) -> None:
        """更新节点"""
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")
        self.nodes[node_id].update(attributes)

class KnowledgeSpectrumAdvancedRepresentation(KnowledgeSpectrumBaseRepresentation):
    """知识谱系高级表示类"""
    
    def __init__(self, dimensions: List[int]):
        """初始化
        
        Args:
            dimensions: 维度列表
        """
        super().__init__(dimensions)
        self.taxonomy = Taxonomy()
        self.features: Dict[str, np.ndarray] = {}
        self.relations: Dict[str, Dict[str, str]] = {}
        
    def add_feature(self, feature_id: str, feature_data: np.ndarray) -> None:
        """添加特征
        
        Args:
            feature_id: 特征ID
            feature_data: 特征数据
        """
        if not feature_id:
            raise ValueError("Feature ID cannot be empty")
        if feature_id in self.features:
            raise ValueError(f"Feature {feature_id} already exists")
        if feature_data.shape != self.shape:
            raise ValueError(f"Feature data shape {feature_data.shape} does not match spectrum shape {self.shape}")
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
        
    def remove_feature(self, feature_id: str) -> None:
        """移除特征
        
        Args:
            feature_id: 特征ID
        """
        if feature_id not in self.features:
            raise ValueError(f"Feature {feature_id} not found")
        del self.features[feature_id]
        
    def remove_relation(self, source_id: str, target_id: str) -> None:
        """移除关系
        
        Args:
            source_id: 源ID
            target_id: 目标ID
        """
        if source_id in self.relations and target_id in self.relations[source_id]:
            del self.relations[source_id][target_id]
            if not self.relations[source_id]:
                del self.relations[source_id]
                
    def get_feature(self, feature_id: str) -> np.ndarray:
        """获取特征
        
        Args:
            feature_id: 特征ID
            
        Returns:
            特征数据
        """
        if feature_id not in self.features:
            raise ValueError(f"Feature {feature_id} not found")
        return self.features[feature_id]
        
    def get_relations(self, source_id: str, relation_type: Optional[str] = None) -> Dict[str, str]:
        """获取关系
        
        Args:
            source_id: 源ID
            relation_type: 关系类型
            
        Returns:
            关系字典
        """
        if source_id not in self.relations:
            return {}
        if relation_type is None:
            return self.relations[source_id]
        return {target: type_ for target, type_ in self.relations[source_id].items() if type_ == relation_type}
        
    def update_feature(self, feature_id: str, feature_data: np.ndarray) -> None:
        """更新特征
        
        Args:
            feature_id: 特征ID
            feature_data: 特征数据
        """
        if feature_id not in self.features:
            raise ValueError(f"Feature {feature_id} not found")
        if feature_data.shape != self.shape:
            raise ValueError(f"Feature data shape {feature_data.shape} does not match spectrum shape {self.shape}")
        self.features[feature_id] = feature_data
        
    def update_relation(self, source_id: str, target_id: str, relation_type: str) -> None:
        """更新关系
        
        Args:
            source_id: 源ID
            target_id: 目标ID
            relation_type: 关系类型
        """
        if source_id not in self.relations or target_id not in self.relations[source_id]:
            raise ValueError(f"Relation from {source_id} to {target_id} not found")
        self.relations[source_id][target_id] = relation_type
        
    def add_taxonomy_node(self, node_id: str, attributes: Dict) -> None:
        """添加分类法节点
        
        Args:
            node_id: 节点ID
            attributes: 节点属性
        """
        self.taxonomy.add_node(node_id, attributes)
        
    def add_taxonomy_edge(self, source_id: str, target_id: str, edge_type: str) -> None:
        """添加分类法边
        
        Args:
            source_id: 源节点ID
            target_id: 目标节点ID
            edge_type: 边类型
        """
        self.taxonomy.add_edge(source_id, target_id, edge_type)
        
    def remove_taxonomy_edge(self, source_id: str, target_id: str) -> None:
        """移除分类法边
        
        Args:
            source_id: 源节点ID
            target_id: 目标节点ID
        """
        self.taxonomy.remove_edge(source_id, target_id)
        
    def get_taxonomy_node(self, node_id: str) -> Dict:
        """获取分类法节点
        
        Args:
            node_id: 节点ID
            
        Returns:
            节点属性
        """
        return self.taxonomy.get_node(node_id)
        
    def get_taxonomy_children(self, node_id: str) -> Dict[str, str]:
        """获取分类法子节点
        
        Args:
            node_id: 节点ID
            
        Returns:
            子节点字典
        """
        return self.taxonomy.get_children(node_id)
        
    def get_taxonomy_relations(self, node_id: str, edge_type: Optional[str] = None) -> Dict[str, str]:
        """获取分类法关系
        
        Args:
            node_id: 节点ID
            edge_type: 边类型
            
        Returns:
            关系字典
        """
        return self.taxonomy.get_relations(node_id, edge_type)
        
    def remove_taxonomy_node(self, node_id: str) -> None:
        """移除分类法节点
        
        Args:
            node_id: 节点ID
        """
        self.taxonomy.remove_node(node_id)
        
    def update_taxonomy_node(self, node_id: str, attributes: Dict) -> None:
        """更新分类法节点
        
        Args:
            node_id: 节点ID
            attributes: 节点属性
        """
        self.taxonomy.update_node(node_id, attributes)
        
    def get_taxonomy_edges(self, node_id: str) -> Dict[str, str]:
        """获取分类法边
        
        Args:
            node_id: 节点ID
            
        Returns:
            边字典
        """
        return self.taxonomy.get_relations(node_id)
        
    def analyze(self) -> Dict[str, Any]:
        """分析谱系
        
        Returns:
            分析结果
        """
        return {
            'nodes': len(self.taxonomy.nodes),
            'edges': sum(len(edges) for edges in self.taxonomy.edges.values()),
            'features': len(self.features),
            'relations': sum(len(relations) for relations in self.relations.values()),
            'shape': self.shape
        }

class KnowledgeSpectrum:
    """知识谱系类"""
    
    def __init__(self, name: str):
        """初始化知识谱系"""
        self.name = name
        self.research_matrix = ResearchCategoryMatrix()
        self.taxonomies: Dict[str, Taxonomy] = {}  # 分类法集合
        self.spectrum_matrix: np.ndarray = None  # 谱系矩阵
        self.mappings: Dict[str, Dict[str, str]] = {}  # 分类法之间的映射关系
        self.integrated_hierarchy: Dict[str, Any] = {}  # 整合后的层次结构
        self.matrix = None  # 用于张量积计算的矩阵
        self.nodes = []  # 用于存储节点列表
        
        # 初始化一个简单的矩阵和节点列表
        self._initialize_default_matrix()
        
    def _initialize_default_matrix(self):
        """初始化默认矩阵"""
        # 创建一些默认节点
        self.nodes = ['Node1', 'Node2', 'Node3']
        size = len(self.nodes)
        
        # 创建一个对角矩阵，并添加一些非零元素
        self.matrix = np.eye(size)
        # 在对角线上方添加一些非零元素
        for i in range(size-1):
            self.matrix[i, i+1] = 1.0
        
        # 转换为稀疏矩阵格式
    def add_taxonomy(self, taxonomy: Taxonomy) -> None:
        """添加分类法"""
        self.taxonomies[taxonomy.name] = taxonomy
        
    def add_mapping(self, source_taxonomy: str, target_taxonomy: str, 
                   source_node: str, target_node: str, confidence: float = 1.0) -> None:
        """添加分类法之间的映射关系
        
        Args:
            source_taxonomy: 源分类法名称
            target_taxonomy: 目标分类法名称
            source_node: 源节点ID
            target_node: 目标节点ID
            confidence: 映射置信度
        """
        if source_taxonomy not in self.mappings:
            self.mappings[source_taxonomy] = {}
        if target_taxonomy not in self.mappings[source_taxonomy]:
            self.mappings[source_taxonomy][target_taxonomy] = []
            
        self.mappings[source_taxonomy][target_taxonomy].append({
            'source_node': source_node,
            'target_node': target_node,
            'confidence': confidence
        })
        
    def integrate_taxonomies(self):
        """集成多个分类体系"""
        if not self.taxonomies:
            return None
        
        # 初始化集成结构
        self.integrated_hierarchy = {
            'nodes': {},
            'mappings': {},
            'root_nodes': set(),
            'levels': {}
        }
        
        # 收集所有节点和关系
        for taxonomy in self.taxonomies.values():
            for node_id in taxonomy.nodes:
                if node_id not in self.integrated_hierarchy['nodes']:
                    self.integrated_hierarchy['nodes'][node_id] = {
                        'attributes': taxonomy.nodes[node_id]['attributes'],
                        'children': set(taxonomy.nodes[node_id]['children']),
                        'relations': {}
                    }
                
                # 添加子节点
                self.integrated_hierarchy['nodes'][node_id]['children'].update(taxonomy.nodes[node_id]['children'])
                
                # 添加关系
                if node_id in taxonomy.relations:
                    for relation in taxonomy.relations[node_id]:
                        relation_type = relation['type']
                        target_id = relation['target']
                        
                        if relation_type not in self.integrated_hierarchy['nodes'][node_id]['relations']:
                            self.integrated_hierarchy['nodes'][node_id]['relations'][relation_type] = set()
                        self.integrated_hierarchy['nodes'][node_id]['relations'][relation_type].add(target_id)
                        
                        # 确保目标节点存在
                        if target_id not in self.integrated_hierarchy['nodes']:
                            self.integrated_hierarchy['nodes'][target_id] = {
                                'attributes': taxonomy.nodes[target_id]['attributes'],
                                'children': set(taxonomy.nodes[target_id]['children']),
                                'relations': {}
                            }
        
        # 解决循环依赖
        cycles = self._find_cycles(self.integrated_hierarchy)
        for cycle in cycles:
            self._resolve_cycle(self.integrated_hierarchy, cycle)
        
        # 找出根节点
        self.integrated_hierarchy['root_nodes'] = {
            node_id for node_id in self.integrated_hierarchy['nodes']
            if not any(node_id in node_info['children'] 
                      for node_info in self.integrated_hierarchy['nodes'].values())
        }
        
        # 计算层级
        visited = set()
        def calculate_level(node_id, level=0):
            if node_id in visited:
                return
            visited.add(node_id)
            self.integrated_hierarchy['levels'][node_id] = level
            children = self.integrated_hierarchy['nodes'][node_id]['children']
            for child in children:
                calculate_level(child, level + 1)
        
        for root in self.integrated_hierarchy['root_nodes']:
            calculate_level(root)
        
        return self.integrated_hierarchy
        
    def _generate_integrated_hierarchy(self, hierarchies: Dict[str, Dict], mapping_graph: Dict) -> Dict:
        """生成整合后的层次结构"""
        integrated = {
            'nodes': {},
            'mappings': mapping_graph,
            'root_nodes': set(),
            'levels': {}
        }
        
        # 收集所有节点
        all_nodes = set()
        for name, hierarchy in hierarchies.items():
            # 添加父节点
            all_nodes.update(hierarchy.keys())
            # 添加子节点
            for node_id, children in hierarchy.items():
                if isinstance(children, dict):
                    all_nodes.update(children.keys())
                    
            # 添加所有节点
            taxonomy = self.taxonomies[name]
            all_nodes.update(taxonomy.nodes.keys())
            for children in taxonomy.nodes.values():
                all_nodes.update(children)
        
        # 添加映射关系中的节点
        for source_name, target_mappings in mapping_graph.items():
            for target_name, node_mappings in target_mappings.items():
                for source_id, mappings in node_mappings.items():
                    all_nodes.add(source_id)
                    for mapping in mappings:
                        all_nodes.add(mapping['target'])
        
        # 初始化所有节点
        for node_id in all_nodes:
            integrated['nodes'][node_id] = {
                'id': node_id,
                'attributes': {},
                'children': set(),
                'relations': []
            }
        
        # 添加节点属性和关系
        for name, hierarchy in hierarchies.items():
            taxonomy = self.taxonomies[name]
            # 添加所有节点的子节点关系
            for node_id, children in hierarchy.items():
                if isinstance(children, dict):
                    for child_id, child_hierarchy in children.items():
                        if child_id in integrated['nodes']:
                            integrated['nodes'][node_id]['children'].add(child_id)
                    
            # 添加所有节点的属性
            for node_id, attrs in taxonomy.nodes[node_id]['attributes'].items():
                if node_id in integrated['nodes']:
                    integrated['nodes'][node_id]['attributes'].update(attrs)
                    
            # 添加所有节点的关系
            for node_id, relations in taxonomy.relations.items():
                if node_id in integrated['nodes']:
                    integrated['nodes'][node_id]['relations'].extend(relations)
        
        # 更新根节点和层次深度
        for hierarchy in hierarchies.values():
            integrated['root_nodes'].update(hierarchy.keys())
            for node_id, level in hierarchy.items():
                if node_id in integrated['nodes']:
                    if node_id not in integrated['levels']:
                        integrated['levels'][node_id] = level
                    else:
                        integrated['levels'][node_id] = min(
                            integrated['levels'][node_id], level
                        )
        
        return integrated
        
    def _build_mapping_graph(self, hierarchies: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """构建映射图"""
        mapping_graph = {}
        
        # 初始化映射图
        for source_name in self.taxonomies:
            mapping_graph[source_name] = {}
            for target_name in self.taxonomies:
                if source_name != target_name:
                    mapping_graph[source_name][target_name] = {}
        
        # 添加直接映射
        for source_name, target_mappings in self.mappings.items():
            for target_name, mappings in target_mappings.items():
                for mapping in mappings:
                    source_id = mapping['source_node']
                    target_id = mapping['target_node']
                    confidence = mapping['confidence']
                    
                    if source_id not in mapping_graph[source_name][target_name]:
                        mapping_graph[source_name][target_name][source_id] = []
                    mapping_graph[source_name][target_name][source_id].append({
                        'target': target_id,
                        'confidence': confidence
                    })
                    
                    # 添加反向映射
                    if target_id not in mapping_graph[target_name][source_name]:
                        mapping_graph[target_name][source_name][target_id] = []
                    mapping_graph[target_name][source_name][target_id].append({
                        'target': source_id,
                        'confidence': confidence
                    })
                    
        # 添加间接映射
        self._add_indirect_mappings(mapping_graph, hierarchies)
        
        return mapping_graph
        
    def _add_indirect_mappings(self, mapping_graph: Dict[str, Dict[str, List[Dict[str, Any]]]],
                                   hierarchies: Dict[str, Dict[str, Any]]) -> None:
        """添加间接映射"""
        taxonomies = list(mapping_graph.keys())
        
        for source_name in taxonomies:
            for target_name in taxonomies:
                if source_name != target_name:
                    # 通过其他分类法建立间接映射
                    for intermediate in taxonomies:
                        if intermediate != source_name and intermediate != target_name:
                            self._add_indirect_mapping_through(
                                mapping_graph, source_name, intermediate, target_name, hierarchies
                            )
                            
    def _add_indirect_mapping_through(self, mapping_graph: Dict[str, Dict[str, List[Dict[str, Any]]]],
                                   source: str, intermediate: str, target: str,
                                   hierarchies: Dict[str, Dict[str, Any]]) -> None:
        """通过中间分类法添加间接映射"""
        for source_node, source_mappings in mapping_graph[source][intermediate].items():
            for source_mapping in source_mappings:
                intermediate_node = source_mapping['target']
                if intermediate_node in mapping_graph[intermediate][target]:
                    for target_mapping in mapping_graph[intermediate][target][intermediate_node]:
                        target_node = target_mapping['target']
                        # 计算间接映射的置信度（取两个直接映射置信度的乘积）
                        confidence = source_mapping['confidence'] * target_mapping['confidence']
                        
                        if source_node not in mapping_graph[source][target]:
                            mapping_graph[source][target][source_node] = []
                        mapping_graph[source][target][source_node].append({
                            'target': target_node,
                            'confidence': confidence,
                            'path': [intermediate]
                        })
                        
    def _resolve_conflicts(self, integrated: Dict[str, Any]) -> None:
        """处理整合过程中的冲突和歧义"""
        # 1. 处理重复节点
        duplicate_nodes = self._find_duplicate_nodes(integrated)
        for node_id, duplicates in duplicate_nodes.items():
            self._merge_duplicate_nodes(integrated, node_id, duplicates)
            
        # 2. 处理循环依赖
        cycles = self._find_cycles(integrated)
        for cycle in cycles:
            self._resolve_cycle(integrated, cycle)
            
        # 3. 确保所有节点都被正确处理
        for node_id in list(integrated['nodes'].keys()):
            if node_id not in integrated['nodes']:
                continue
                
            node_info = integrated['nodes'][node_id]
            
            # 确保子节点集合是有效的
            valid_children = set()
            for child_id in node_info['children']:
                if child_id in integrated['nodes']:
                    valid_children.add(child_id)
            node_info['children'] = valid_children
            
            # 确保关系列表是有效的
            valid_relations = []
            for relation in node_info['relations']:
                if relation['target'] in integrated['nodes']:
                    valid_relations.append(relation)
            node_info['relations'] = valid_relations
            
        # 4. 再次检查循环依赖
        cycles = self._find_cycles(integrated)
        for cycle in cycles:
            self._resolve_cycle(integrated, cycle)
        
    def _find_duplicate_nodes(self, integrated: Dict[str, Any]) -> Dict[str, List[str]]:
        """查找重复节点"""
        duplicates = {}
        node_attributes = {}
        
        for node_id, node_info in integrated['nodes'].items():
            attr_key = tuple(sorted(node_info['attributes'].items()))
            if attr_key not in node_attributes:
                node_attributes[attr_key] = []
            node_attributes[attr_key].append(node_id)
            
        for attr_key, node_ids in node_attributes.items():
            if len(node_ids) > 1:
                duplicates[node_ids[0]] = node_ids[1:]
                
        return duplicates
        
    def _merge_duplicate_nodes(self, integrated: Dict[str, Any],
                            primary_id: str, duplicate_ids: List[str]) -> None:
        """合并重复节点"""
        primary_node = integrated['nodes'][primary_id]
        
        for duplicate_id in duplicate_ids:
            duplicate_node = integrated['nodes'][duplicate_id]
            
            # 合并属性
            for attr_name, attr_value in duplicate_node['attributes'].items():
                if attr_name not in primary_node['attributes']:
                    primary_node['attributes'][attr_name] = attr_value
                    
            # 更新子节点关系
            for child_id in duplicate_node['children']:
                primary_node['children'].add(child_id)
                
            # 更新映射关系
            for source_name, target_mappings in integrated['mappings'].items():
                for target_name, node_mappings in target_mappings.items():
                    for node_id, mappings in node_mappings.items():
                        for mapping in mappings:
                            if mapping['target'] == duplicate_id:
                                mapping['target'] = primary_id
                                
            # 删除重复节点
            del integrated['nodes'][duplicate_id]
            
    def _find_cycles(self, integrated: Dict[str, Any]) -> List[List[str]]:
        """查找循环依赖"""
        cycles = []
        visited = set()
        path = []
        
        def dfs(node_id: str) -> None:
            if node_id in path:
                cycle_start = path.index(node_id)
                cycles.append(path[cycle_start:])
                return
                
            if node_id in visited:
                return
                
            visited.add(node_id)
            path.append(node_id)
            
            if node_id in integrated['nodes']:
                for child_id in integrated['nodes'][node_id]['children']:
                    if child_id in integrated['nodes']:
                        dfs(child_id)
                
            path.pop()
            
        # 从每个节点开始搜索
        for node_id in integrated['nodes']:
            if node_id not in visited:
                dfs(node_id)
                
        return cycles
        
    def _resolve_cycle(self, integrated: Dict[str, Any], cycle: List[str]) -> None:
        """解决循环依赖"""
        # 选择置信度最低的边断开
        min_confidence = float('inf')
        edge_to_remove = None
        
        for i in range(len(cycle)):
            source_id = cycle[i]
            target_id = cycle[(i + 1) % len(cycle)]
            
            # 查找映射关系中的置信度
            for source_name, target_mappings in integrated['mappings'].items():
                for target_name, node_mappings in target_mappings.items():
                    if source_id in node_mappings:
                        for mapping in node_mappings[source_id]:
                            if mapping['target'] == target_id:
                                if mapping['confidence'] < min_confidence:
                                    min_confidence = mapping['confidence']
                                    edge_to_remove = (source_id, target_id)
                                    
        if edge_to_remove:
            source_id, target_id = edge_to_remove
            if source_id in integrated['nodes'] and target_id in integrated['nodes']:
                # 断开双向关系
                integrated['nodes'][source_id]['children'].discard(target_id)
                integrated['nodes'][target_id]['children'].discard(source_id)
                
                # 更新映射关系
                for source_name, target_mappings in integrated['mappings'].items():
                    for target_name, node_mappings in target_mappings.items():
                        if source_id in node_mappings:
                            node_mappings[source_id] = [
                                m for m in node_mappings[source_id]
                                if m['target'] != target_id
                            ]
                        if target_id in node_mappings:
                            node_mappings[target_id] = [
                                m for m in node_mappings[target_id]
                                if m['target'] != source_id
                            ]
        
    def get_integrated_hierarchy(self) -> Dict[str, Any]:
        """获取整合后的层次结构"""
        if not self.integrated_hierarchy:
            self.integrate_taxonomies()
        return self.integrated_hierarchy

    def generate_spectrum(self) -> np.ndarray:
        """生成谱系矩阵"""
        # 1. 检查层次结构是否为空
        if not self.integrated_hierarchy or not self.integrated_hierarchy['nodes']:
            # 创建一个1x1的空矩阵
            self.spectrum_matrix = sparse.csr_matrix((1, 1), dtype=np.float64)
            return np.zeros((1, 1))
            
        # 2. 获取所有节点ID
        node_ids = list(self.integrated_hierarchy['nodes'].keys())
        n_nodes = len(node_ids)
        
        # 3. 创建基础谱系矩阵
        spectrum = np.zeros((n_nodes, n_nodes), dtype=np.float64)
        
        # 4. 构建节点索引映射
        node_to_idx = {node_id: idx for idx, node_id in enumerate(node_ids)}
        
        # 5. 基于层次结构填充基础谱系矩阵
        for node_id, node_info in self.integrated_hierarchy['nodes'].items():
            node_idx = node_to_idx[node_id]
            
            # 5.1 设置自相关
            spectrum[node_idx, node_idx] = 1.0
            
            # 5.2 设置父子关系
            for child_id in node_info.get('children', []):
                if child_id in node_to_idx:
                    child_idx = node_to_idx[child_id]
                    spectrum[node_idx, child_idx] = 0.8  # 父子关系权重
                    spectrum[child_idx, node_idx] = 0.8
                    
        # 6. 应用映射关系
        mappings = self.integrated_hierarchy.get('mappings', {})
        for source_name, target_mappings in mappings.items():
            for target_name, node_mappings in target_mappings.items():
                for source_node, mappings in node_mappings.items():
                    if source_node in node_to_idx:
                        source_idx = node_to_idx[source_node]
                        for mapping in mappings:
                            target_node = mapping['target']
                            if target_node in node_to_idx:
                                target_idx = node_to_idx[target_node]
                                confidence = mapping['confidence']
                                
                                # 更新映射关系
                                spectrum[source_idx, target_idx] = max(
                                    spectrum[source_idx, target_idx],
                                    confidence
                                )
                                spectrum[target_idx, source_idx] = max(
                                    spectrum[target_idx, source_idx],
                                    confidence
                                )
                                
        # 7. 矩阵归一化
        spectrum = self._normalize_matrix(spectrum)
        
        # 8. 保存谱系矩阵
        self.spectrum_matrix = sparse.csr_matrix(spectrum, dtype=np.float64)
        
        return spectrum
        
    def _find_spectrum_nodes(self, research_node: str) -> List[str]:
        """查找研究节点对应的谱系节点"""
        spectrum_nodes = []
        
        for node_id, node_info in self.integrated_hierarchy['nodes'].items():
            # 检查节点属性中是否包含研究节点信息
            if 'research_nodes' in node_info['attributes']:
                research_nodes = node_info['attributes']['research_nodes']
                if isinstance(research_nodes, str):
                    research_nodes = [research_nodes]
                if research_node in research_nodes:
                    spectrum_nodes.append(node_id)
                    
        return spectrum_nodes
        
    def _normalize_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """矩阵归一化"""
        # 计算每行的最大值
        row_max = np.max(matrix, axis=1, keepdims=True)
        # 避免除以零
        row_max[row_max == 0] = 1
        # 归一化
        return matrix / row_max
        
    def get_spectrum_matrix(self) -> np.ndarray:
        """获取谱系矩阵"""
        if self.spectrum_matrix is None:
            self.generate_spectrum()
        return self.spectrum_matrix

    def analyze_spectrum(self):
        """分析谱系矩阵并返回相关指标"""
        if not hasattr(self, 'spectrum_matrix') or self.spectrum_matrix is None:
            self.generate_spectrum()
        
        if self.spectrum_matrix is None:
            return None
        
        n = len(self.spectrum_matrix)
        if n == 0:
            return None
        
        # 计算基本指标
        total_edges = np.sum(self.spectrum_matrix > 0.5)  # 只计算显著的关系
        max_edges = n * (n - 1)  # 有向图中可能的最大边数
        density = total_edges / max_edges if max_edges > 0 else 0
        
        # 获取层次结构
        hierarchy = self.get_integrated_hierarchy()
        
        # 计算层级数
        max_depth = max(hierarchy['levels'].values()) if hierarchy['levels'] else 0
        
        # 计算模块度
        communities = self._detect_communities(self.spectrum_matrix)
        modularity = self._calculate_modularity_fast(self.spectrum_matrix, communities)
        
        return {
            'density': float(density),
            'modularity': float(modularity),
            'hierarchy_levels': max_depth,
            'community_structure': float(len(set(communities)))
        }

    def _detect_communities(self, spectrum: np.ndarray) -> List[int]:
        """检测社区结构"""
        n_nodes = spectrum.shape[0]
        if n_nodes <= 2:
            return [0] * n_nodes
        
        # 将谱系矩阵转换为邻接矩阵
        adj = (spectrum > 0.5).astype(float)
        if np.sum(adj) == 0:
            return [0] * n_nodes
        
        # 使用深度优先搜索检测社区
        communities = [-1] * n_nodes
        current_community = 0
        
        def dfs(node: int) -> None:
            communities[node] = current_community
            for neighbor in range(n_nodes):
                if adj[node, neighbor] > 0 and communities[neighbor] == -1:
                    dfs(neighbor)
        
        for node in range(n_nodes):
            if communities[node] == -1:
                dfs(node)
                current_community += 1
            
        return communities

    def _calculate_modularity_fast(self, spectrum: np.ndarray, communities: List[int]) -> float:
        """快速计算模块度"""
        n_nodes = spectrum.shape[0]
        if n_nodes < 2:
            return 0.0

        adj = (spectrum > 0.5).astype(float)
        m = np.sum(adj) / 2
        if m == 0:
            return 0.0

        k = np.sum(adj, axis=1)
        communities = np.array(communities)
        
        modularity = 0.0
        for community in set(communities):
            nodes = (communities == community)
            k_in = np.sum(adj[nodes][:, nodes])
            k_total = np.sum(k[nodes])
            modularity += k_in / (2 * m) - (k_total / (2 * m)) ** 2
        
        return float(modularity)

    def verify_relation_completeness(self) -> float:
        """验证关系完整性
        
        Returns:
            float: 关系完整性得分，范围[0,1]
        """
        if not self.integrated_hierarchy:
            return 0.0
            
        total_nodes = len(self.integrated_hierarchy['nodes'])
        if total_nodes == 0:
            return 0.0
            
        # 检查节点关系的完整性
        relation_count = 0
        for node_id, node_info in self.integrated_hierarchy['nodes'].items():
            # 检查子节点关系
            relation_count += len(node_info['children'])
            
            # 检查其他类型的关系
            if 'relations' in node_info:
                for relation_type, targets in node_info['relations'].items():
                    relation_count += len(targets)
                    
        # 计算完整性得分
        # 理想情况下，每个节点至少应该有一个关系
        completeness = min(1.0, relation_count / (total_nodes * 2))  # 使用2作为每个节点的理想关系数
        
        return completeness

    def check_relation_consistency(self) -> float:
        """检查关系一致性
        
        Returns:
            float: 关系一致性得分，范围[0,1]
        """
        if not self.integrated_hierarchy:
            return 0.0
            
        total_nodes = len(self.integrated_hierarchy['nodes'])
        if total_nodes == 0:
            return 0.0
            
        # 检查节点关系的一致性
        consistent_relations = 0
        total_relations = 0
        
        for node_id, node_info in self.integrated_hierarchy['nodes'].items():
            # 检查子节点关系的一致性
            for child_id in node_info['children']:
                total_relations += 1
                if child_id in self.integrated_hierarchy['nodes']:
                    consistent_relations += 1
                    
            # 检查其他类型关系的一致性
            if 'relations' in node_info:
                for relation_type, targets in node_info['relations'].items():
                    for target_id in targets:
                        total_relations += 1
                        if target_id in self.integrated_hierarchy['nodes']:
                            consistent_relations += 1
                            
        # 计算一致性得分
        consistency = consistent_relations / max(1, total_relations)
        
        return consistency 