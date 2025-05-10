"""特征图谱模块
"""
from typing import Dict, List, Any, Optional, Tuple
import uuid

class FeatureGraph:
    """特征图谱类"""
    
    def __init__(self):
        """初始化"""
        self.features = {}  # 特征字典
        self.relations = {}  # 关系字典
        self.valid_feature_types = {"metric", "property", "attribute"}
        self.valid_relation_types = {"trade_off", "correlation", "dependency"}
        
    def add_feature(self, name: str, properties: Dict[str, Any]) -> str:
        """添加特征
        
        Args:
            name: 特征名称
            properties: 特征属性
            
        Returns:
            str: 特征ID
            
        Raises:
            ValueError: 当特征类型无效或特征已存在时
        """
        if "type" not in properties or properties["type"] not in self.valid_feature_types:
            raise ValueError(f"Invalid feature type: {properties.get('type')}")
            
        # 检查是否存在同名特征
        for feature in self.features.values():
            if feature["name"] == name:
                raise ValueError(f"Feature already exists: {name}")
                
        feature_id = str(uuid.uuid4())
        self.features[feature_id] = {
            "name": name,
            "properties": properties
        }
        return feature_id
        
    def add_feature_relation(self, source_id: str, target_id: str,
                           relation_type: str, properties: Dict[str, Any]) -> str:
        """添加特征关系
        
        Args:
            source_id: 源特征ID
            target_id: 目标特征ID
            relation_type: 关系类型
            properties: 关系属性
            
        Returns:
            str: 关系ID
            
        Raises:
            ValueError: 当关系类型无效或特征不存在时
        """
        if relation_type not in self.valid_relation_types:
            raise ValueError(f"Invalid relation type: {relation_type}")
            
        if source_id not in self.features:
            raise ValueError(f"Source feature not found: {source_id}")
            
        if target_id not in self.features:
            raise ValueError(f"Target feature not found: {target_id}")
            
        relation_id = str(uuid.uuid4())
        self.relations[relation_id] = {
            "source": source_id,
            "target": target_id,
            "type": relation_type,
            "properties": properties
        }
        return relation_id
        
    def get_feature(self, feature_id: str) -> Dict[str, Any]:
        """获取特征
        
        Args:
            feature_id: 特征ID
            
        Returns:
            Dict[str, Any]: 特征数据
            
        Raises:
            ValueError: 当特征不存在时
        """
        if feature_id not in self.features:
            raise ValueError(f"Feature not found: {feature_id}")
        return self.features[feature_id]
        
    def get_feature_relation(self, relation_id: str) -> Dict[str, Any]:
        """获取特征关系
        
        Args:
            relation_id: 关系ID
            
        Returns:
            Dict[str, Any]: 关系数据
            
        Raises:
            ValueError: 当关系不存在时
        """
        if relation_id not in self.relations:
            raise ValueError(f"Relation not found: {relation_id}")
        return self.relations[relation_id]
        
    def get_related_features(self, feature_id: str) -> List[str]:
        """获取相关特征
        
        Args:
            feature_id: 特征ID
            
        Returns:
            List[str]: 相关特征ID列表
            
        Raises:
            ValueError: 当特征不存在时
        """
        if feature_id not in self.features:
            raise ValueError(f"Feature not found: {feature_id}")
            
        related_features = []
        for relation in self.relations.values():
            if relation["source"] == feature_id:
                related_features.append(relation["target"])
            elif relation["target"] == feature_id:
                related_features.append(relation["source"])
        return related_features
        
    def update_feature(self, feature_id: str, properties: Dict[str, Any]) -> None:
        """更新特征
        
        Args:
            feature_id: 特征ID
            properties: 新的特征属性
            
        Raises:
            ValueError: 当特征不存在时
        """
        if feature_id not in self.features:
            raise ValueError(f"Feature not found: {feature_id}")
        self.features[feature_id]["properties"].update(properties)
        
    def remove_feature(self, feature_id: str) -> None:
        """删除特征
        
        Args:
            feature_id: 特征ID
            
        Raises:
            ValueError: 当特征不存在时
        """
        if feature_id not in self.features:
            raise ValueError(f"Feature not found: {feature_id}")
            
        # 删除与该特征相关的关系
        relations_to_remove = []
        for relation_id, relation in self.relations.items():
            if relation["source"] == feature_id or relation["target"] == feature_id:
                relations_to_remove.append(relation_id)
                
        for relation_id in relations_to_remove:
            del self.relations[relation_id]
            
        del self.features[feature_id]
        
    def get_feature_statistics(self) -> Dict[str, Any]:
        """获取特征统计信息
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        # 统计特征总数
        total_features = len(self.features)
        
        # 统计特征类型分布
        feature_types = {}
        for feature in self.features.values():
            feature_type = feature["properties"]["type"]
            feature_types[feature_type] = feature_types.get(feature_type, 0) + 1
            
        # 统计特征值范围
        value_ranges = {}
        for feature in self.features.values():
            if "value" in feature["properties"]:
                feature_type = feature["properties"]["type"]
                value = feature["properties"]["value"]
                if feature_type not in value_ranges:
                    value_ranges[feature_type] = {"min": value, "max": value}
                else:
                    value_ranges[feature_type]["min"] = min(value_ranges[feature_type]["min"], value)
                    value_ranges[feature_type]["max"] = max(value_ranges[feature_type]["max"], value)
                    
        return {
            "total_features": total_features,
            "feature_types": feature_types,
            "value_ranges": value_ranges
        }
        
    def analyze_feature_correlations(self) -> Dict[Tuple[str, str], float]:
        """分析特征相关性
        
        Returns:
            Dict[Tuple[str, str], float]: 特征对之间的相关性得分
        """
        correlations = {}
        
        # 遍历所有特征对
        feature_ids = list(self.features.keys())
        for i in range(len(feature_ids)):
            for j in range(i + 1, len(feature_ids)):
                source_id = feature_ids[i]
                target_id = feature_ids[j]
                
                # 检查是否存在相关性关系
                for relation in self.relations.values():
                    if (relation["source"] == source_id and relation["target"] == target_id) or \
                       (relation["source"] == target_id and relation["target"] == source_id):
                        if relation["type"] == "correlation":
                            # 获取相关性强度
                            strength = relation["properties"].get("strength", 0)
                            correlations[(source_id, target_id)] = strength
                            break
                            
        return correlations 