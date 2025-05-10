"""Knowledge Graph Builder Module
"""
import uuid
from typing import Dict, Any, Optional, List
import logging

class GraphBuilder:
    """图构建器"""
    
    def __init__(self):
        """初始化图构建器"""
        self.graph = {"nodes": [], "edges": []}
        self.nodes = {}  # 节点字典，用于快速查找
        self.edges = {}  # 边字典，用于快速查找
        self.valid_node_types = {"concept", "entity", "attribute"}
        self.valid_edge_types = {"includes", "uses", "related", "same_as", "subclass"}
        self.logger = logging.getLogger(__name__)
        
    def add_node(self, node: Dict[str, Any]) -> bool:
        """添加节点
        
        Args:
            node: 节点对象，包含 id、type 等属性
            
        Returns:
            bool: 是否添加成功
            
        Raises:
            ValueError: 当节点类型无效或缺少必要字段时
        """
        if not node:
            raise ValueError("节点不能为空")
            
        node_type = node.get("type")
        if node_type not in self.valid_node_types:
            raise ValueError(f"无效的节点类型: {node_type}")
            
        # 检查必要字段
        required_fields = ["id", "name"]
        for field in required_fields:
            if field not in node:
                raise ValueError(f"缺少必要字段: {field}")
                
        self.nodes[node["id"]] = node
        self.graph["nodes"].append(node)
        self.logger.info(f"添加节点: {node['id']}")
        return True
        
    def add_edge(self, edge: Dict[str, Any]) -> bool:
        """添加边
        
        Args:
            edge: 边对象，包含 source、target、type 等属性
            
        Returns:
            bool: 是否添加成功
            
        Raises:
            ValueError: 当边类型无效或节点不存在时
        """
        if not edge:
            raise ValueError("边不能为空")
            
        # 验证边类型
        if edge["type"] not in self.valid_edge_types:
            raise ValueError(f"无效的边类型: {edge['type']}")
            
        # 检查源节点和目标节点是否存在
        if edge["source"] not in self.nodes:
            raise ValueError(f"源节点不存在: {edge['source']}")
        if edge["target"] not in self.nodes:
            raise ValueError(f"目标节点不存在: {edge['target']}")
            
        # 生成边ID
        edge_id = str(uuid.uuid4())
        edge["id"] = edge_id
        
        self.edges[edge_id] = edge
        self.graph["edges"].append(edge)
        self.logger.info(f"添加边: {edge_id}")
        return True
        
    def build_graph(self, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, List]:
        """Build graph from nodes and edges
        
        Args:
            nodes: List of nodes
            edges: List of edges
            
        Returns:
            Dict[str, List]: Graph data
        """
        self.graph = {
            "nodes": nodes,
            "edges": edges
        }
        return self.graph
        
    def get_node(self, node_id: str) -> Dict[str, Any]:
        """Get node
        
        Args:
            node_id: Node ID
            
        Returns:
            Dict[str, Any]: Node data
            
        Raises:
            ValueError: When node does not exist
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node not found: {node_id}")
        return self.nodes[node_id]
        
    def get_edge(self, edge_id: str) -> Dict[str, Any]:
        """Get edge
        
        Args:
            edge_id: Edge ID
            
        Returns:
            Dict[str, Any]: Edge data
            
        Raises:
            ValueError: When edge does not exist
        """
        if edge_id not in self.edges:
            raise ValueError(f"Edge not found: {edge_id}")
        return self.edges[edge_id]
        
    def remove_node(self, node_id: str) -> None:
        """Remove node
        
        Args:
            node_id: Node ID
            
        Raises:
            ValueError: When node does not exist
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node not found: {node_id}")
            
        # Remove edges related to this node
        edges_to_remove = []
        for edge_id, edge in self.edges.items():
            if edge["source"] == node_id or edge["target"] == node_id:
                edges_to_remove.append(edge_id)
                
        for edge_id in edges_to_remove:
            del self.edges[edge_id]
            
        del self.nodes[node_id]
        
    def remove_edge(self, edge_id: str) -> None:
        """Remove edge
        
        Args:
            edge_id: Edge ID
            
        Raises:
            ValueError: When edge does not exist
        """
        if edge_id not in self.edges:
            raise ValueError(f"Edge not found: {edge_id}")
        del self.edges[edge_id]
        
    def update_node(self, node_id: str, properties: Dict[str, Any]) -> None:
        """Update node
        
        Args:
            node_id: Node ID
            properties: New node properties
            
        Raises:
            ValueError: When node does not exist
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node not found: {node_id}")
        self.nodes[node_id]["properties"].update(properties)
        
    def update_edge(self, edge_id: str, properties: Dict[str, Any]) -> None:
        """Update edge
        
        Args:
            edge_id: Edge ID
            properties: New edge properties
            
        Raises:
            ValueError: When edge does not exist
        """
        if edge_id not in self.edges:
            raise ValueError(f"Edge not found: {edge_id}")
        self.edges[edge_id]["properties"].update(properties) 