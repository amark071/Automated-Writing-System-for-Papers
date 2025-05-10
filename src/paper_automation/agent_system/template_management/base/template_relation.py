from typing import Dict, List, Any
import logging
from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class TemplateRelation:
    """模板关系类，用于管理模板元素之间的关系"""
    relation_id: str
    source_id: str
    target_id: str
    relation_type: str
    relation_data: Dict[str, Any] = field(default_factory=dict)
    attributes: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """初始化后的验证"""
        self.logger = logging.getLogger(__name__)
        if not self.relation_id:
            raise ValueError("Relation ID cannot be empty")
        if not self.source_id:
            raise ValueError("Source ID cannot be empty")
        if not self.target_id:
            raise ValueError("Target ID cannot be empty")
        if not self.relation_type:
            raise ValueError("Relation type cannot be empty")
        if not isinstance(self.relation_data, dict):
            raise ValueError("Relation data must be a dictionary")
            
        # 初始化元数据
        if not self.metadata:
            self.metadata = {
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
    def add_attribute(self, key: str, value: Any) -> bool:
        """添加属性
        
        Args:
            key: 属性名
            value: 属性值
            
        Returns:
            bool: 是否添加成功
            
        Raises:
            ValueError: 当属性名为空或值为 None 时抛出
            KeyError: 当属性已存在时抛出
        """
        if not key:
            raise ValueError("Attribute key cannot be empty")
            
        if value is None:
            raise ValueError("Attribute value cannot be None")
            
        if key in self.attributes:
            raise KeyError(f"Attribute {key} already exists")
            
        self.attributes[key] = value
        self.metadata["updated_at"] = datetime.now().isoformat()
        self.logger.info(f"Added attribute {key} to relation {self.relation_id}")
        return True
            
    def update_attribute(self, key: str, value: Any) -> bool:
        """更新属性
        
        Args:
            key: 属性名
            value: 属性值
            
        Returns:
            bool: 是否更新成功
        """
        if not key:
            raise ValueError("Attribute key cannot be empty")
                
        if key not in self.attributes:
            raise KeyError(f"Attribute {key} does not exist")
                
        self.attributes[key] = value
        self.metadata["updated_at"] = datetime.now().isoformat()
        self.logger.info(f"Updated attribute {key} of relation {self.relation_id}")
        return True
            
    def get_attribute(self, key: str) -> Any:
        """获取属性
        
        Args:
            key: 属性名
            
        Returns:
            Any: 属性值
        """
        return self.attributes.get(key)
        
    def remove_attribute(self, key: str) -> bool:
        """删除属性
        
        Args:
            key: 属性名
            
        Returns:
            bool: 是否删除成功
        """
        if not key:
            raise ValueError("Attribute key cannot be empty")
                
        if key not in self.attributes:
            raise KeyError(f"Attribute {key} does not exist")
                
        del self.attributes[key]
        self.metadata["updated_at"] = datetime.now().isoformat()
        self.logger.info(f"Removed attribute {key} from relation {self.relation_id}")
        return True
            
    def validate(self) -> bool:
        """验证关系
        
        Returns:
            bool: 是否有效
            
        Raises:
            ValueError: 当关系ID、源ID、目标ID或关系类型为空时抛出
        """
        if not self.relation_id:
            raise ValueError("Relation ID cannot be empty")
            
        if not self.source_id:
            raise ValueError("Source ID cannot be empty")
            
        if not self.target_id:
            raise ValueError("Target ID cannot be empty")
            
        if not self.relation_type:
            raise ValueError("Relation type cannot be empty")
            
        if not isinstance(self.relation_data, dict):
            raise ValueError("Relation data must be a dictionary")
            
        return True
            
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "relation_id": self.relation_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation_type": self.relation_type,
            "relation_data": self.relation_data,
            "attributes": self.attributes,
            "metadata": self.metadata
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TemplateRelation':
        """从字典创建关系实例"""
        if not data:
            raise ValueError("Relation data cannot be empty")
            
        relation_id = data.get("relation_id")
        if not relation_id:
            raise ValueError("Relation ID cannot be empty")
            
        return cls(
            relation_id=relation_id,
            source_id=data.get("source_id", ""),
            target_id=data.get("target_id", ""),
            relation_type=data.get("relation_type", ""),
            relation_data=data.get("relation_data", {}),
            attributes=data.get("attributes", {}),
            metadata=data.get("metadata", {})
        ) 