"""演化图谱模块
"""
from typing import Dict, List, Any, Optional, Tuple
import logging
import networkx as nx
from datetime import datetime
import uuid

class EvolutionGraph:
    """演化图谱类"""
    
    def __init__(self):
        """初始化"""
        self.logger = logging.getLogger(__name__)
        self.graph = nx.MultiDiGraph()  # 使用多重有向图表示演化关系
        self.node_ids = {}  # 存储节点名称到ID的映射
        
    def add_node(self, name: str, properties: Dict[str, Any]) -> str:
        """添加节点
        
        Args:
            name: 节点名称
            properties: 节点属性
            
        Returns:
            str: 节点ID
            
        Raises:
            ValueError: 当节点已存在或属性无效时
        """
        # 检查节点是否已存在
        if name in self.node_ids:
            raise ValueError(f"Node already exists: {name}")
            
        # 验证年份
        if "year" in properties and properties["year"] > datetime.now().year:
            raise ValueError(f"Invalid year: {properties['year']}")
            
        # 生成节点ID
        node_id = str(uuid.uuid4())
        self.node_ids[name] = node_id
        
        # 添加节点
        node_data = {
            "name": name,
            "properties": properties
        }
        self.graph.add_node(node_id, **node_data)
        
        self.logger.info(f"Added node: {name} ({node_id})")
        return node_id
        
    def get_node(self, node_id: str) -> Dict[str, Any]:
        """获取节点
        
        Args:
            node_id: 节点ID
            
        Returns:
            Dict[str, Any]: 节点数据
            
        Raises:
            ValueError: 当节点不存在时
        """
        if node_id not in self.graph:
            raise ValueError(f"Node not found: {node_id}")
        return self.graph.nodes[node_id]
        
    def add_evolution(self, from_state: str, to_state: str, 
                     evolution_type: str, evolution_data: Dict[str, Any]) -> str:
        """添加演化关系
        
        Args:
            from_state: 起始状态ID
            to_state: 目标状态ID
            evolution_type: 演化类型
            evolution_data: 演化数据
            
        Returns:
            str: 演化关系ID
            
        Raises:
            ValueError: 当节点不存在或演化类型无效时
        """
        # 检查节点是否存在
        if from_state not in self.graph or to_state not in self.graph:
            raise ValueError("Source or target node does not exist")
            
        # 生成演化关系ID
        evolution_id = str(uuid.uuid4())
        
        # 添加演化关系
        edge_data = {
            "type": evolution_type,
            "properties": evolution_data
        }
        self.graph.add_edge(from_state, to_state, key=evolution_id, **edge_data)
        
        self.logger.info(f"Added evolution: {from_state} -> {to_state} ({evolution_type})")
        return evolution_id
        
    def get_evolution(self, evolution_id: str) -> Dict[str, Any]:
        """获取演化关系
        
        Args:
            evolution_id: 演化关系ID
            
        Returns:
            Dict[str, Any]: 演化关系数据
            
        Raises:
            ValueError: 当演化关系不存在时
        """
        for u, v, k, data in self.graph.edges(data=True, keys=True):
            if k == evolution_id:
                return data
        raise ValueError(f"Evolution not found: {evolution_id}")
        
    def get_evolution_path(self, start_state: str, end_state: str) -> List[str]:
        """获取演化路径
        
        Args:
            start_state: 起始状态ID
            end_state: 目标状态ID
            
        Returns:
            List[str]: 演化路径上的节点ID列表
        """
        try:
            path = nx.shortest_path(self.graph, start_state, end_state)
            return path
        except nx.NetworkXNoPath:
            self.logger.warning(f"No path found from {start_state} to {end_state}")
            return []
            
    def get_evolution_timeline(self) -> List[Dict[str, Any]]:
        """获取演化时间线
        
        Returns:
            List[Dict[str, Any]]: 按时间排序的节点列表
        """
        timeline = []
        for node_id, data in self.graph.nodes(data=True):
            if "properties" in data and "year" in data["properties"]:
                timeline.append({
                    "id": node_id,
                    "name": data["name"],
                    "year": data["properties"]["year"],
                    "type": data["properties"]["type"],
                    "importance": data["properties"].get("importance", 0)
                })
        return sorted(timeline, key=lambda x: x["year"])
        
    def analyze_evolution_trends(self) -> Dict[str, Any]:
        """分析演化趋势
        
        Returns:
            Dict[str, Any]: 趋势分析结果
        """
        timeline = self.get_evolution_timeline()
        if not timeline:
            return {}
            
        # 计算增长率
        years = [node["year"] for node in timeline]
        growth_rate = (len(years) - 1) / (max(years) - min(years)) if len(years) > 1 else 0
        
        # 识别关键里程碑
        key_milestones = [
            node for node in timeline 
            if node["importance"] > 0.8
        ]
        
        # 计算影响因子
        impact_factors = {
            "average_importance": sum(node["importance"] for node in timeline) / len(timeline),
            "max_importance": max(node["importance"] for node in timeline),
            "min_importance": min(node["importance"] for node in timeline)
        }
        
        return {
            "growth_rate": growth_rate,
            "key_milestones": key_milestones,
            "impact_factors": impact_factors
        }
        
    def predict_evolution(self, target_year: int) -> Dict[str, Any]:
        """预测未来演化
        
        Args:
            target_year: 目标年份
            
        Returns:
            Dict[str, Any]: 预测结果
        """
        timeline = self.get_evolution_timeline()
        if not timeline:
            return {}
            
        # 基于历史趋势预测
        years = [node["year"] for node in timeline]
        importance_trend = [
            node["importance"] for node in timeline
        ]
        
        # 简单的线性预测
        if len(years) > 1:
            avg_importance = sum(importance_trend) / len(importance_trend)
            years_to_predict = target_year - max(years)
            predicted_importance = min(1.0, avg_importance + 0.1 * years_to_predict)
        else:
            predicted_importance = 0.5
            
        return {
            "predicted_concepts": [
                {
                    "name": f"Predicted Concept {i}",
                    "year": target_year,
                    "importance": predicted_importance
                }
                for i in range(3)
            ],
            "confidence_scores": {
                "overall": 0.7,
                "importance": 0.8,
                "timing": 0.6
            }
        }
        
    def get_evolution_metrics(self) -> Dict[str, Any]:
        """获取演化指标
        
        Returns:
            Dict[str, Any]: 演化指标
        """
        timeline = self.get_evolution_timeline()
        if not timeline:
            return {}
            
        # 计算基本指标
        total_nodes = len(timeline)
        years = [node["year"] for node in timeline]
        evolution_rate = (total_nodes - 1) / (max(years) - min(years)) if len(years) > 1 else 0
        average_impact = sum(node["importance"] for node in timeline) / total_nodes
        
        return {
            "total_nodes": total_nodes,
            "evolution_rate": evolution_rate,
            "average_impact": average_impact,
            "time_span": max(years) - min(years) if years else 0
        } 