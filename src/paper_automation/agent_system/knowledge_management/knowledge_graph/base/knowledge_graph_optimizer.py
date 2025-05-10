"""Knowledge Graph Optimizer Module"""

import networkx as nx
from typing import Dict, Any, List, Set
import logging

class KnowledgeGraphOptimizer:
    """知识图谱优化器"""
    
    def __init__(self, builder, analyzer):
        """初始化优化器
        
        Args:
            builder: 图构建器实例
            analyzer: 图分析器实例
        """
        self.builder = builder
        self.analyzer = analyzer
        self.logger = logging.getLogger(__name__)
        
    def _are_nodes_similar(self, node1: Dict[str, Any], node2: Dict[str, Any]) -> bool:
        """判断两个节点是否相似
        
        Args:
            node1: 第一个节点
            node2: 第二个节点
            
        Returns:
            bool: 是否相似
        """
        # 检查节点类型
        if node1["type"] != node2["type"]:
            return False
            
        # 检查节点名称
        name1 = node1.get("name", "")
        name2 = node2.get("name", "")
        if name1 and name2 and name1 == name2:
            return True
            
        # 检查节点属性
        name1 = node1["properties"].get("name", "")
        name2 = node2["properties"].get("name", "")
        if name1 and name2 and name1 == name2:
            return True
            
        return False
        
    def merge_duplicate_nodes(self, node_ids: List[str]) -> str:
        """合并重复节点
        
        Args:
            node_ids: 要合并的节点ID列表
            
        Returns:
            str: 合并后的基础节点ID
        """
        if not node_ids:
            return ""
            
        # 选择重要性最高的节点作为基础节点
        base_node = max(
            [self.builder.get_node(node_id) for node_id in node_ids],
            key=lambda x: x["properties"].get("importance", 0)
        )
        base_node_id = base_node["id"]
        
        # 合并其他节点的属性
        for node_id in node_ids:
            if node_id == base_node_id:
                continue
                
            node = self.builder.get_node(node_id)
            for key, value in node["properties"].items():
                if key not in base_node["properties"]:
                    base_node["properties"][key] = value
                    
        # 更新边的连接
        for node_id in node_ids:
            if node_id == base_node_id:
                continue
                
            # 获取与当前节点相连的边
            edges_to_update = []
            for edge in self.builder.graph["edges"]:
                if edge["source"] == node_id:
                    edges_to_update.append((edge, "source"))
                elif edge["target"] == node_id:
                    edges_to_update.append((edge, "target"))
                    
            # 更新边的连接
            for edge, direction in edges_to_update:
                if direction == "source":
                    edge["source"] = base_node_id
                else:
                    edge["target"] = base_node_id
                    
            # 删除原节点
            self.builder.remove_node(node_id)
            
        return base_node_id
        
    def prune_weak_connections(self, threshold: float = 0.3) -> List[Dict[str, Any]]:
        """剪枝弱连接
        
        Args:
            threshold: 权重阈值
            
        Returns:
            List[Dict[str, Any]]: 被删除的边列表
        """
        removed_edges = []
        edges_to_remove = []
        
        for edge in self.builder.graph["edges"]:
            weight = edge["properties"].get("weight", 0)
            if weight < threshold:
                edges_to_remove.append(edge)
                
        for edge in edges_to_remove:
            self.builder.graph["edges"].remove(edge)
            removed_edges.append(edge)
            
        return removed_edges
        
    def optimize(self) -> Dict[str, Any]:
        """优化知识图谱
        
        Returns:
            Dict[str, Any]: 优化结果
        """
        try:
            # 合并重复节点
            merged_nodes = []
            nodes_to_merge = {}
            
            for node1 in self.builder.graph["nodes"]:
                if node1["id"] in nodes_to_merge:
                    continue
                    
                similar_nodes = []
                for node2 in self.builder.graph["nodes"]:
                    if node2["id"] in nodes_to_merge:
                        continue
                        
                    if self._are_nodes_similar(node1, node2):
                        similar_nodes.append(node2["id"])
                        nodes_to_merge[node2["id"]] = True
                        
                if len(similar_nodes) > 1:
                    base_node_id = self.merge_duplicate_nodes(similar_nodes)
                    merged_nodes.extend([node_id for node_id in similar_nodes if node_id != base_node_id])
                    
            self.logger.info(f"After merging nodes: {[(node['id'], node['name']) for node in self.builder.graph['nodes']]}")
            self.logger.info(f"After merging edges: {[(edge['source'], edge['target'], edge['type'], edge['properties'].get('weight', 0)) for edge in self.builder.graph['edges']]}")
            
            # 删除冗余边
            removed_edges = []
            node_pairs = {}
            
            # 按节点对分组边
            for edge in self.builder.graph["edges"]:
                pair = (edge["source"], edge["target"])
                node_pairs.setdefault(pair, []).append(edge)
                
            # 处理每组边
            for pair, edges in node_pairs.items():
                if len(edges) <= 1:
                    continue
                    
                # 按边类型分组
                type_groups = {}
                for edge in edges:
                    edge_type = edge["type"]
                    type_groups.setdefault(edge_type, []).append(edge)
                    
                # 处理每种类型的边
                for edge_type, type_edges in type_groups.items():
                    if len(type_edges) <= 1:
                        continue
                        
                    # 选择权重最大的边
                    best_edge = max(type_edges, key=lambda x: x["properties"].get("weight", 0))
                    
                    # 删除其他边
                    for edge in type_edges:
                        if edge != best_edge:
                            self.builder.graph["edges"].remove(edge)
                            removed_edges.append(edge)
                            
            self.logger.info(f"After removing redundant edges: {[(edge['source'], edge['target'], edge['type'], edge['properties'].get('weight', 0)) for edge in self.builder.graph['edges']]}")
            
            # 剪枝弱连接
            pruned_edges = self.prune_weak_connections(0.3)
            removed_edges.extend(pruned_edges)
            
            self.logger.info(f"After pruning weak connections: {[(edge['source'], edge['target'], edge['type'], edge['properties'].get('weight', 0)) for edge in self.builder.graph['edges']]}")
            
            # 删除传递边
            edges_to_remove = []
            for edge1 in self.builder.graph["edges"]:
                for edge2 in self.builder.graph["edges"]:
                    if edge1 != edge2 and edge1["source"] == edge2["source"]:
                        for edge3 in self.builder.graph["edges"]:
                            if edge3["source"] == edge2["target"] and edge3["target"] == edge1["target"]:
                                edges = [edge1, edge2, edge3]
                                edges.sort(key=lambda x: x["properties"].get("weight", 0))
                                edges_to_remove.append(edges[0])
                                
            for edge in edges_to_remove:
                if edge in self.builder.graph["edges"]:
                    self.builder.graph["edges"].remove(edge)
                    removed_edges.append(edge)
                    
            self.logger.info(f"After removing transitive edges: {[(edge['source'], edge['target'], edge['type'], edge['properties'].get('weight', 0)) for edge in self.builder.graph['edges']]}")
            
            # 删除孤立节点
            isolated_nodes = []
            for node in self.builder.graph["nodes"]:
                if not any(edge["source"] == node["id"] or edge["target"] == node["id"] for edge in self.builder.graph["edges"]):
                    self.builder.graph["nodes"].remove(node)
                    isolated_nodes.append(node["id"])
                    
            self.logger.info(f"After removing isolated nodes: {[(node['id'], node['name']) for node in self.builder.graph['nodes']]}")
            self.logger.info(f"Final edges: {[(edge['source'], edge['target'], edge['type'], edge['properties'].get('weight', 0)) for edge in self.builder.graph['edges']]}")
            
            return {
                "merged_nodes": merged_nodes,
                "removed_edges": removed_edges,
                "updated_weights": [],
                "isolated_nodes": isolated_nodes
            }
            
        except Exception as e:
            self.logger.error(f"Error optimizing graph: {str(e)}")
            return {}
            
    def validate_optimization(self) -> Dict[str, Any]:
        """验证优化结果
        
        Returns:
            Dict[str, Any]: 验证结果
        """
        # 检查图的连通性
        components = self.analyzer.get_connected_components()
        is_connected = len(components) == 1
        
        # 计算图密度和平均聚类系数
        density = self.analyzer.get_graph_density()
        avg_clustering = self.analyzer.get_average_clustering()
        
        # 计算优化得分
        score = (density * 0.4 + avg_clustering * 0.6) * (1.0 if is_connected else 0.8)
        
        # 验证优化结果
        is_valid = is_connected and density > 0.1 and avg_clustering > 0.2
        
        return {
            "is_valid": is_valid,
            "density": density,
            "avg_clustering": avg_clustering,
            "score": score
        } 