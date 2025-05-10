from typing import Dict, List, Any, Set
import logging
from ..base.template import Template
from ..base.template_element import TemplateElement
from .evaluator import TemplateEvaluator
from .monitor import PerformanceMonitor

class TemplateOptimizer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.evaluator = TemplateEvaluator()
        self.monitor = PerformanceMonitor()
        self.required_sections = {"abstract", "introduction", "methods", "results", "discussion"}
        
    def optimize_template(self, template: Template) -> Template:
        """优化模板"""
        try:
            self.monitor.start_monitoring("optimize_template")
            
            # 评估当前模板
            initial_scores = self.evaluator.evaluate_template(template)
            
            # 优化结构
            template = self.optimize_structure(template)
            
            # 优化关系
            template = self.optimize_relations(template)
            
            # 优化内容
            template = self.optimize_content(template)
            
            # 评估优化结果
            final_scores = self.evaluator.evaluate_template(template)
            
            duration = self.monitor.stop_monitoring("optimize_template")
            self.logger.info(f"Optimized template: {template.template_id}")
            self.logger.info(f"Score improvement: {final_scores['total_score'] - initial_scores['total_score']}")
            self.logger.info(f"Optimization completed in {duration:.2f} seconds")
            
            return template
        except Exception as e:
            self.logger.error(f"Error optimizing template: {e}")
            return template

    def optimize_structure(self, template: Template) -> Template:
        """优化模板结构"""
        try:
            if not template.elements:
                return template
                
            # 首先移除无效元素
            self._remove_invalid_elements(template)
                
            # 优化元素层级关系
            for element in template.elements.values():
                if element.element_type == "section":
                    self._optimize_section_structure(element)
                    
            # 检查并修复缺失的必要部分
            self._ensure_required_sections(template)
            
            return template
        except Exception as e:
            self.logger.error(f"Error optimizing structure: {e}")
            return template

    def optimize_relations(self, template: Template) -> Template:
        """优化模板关系"""
        try:
            if not template.relations:
                return template
                
            # 检查并修复关系完整性
            valid_relations = {}
            for rel_id, relation in template.relations.items():
                if (relation.source_id in template.elements and 
                    relation.target_id in template.elements):
                    valid_relations[rel_id] = relation
                    
            template.relations = valid_relations
            
            # 确保关系类型正确
            for relation in template.relations.values():
                self._validate_relation_type(relation)
            
            return template
        except Exception as e:
            self.logger.error(f"Error optimizing relations: {e}")
            return template

    def optimize_content(self, template: Template) -> Template:
        """优化模板内容"""
        try:
            if not template.elements:
                return template
                
            # 优化每个元素的内容
            for element in template.elements.values():
                self._optimize_element_content(element)
            
            return template
        except Exception as e:
            self.logger.error(f"Error optimizing content: {e}")
            return template
            
    def _optimize_section_structure(self, element: TemplateElement) -> None:
        """优化章节结构"""
        try:
            content = element.content
            if not isinstance(content, dict):
                content = {}
                
            # 确保必要的字段存在
            if "level" not in content:
                content["level"] = 1
            if "content" not in content:
                content["content"] = ""
                
            element.content = content
        except Exception as e:
            self.logger.error(f"Error optimizing section structure: {e}")
            
    def _ensure_required_sections(self, template: Template) -> None:
        """确保必要章节存在"""
        try:
            present_sections = {elem.content.get("content", "").lower() 
                              for elem in template.elements.values() 
                              if elem.element_type == "section"}
                              
            missing_sections = self.required_sections - present_sections
            
            for section in missing_sections:
                element_id = f"section_{section}"
                element = TemplateElement(
                    element_id=element_id,
                    element_type="section",
                    content={"content": section.capitalize(), "level": 1}
                )
                template.elements[element_id] = element
        except Exception as e:
            self.logger.error(f"Error ensuring required sections: {e}")
            
    def _remove_invalid_elements(self, template: Template) -> None:
        """移除无效元素"""
        try:
            valid_elements = {}
            for elem_id, element in template.elements.items():
                if element is not None and isinstance(element, TemplateElement):
                    try:
                        # 验证元素的必要属性
                        if (hasattr(element, 'element_id') and 
                            hasattr(element, 'element_type') and 
                            hasattr(element, 'content')):
                            valid_elements[elem_id] = element
                    except Exception as e:
                        self.logger.error(f"Error validating element {elem_id}: {e}")
            template.elements = valid_elements
        except Exception as e:
            self.logger.error(f"Error removing invalid elements: {e}")
            
    def _validate_relation_type(self, relation: Any) -> None:
        """验证关系类型"""
        try:
            valid_types = {"sequence", "reference", "dependency"}
            if relation.relation_type not in valid_types:
                relation.relation_type = "sequence"
        except Exception as e:
            self.logger.error(f"Error validating relation type: {e}")
            
    def _optimize_element_content(self, element: TemplateElement) -> None:
        """优化元素内容"""
        try:
            if not isinstance(element.content, dict):
                element.content = {}
                
            # 确保内容格式正确
            if element.element_type == "section":
                if "content" not in element.content:
                    element.content["content"] = ""
                if "level" not in element.content:
                    element.content["level"] = 1
        except Exception as e:
            self.logger.error(f"Error optimizing element content: {e}") 