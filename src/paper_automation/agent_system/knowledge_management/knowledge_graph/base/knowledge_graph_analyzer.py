"""知识图谱分析器模块"""

import networkx as nx
from typing import Dict, Any, List, Set, Optional
from collections import defaultdict, deque
import logging
from .builder import GraphBuilder

class KnowledgeGraphAnalyzer:
    """知识图谱分析器"""
    
    def __init__(self, builder: GraphBuilder):
        """初始化分析器
        
        Args:
            builder: 图构建器实例
        """
        self.builder = builder
        self.logger = logging.getLogger(__name__)
        
    def get_node_neighbors(self, node_id: str) -> List[str]:
        """获取节点的邻居节点
        
        Args:
            node_id: 节点ID
            
        Returns:
            List[str]: 邻居节点ID列表
            
        Raises:
            ValueError: 当节点不存在时抛出
        """
        if not any(node["id"] == node_id for node in self.builder.graph["nodes"]):
            raise ValueError(f"Node not found: {node_id}")
            
        neighbors = set()
        for edge in self.builder.graph["edges"]:
            if edge["source"] == node_id:
                neighbors.add(edge["target"])
            elif edge["target"] == node_id:
                neighbors.add(edge["source"])
        return list(neighbors)
        
    def get_node_degree(self, node_id: str) -> int:
        """获取节点的度
        
        Args:
            node_id: 节点ID
            
        Returns:
            int: 节点的度
            
        Raises:
            ValueError: 当节点不存在时抛出
        """
        if not any(node["id"] == node_id for node in self.builder.graph["nodes"]):
            raise ValueError(f"Node not found: {node_id}")
            
        degree = 0
        for edge in self.builder.graph["edges"]:
            if edge["source"] == node_id or edge["target"] == node_id:
                degree += 1
        return degree
        
    def find_path(self, source_id: str, target_id: str) -> List[str]:
        """查找两个节点之间的最短路径
        
        Args:
            source_id: 源节点ID
            target_id: 目标节点ID
            
        Returns:
            List[str]: 路径上的节点ID列表
            
        Raises:
            ValueError: 当找不到路径时抛出
        """
        if not any(node["id"] == source_id for node in self.builder.graph["nodes"]):
            raise ValueError(f"Source node not found: {source_id}")
            
        if not any(node["id"] == target_id for node in self.builder.graph["nodes"]):
            raise ValueError(f"Target node not found: {target_id}")
            
        # 使用BFS查找最短路径
        queue = deque([[source_id]])
        visited = {source_id}
        
        while queue:
            path = queue.popleft()
            node = path[-1]
            
            if node == target_id:
                return path
                
            for neighbor in self.get_node_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
                    
        raise ValueError(f"No path found between {source_id} and {target_id}")
        
    def get_connected_components(self) -> List[Set[str]]:
        """获取图的连通分量
        
        Returns:
            List[Set[str]]: 连通分量列表
        """
        G = nx.Graph()
        
        # 添加节点
        for node in self.builder.graph["nodes"]:
            G.add_node(node["id"])
            
        # 添加边
        for edge in self.builder.graph["edges"]:
            G.add_edge(edge["source"], edge["target"])
            
        # 获取连通分量
        components = list(nx.connected_components(G))
        return [set(component) for component in components]
        
    def get_centrality(self, node_id: str) -> float:
        """获取节点的中心性
        
        Args:
            node_id: 节点ID
            
        Returns:
            float: 节点的中心性值
            
        Raises:
            ValueError: 当节点不存在时抛出
        """
        if not any(node["id"] == node_id for node in self.builder.graph["nodes"]):
            raise ValueError(f"Node not found: {node_id}")
            
        node_count = len(self.builder.graph["nodes"])
        if node_count > 1:
            return self.get_node_degree(node_id) / (node_count - 1)
        return 0.0
        
    def get_clustering_coefficient(self, node_id: str) -> float:
        """获取节点的聚类系数
        
        Args:
            node_id: 节点ID
            
        Returns:
            float: 节点的聚类系数
            
        Raises:
            ValueError: 当节点不存在时抛出
        """
        if not any(node["id"] == node_id for node in self.builder.graph["nodes"]):
            raise ValueError(f"Node not found: {node_id}")
            
        neighbors = self.get_node_neighbors(node_id)
        if len(neighbors) < 2:
            return 0.0
            
        edge_count = 0
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                for edge in self.builder.graph["edges"]:
                    if (edge["source"] == neighbors[i] and edge["target"] == neighbors[j]) or \
                       (edge["source"] == neighbors[j] and edge["target"] == neighbors[i]):
                        edge_count += 1
                        break
                        
        max_edges = len(neighbors) * (len(neighbors) - 1) / 2
        if max_edges > 0:
            return edge_count / max_edges
        return 0.0
        
    def get_graph_density(self) -> float:
        """获取图的密度
        
        Returns:
            float: 图的密度
        """
        node_count = len(self.builder.graph["nodes"])
        if node_count < 2:
            return 0.0
            
        max_edges = node_count * (node_count - 1) / 2
        if max_edges > 0:
            return len(self.builder.graph["edges"]) / max_edges
        return 0.0
        
    def get_average_clustering(self) -> float:
        """获取图的平均聚类系数
        
        Returns:
            float: 图的平均聚类系数
        """
        node_ids = [node["id"] for node in self.builder.graph["nodes"]]
        if not node_ids:
            return 0.0
            
        coefficients = []
        for node_id in node_ids:
            try:
                coefficient = self.get_clustering_coefficient(node_id)
                coefficients.append(coefficient)
            except ValueError:
                continue
                
        if coefficients:
            return sum(coefficients) / len(coefficients)
        return 0.0
        
    def analyze_structure(self) -> Dict[str, Any]:
        """分析图的结构
        
        Returns:
            Dict[str, Any]: 结构分析结果
        """
        try:
            graph = self.builder.to_networkx(directed=True)
            
            node_count = len(self.builder.graph["nodes"])
            edge_count = len(self.builder.graph["edges"])
            density = self.get_graph_density()
            avg_clustering = self.get_average_clustering()
            components = len(self.get_connected_components())
            
            # 计算平均度
            if self.builder.graph["nodes"]:
                avg_degree = sum(self.get_node_degree(node["id"]) for node in self.builder.graph["nodes"]) / node_count
            else:
                avg_degree = 0.0
                
            return {
                "node_count": node_count,
                "edge_count": edge_count,
                "density": density,
                "avg_clustering": avg_clustering,
                "components": components,
                "avg_degree": avg_degree
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing graph structure: {str(e)}")
            return {}
            
    def analyze_connectivity(self) -> Dict[str, Any]:
        """分析图的连通性
        
        Returns:
            Dict[str, Any]: 连通性分析结果
        """
        try:
            graph = self.builder.to_networkx(directed=True)
            
            strongly_connected = list(nx.strongly_connected_components(graph))
            weakly_connected = list(nx.weakly_connected_components(graph))
            density = nx.density(graph)
            
            # 计算平均度
            if graph.number_of_nodes() > 0:
                average_degree = sum(dict(graph.degree()).values()) / graph.number_of_nodes()
            else:
                average_degree = 0
                
            return {
                "strongly_connected_components": strongly_connected,
                "weakly_connected_components": weakly_connected,
                "density": density,
                "average_degree": average_degree
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing graph connectivity: {str(e)}")
            return {}
            
    def analyze_centrality(self) -> Dict[str, Dict[str, float]]:
        """分析图的中心性
        
        Returns:
            Dict[str, Dict[str, float]]: 中心性分析结果
        """
        try:
            graph = self.builder.to_networkx(directed=True)
            
            degree_centrality = nx.degree_centrality(graph)
            in_degree_centrality = nx.in_degree_centrality(graph)
            out_degree_centrality = nx.out_degree_centrality(graph)
            betweenness_centrality = nx.betweenness_centrality(graph)
            closeness_centrality = nx.closeness_centrality(graph)
            eigenvector_centrality = nx.eigenvector_centrality(graph, max_iter=1000)
            
            return {
                "degree": degree_centrality,
                "in_degree": in_degree_centrality,
                "out_degree": out_degree_centrality,
                "betweenness": betweenness_centrality,
                "closeness": closeness_centrality,
                "eigenvector": eigenvector_centrality
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing graph centrality: {str(e)}")
            return {} 