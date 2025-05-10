"""关系图谱模块"""

from typing import Dict, List, Any, Optional, Set
from collections import deque
import uuid

class RelationGraph:
    """关系图谱类"""
    
    def __init__(self):
        """初始化关系图谱"""
        self.concepts: Dict[str, Dict[str, Any]] = {}
        self.relations: Dict[str, Dict[str, Any]] = {}
        self.valid_concept_types = {"subfield", "field", "technique"}
        self.valid_relation_types = {"uses", "implements", "includes", "related"}
    
    def add_concept(self, name: str, properties: Dict[str, Any]) -> str:
        """添加概念
        
        Args:
            name: 概念名称
            properties: 概念属性
            
        Returns:
            str: 概念ID
            
        Raises:
            ValueError: 概念类型无效或概念已存在
        """
        if "type" not in properties or properties["type"] not in self.valid_concept_types:
            raise ValueError(f"Invalid concept type: {properties.get('type')}")
            
        for concept in self.concepts.values():
            if concept["name"] == name:
                raise ValueError(f"Concept already exists: {name}")
                
        concept_id = str(uuid.uuid4())
        self.concepts[concept_id] = {
            "name": name,
            "properties": properties
        }
        return concept_id
    
    def add_relation(self, source_id: str, target_id: str, 
                    relation_type: str, properties: Dict[str, Any]) -> str:
        """添加关系
        
        Args:
            source_id: 源概念ID
            target_id: 目标概念ID
            relation_type: 关系类型
            properties: 关系属性
            
        Returns:
            str: 关系ID
            
        Raises:
            ValueError: 关系类型无效或概念不存在
        """
        if relation_type not in self.valid_relation_types:
            raise ValueError(f"Invalid relation type: {relation_type}")
            
        if source_id not in self.concepts:
            raise ValueError(f"Source concept not found: {source_id}")
            
        if target_id not in self.concepts:
            raise ValueError(f"Target concept not found: {target_id}")
            
        relation_id = str(uuid.uuid4())
        self.relations[relation_id] = {
            "source": source_id,
            "target": target_id,
            "type": relation_type,
            "properties": properties
        }
        return relation_id
    
    def get_concept(self, concept_id: str) -> Dict[str, Any]:
        """获取概念
        
        Args:
            concept_id: 概念ID
            
        Returns:
            Dict[str, Any]: 概念信息
            
        Raises:
            ValueError: 概念不存在
        """
        if concept_id not in self.concepts:
            raise ValueError(f"Concept not found: {concept_id}")
        return self.concepts[concept_id]
    
    def get_relation(self, relation_id: str) -> Dict[str, Any]:
        """获取关系
        
        Args:
            relation_id: 关系ID
            
        Returns:
            Dict[str, Any]: 关系信息
            
        Raises:
            ValueError: 关系不存在
        """
        if relation_id not in self.relations:
            raise ValueError(f"Relation not found: {relation_id}")
        return self.relations[relation_id]
    
    def get_related_concepts(self, concept_id: str) -> List[str]:
        """获取相关概念
        
        Args:
            concept_id: 概念ID
            
        Returns:
            List[str]: 相关概念ID列表
            
        Raises:
            ValueError: 概念不存在
        """
        if concept_id not in self.concepts:
            raise ValueError(f"Concept not found: {concept_id}")
            
        related_concepts = []
        for relation in self.relations.values():
            if relation["source"] == concept_id:
                related_concepts.append(relation["target"])
            elif relation["target"] == concept_id:
                related_concepts.append(relation["source"])
        return related_concepts
    
    def update_concept(self, concept_id: str, properties: Dict[str, Any]) -> None:
        """更新概念
        
        Args:
            concept_id: 概念ID
            properties: 概念属性
            
        Raises:
            ValueError: 概念不存在
        """
        if concept_id not in self.concepts:
            raise ValueError(f"Concept not found: {concept_id}")
        self.concepts[concept_id]["properties"].update(properties)
    
    def remove_concept(self, concept_id: str) -> None:
        """删除概念
        
        Args:
            concept_id: 概念ID
            
        Raises:
            ValueError: 概念不存在
        """
        if concept_id not in self.concepts:
            raise ValueError(f"Concept not found: {concept_id}")
            
        # 删除相关关系
        relations_to_remove = []
        for relation_id, relation in self.relations.items():
            if relation["source"] == concept_id or relation["target"] == concept_id:
                relations_to_remove.append(relation_id)
                
        for relation_id in relations_to_remove:
            del self.relations[relation_id]
            
        # 删除概念
        del self.concepts[concept_id]
    
    def get_concept_hierarchy(self, root_id: str) -> Dict[str, Any]:
        """获取概念层次结构
        
        Args:
            root_id: 根概念ID
            
        Returns:
            Dict[str, Any]: 层次结构信息
            
        Raises:
            ValueError: 概念不存在
        """
        if root_id not in self.concepts:
            raise ValueError(f"Concept not found: {root_id}")
            
        def build_hierarchy(concept_id: str, visited: Set[str]) -> Optional[Dict[str, Any]]:
            """构建层次结构
            
            Args:
                concept_id: 概念ID
                visited: 已访问的概念集合
                
            Returns:
                Optional[Dict[str, Any]]: 层次结构信息
            """
            if concept_id in visited:
                return None
                
            visited.add(concept_id)
            children = []
            
            # 查找子概念
            for relation in self.relations.values():
                if (relation["source"] == concept_id and 
                    relation["type"] == "includes"):
                    child_id = relation["target"]
                    child_hierarchy = build_hierarchy(child_id, visited)
                    if child_hierarchy:
                        children.append(child_hierarchy)
                        
            # 构建当前概念的层次结构
            concept = self.concepts[concept_id]
            hierarchy = {
                "id": concept_id,
                "name": concept["name"],
                "type": concept["properties"]["type"],
                "children": children
            }
            
            # 添加其他属性
            for key, value in concept["properties"].items():
                if key != "type":
                    hierarchy[key] = value
                    
            return hierarchy
            
        return build_hierarchy(root_id, set())
    
    def find_path(self, source_id: str, target_id: str) -> List[str]:
        """查找两个概念之间的路径
        
        Args:
            source_id: 源概念ID
            target_id: 目标概念ID
            
        Returns:
            List[str]: 路径上的概念ID列表
            
        Raises:
            ValueError: 概念不存在或路径不存在
        """
        if source_id not in self.concepts:
            raise ValueError(f"Source concept not found: {source_id}")
            
        if target_id not in self.concepts:
            raise ValueError(f"Target concept not found: {target_id}")
            
        # 使用广度优先搜索查找路径
        queue = deque([[source_id]])
        visited = {source_id}
        
        while queue:
            path = queue.popleft()
            node = path[-1]
            
            if node == target_id:
                return path
                
            for neighbor in self.get_related_concepts(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
                    
        raise ValueError(f"No path found between {source_id} and {target_id}") 