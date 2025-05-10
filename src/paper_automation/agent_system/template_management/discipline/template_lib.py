from typing import Dict, List, Any
import logging
import json
from ..base.template import Template

class TemplateLibrary:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.templates: Dict[str, Template] = {}
        
    def add_template(self, discipline: str, template: Template) -> bool:
        """添加学科模板"""
        try:
            if not discipline or not template:
                self.logger.error("Invalid discipline or template")
                return False
                
            if discipline in self.templates:
                self.logger.warning(f"Template for discipline {discipline} already exists")
            self.templates[discipline] = template
            self.logger.info(f"Added template for discipline: {discipline}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding template: {e}")
            return False

    def get_template(self, discipline: str) -> Template:
        """获取学科模板"""
        try:
            return self.templates.get(discipline)
        except Exception as e:
            self.logger.error(f"Error getting template: {e}")
            return None

    def save_library(self, file_path: str) -> bool:
        """保存模板库到文件"""
        try:
            library_data = {
                discipline: {
                    'template_id': template.template_id,
                    'name': template.name,
                    'description': template.description,
                    'version': template.version,
                    'template_data': template.template_data,
                    'elements': template.elements,
                    'relations': template.relations
                }
                for discipline, template in self.templates.items()
            }
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(library_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Saved template library to: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving library: {e}")
            return False

    def load_library(self, file_path: str) -> bool:
        """从文件加载模板库
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否加载成功
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            if not isinstance(data, dict):
                raise ValueError("Invalid library data format")
                
            self.templates = {}
            for discipline, template_data in data.items():
                template = Template(
                    template_id=template_data['template_id'],
                    name=template_data['name'],
                    description=template_data['description'],
                    version=template_data['version'],
                    template_data=template_data.get('template_data', {})
                )
                
                # 恢复元素和关系
                template.elements = template_data.get('elements', {})
                template.relations = template_data.get('relations', {})
                
                self.templates[discipline] = template
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading library: {str(e)}")
            return False

    def remove_template(self, template_id: str) -> bool:
        """移除模板
        
        Args:
            template_id: 模板ID
            
        Returns:
            bool: 是否移除成功
            
        Raises:
            ValueError: 当模板ID为空或不存在时
        """
        if not template_id:
            raise ValueError("Template ID cannot be empty")
            
        if template_id not in self.templates:
            raise ValueError(f"Template {template_id} not found")
            
        del self.templates[template_id]
        return True 