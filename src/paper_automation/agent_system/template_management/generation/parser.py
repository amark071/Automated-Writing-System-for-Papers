from typing import Dict, List, Any
import logging
import json

class TemplateParser:
    def __init__(self, validate_schema: bool = True):
        """初始化模板解析器
        
        Args:
            validate_schema: 是否验证模板结构
        """
        self.logger = logging.getLogger(__name__)
        self.validate_schema = validate_schema
        
    def parse_template(self, template_json: str) -> Dict[str, Any]:
        """解析模板JSON字符串
        
        Args:
            template_json: 模板JSON字符串
            
        Returns:
            Dict[str, Any]: 解析后的模板数据
        """
        try:
            template_data = json.loads(template_json)
            if self.validate_schema:
                if not self.validate_template_structure(template_data):
                    raise ValueError("Invalid template structure")
            self.logger.info("Successfully parsed template JSON")
            return template_data
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse template JSON: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error parsing template: {e}")
            raise
            
    def serialize_template(self, template: 'Template') -> str:
        """序列化模板为JSON字符串
        
        Args:
            template: 要序列化的模板对象
            
        Returns:
            str: 序列化后的JSON字符串
        """
        try:
            if not template:
                raise ValueError("Template cannot be None")
                
            template_dict = {
                "template_id": template.template_id,
                "name": template.name,
                "description": template.description,
                "version": template.version,
                "structure": template.structure,
                "elements": template.elements,
                "relations": template.relations,
                "content": template.content,
                "metadata": template.metadata,
                "style": template.style
            }
            
            return json.dumps(template_dict, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error serializing template: {e}")
            raise
            
    def validate_template_structure(self, template_data: Dict[str, Any]) -> bool:
        """验证模板结构
        
        Args:
            template_data: 待验证的模板数据
            
        Returns:
            bool: 验证是否通过
        """
        try:
            # 验证基本字段
            required_fields = ['template_id', 'name', 'structure', 'elements', 'relations']
            for field in required_fields:
                if field not in template_data:
                    self.logger.error(f"Template missing required field: {field}")
                    return False
                    
            # 验证结构
            if not isinstance(template_data['structure'], dict):
                self.logger.error("structure must be a dictionary")
                return False
                
            # 验证元素
            if not isinstance(template_data['elements'], dict):
                self.logger.error("elements must be a dictionary")
                return False
                
            # 验证关系
            if not isinstance(template_data['relations'], dict):
                self.logger.error("relations must be a dictionary")
                return False
                
            # 验证内容
            if 'content' in template_data and not isinstance(template_data['content'], dict):
                self.logger.error("content must be a dictionary")
                return False
                
            # 验证元数据
            if 'metadata' in template_data and not isinstance(template_data['metadata'], dict):
                self.logger.error("metadata must be a dictionary")
                return False
                
            # 验证样式
            if 'style' in template_data and not isinstance(template_data['style'], dict):
                self.logger.error("style must be a dictionary")
                return False
                
            self.logger.info("Template structure validation passed")
            return True
        except Exception as e:
            self.logger.error(f"Error validating template structure: {e}")
            return False 