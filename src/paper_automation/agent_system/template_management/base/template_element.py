"""模板元素模块
"""
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime

@dataclass
class TemplateElement:
    """模板元素类"""
    
    element_id: str
    element_type: str
    content: Dict[str, Any]
    attributes: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """初始化后的验证"""
        self.logger = logging.getLogger(__name__)
        
        if not self.element_id:
            raise ValueError("Element ID cannot be empty")
            
        if not self.element_type:
            raise ValueError("Element type cannot be empty")
            
        if not isinstance(self.content, dict):
            raise ValueError("Content must be a dictionary")
            
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
            ValueError: 当属性名为空或值为 None 时
            KeyError: 当属性已存在时
        """
        if not key or not isinstance(key, str):
            raise ValueError("Attribute key cannot be empty")
            
        if value is None:
            raise ValueError("Attribute value cannot be None")
            
        if key in self.attributes:
            raise KeyError(f"Attribute {key} already exists")
            
        self.attributes[key] = value
        self.metadata["updated_at"] = datetime.now().isoformat()
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
        return True
            
    def get_attribute(self, key: str) -> Optional[Any]:
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
        return True
            
    def validate(self) -> bool:
        """验证元素
        
        Returns:
            bool: 是否有效
        """
        try:
            if not self.element_id:
                raise ValueError("Element ID cannot be empty")
                
            if not self.element_type:
                raise ValueError("Element type cannot be empty")
                
            if not isinstance(self.content, dict):
                raise ValueError("Content must be a dictionary")
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating element: {str(e)}")
            return False
            
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "element_id": self.element_id,
            "element_type": self.element_type,
            "content": self.content,
            "attributes": self.attributes,
            "metadata": self.metadata
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TemplateElement':
        """从字典创建元素
        
        Args:
            data: 元素数据
            
        Returns:
            TemplateElement: 模板元素实例
        """
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
            
        element_id = data.get("element_id")
        if not element_id:
            raise ValueError("Element ID cannot be empty")
            
        element_type = data.get("element_type")
        if not element_type:
            raise ValueError("Element type cannot be empty")
            
        content = data.get("content", {})
        if not isinstance(content, dict):
            raise ValueError("Content must be a dictionary")
            
        return cls(
            element_id=element_id,
            element_type=element_type,
            content=content,
            attributes=data.get("attributes", {}),
            metadata=data.get("metadata", {})
        ) 