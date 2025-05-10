"""知识映射接口模块
"""
from typing import Dict, Any
import logging

class MappingInterface:
    """知识映射接口类"""
    
    def __init__(self):
        """初始化知识映射接口"""
        self.logger = logging.getLogger(__name__)
        self.mappings: Dict[str, Dict[str, Any]] = {}
        
    def create_mapping(self, mapping_name: str, source: Dict[str, Any], target: Dict[str, Any]) -> Dict[str, Any]:
        """创建知识映射
        
        Args:
            mapping_name: 映射名称
            source: 源对象
            target: 目标对象
            
        Returns:
            Dict[str, Any]: 创建的映射
            
        Raises:
            ValueError: 当映射名称已存在或参数无效时抛出
        """
        # 验证参数
        if not mapping_name:
            raise ValueError("映射名称不能为空")
            
        if mapping_name in self.mappings:
            raise ValueError(f"映射 {mapping_name} 已存在")
            
        required_fields = ["id", "type"]
        for field in required_fields:
            if field not in source or not source[field]:
                raise ValueError(f"源对象缺少必要字段: {field}")
            if field not in target or not target[field]:
                raise ValueError(f"目标对象缺少必要字段: {field}")
                
        # 创建映射
        mapping = {
            "name": mapping_name,
            "source": source,
            "target": target
        }
        self.mappings[mapping_name] = mapping
        self.logger.info(f"创建映射 {mapping_name}")
        return mapping
        
    def get_mapping(self, mapping_name: str) -> Dict[str, Any]:
        """获取知识映射
        
        Args:
            mapping_name: 映射名称
            
        Returns:
            Dict[str, Any]: 获取的映射
            
        Raises:
            ValueError: 当映射不存在时抛出
        """
        if mapping_name not in self.mappings:
            raise ValueError(f"映射 {mapping_name} 不存在")
            
        return self.mappings[mapping_name]
        
    def update_mapping(self, mapping_name: str, source: Dict[str, Any], target: Dict[str, Any]) -> Dict[str, Any]:
        """更新知识映射
        
        Args:
            mapping_name: 映射名称
            source: 新的源对象
            target: 新的目标对象
            
        Returns:
            Dict[str, Any]: 更新后的映射
            
        Raises:
            ValueError: 当映射不存在或参数无效时抛出
        """
        if mapping_name not in self.mappings:
            raise ValueError(f"映射 {mapping_name} 不存在")
            
        # 验证参数
        required_fields = ["id", "type"]
        for field in required_fields:
            if field not in source or not source[field]:
                raise ValueError(f"源对象缺少必要字段: {field}")
            if field not in target or not target[field]:
                raise ValueError(f"目标对象缺少必要字段: {field}")
                
        # 更新映射
        mapping = self.mappings[mapping_name]
        mapping["source"] = source
        mapping["target"] = target
        self.logger.info(f"更新映射 {mapping_name}")
        return mapping
        
    def delete_mapping(self, mapping_name: str) -> None:
        """删除知识映射
        
        Args:
            mapping_name: 映射名称
            
        Raises:
            ValueError: 当映射不存在时抛出
        """
        if mapping_name not in self.mappings:
            raise ValueError(f"映射 {mapping_name} 不存在")
            
        del self.mappings[mapping_name]
        self.logger.info(f"删除映射 {mapping_name}")
        
    def analyze_mapping(self, mapping_name: str) -> Dict[str, Any]:
        """分析知识映射
        
        Args:
            mapping_name: 映射名称
            
        Returns:
            Dict[str, Any]: 分析结果
            
        Raises:
            ValueError: 当映射不存在时抛出
        """
        if mapping_name not in self.mappings:
            raise ValueError(f"映射 {mapping_name} 不存在")
            
        mapping = self.mappings[mapping_name]
        analysis = {
            "type": "direct" if mapping["source"]["type"] == mapping["target"]["type"] else "transform",
            "properties": {
                "source_type": mapping["source"]["type"],
                "target_type": mapping["target"]["type"],
                "bidirectional": False  # 默认为单向映射
            }
        }
        self.logger.info(f"分析映射 {mapping_name}")
        return analysis 