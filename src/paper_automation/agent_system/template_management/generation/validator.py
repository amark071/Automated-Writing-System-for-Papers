"""模板验证器模块

此模块实现了模板的验证功能，包括结构验证、内容验证和关系验证。
"""

from typing import Dict, List, Any, Tuple
import logging
import re
from ..base.template import Template
from ..discipline.analyzer import DisciplineAnalyzer

class TemplateValidator:
    """模板验证器"""
    
    def __init__(self, validate_structure: bool = True, validate_content: bool = True, validate_relations: bool = True):
        """初始化验证器
        
        Args:
            validate_structure: 是否验证结构
            validate_content: 是否验证内容
            validate_relations: 是否验证关系
        """
        self.logger = logging.getLogger(__name__)
        self.discipline_analyzer = DisciplineAnalyzer()
        self.validate_structure = validate_structure
        self.validate_content = validate_content
        self.validate_relations = validate_relations
        
        # 定义有效的元素类型
        self.valid_element_types = {"chapter", "section", "paragraph", "table", "figure", "code", "equation"}
        # 定义有效的关系类型
        self.valid_relation_types = {"contains", "references", "depends_on", "follows"}
        
    def validate_template(self, template: Template) -> Dict[str, Any]:
        """
        验证模板的有效性。

        Args:
            template (Template): 要验证的模板对象

        Returns:
            Dict[str, Any]: 包含验证结果的字典
                {
                    "is_valid": bool,  # 模板是否有效
                    "errors": List[str],  # 错误信息列表
                    "warnings": List[str]  # 警告信息列表
                }
        """
        result = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }

        # 验证基本信息
        if not template.template_id or not template.name:
            result["is_valid"] = False
            result["errors"].append("Invalid template basic information")

        # 验证版本格式
        if not isinstance(template.version, str) or not re.match(r'^\d+\.\d+(\.\d+)?$', template.version):
            result["is_valid"] = False
            result["errors"].append("Invalid version format")

        # 验证元素
        if not template.elements:
            result["is_valid"] = False
            result["errors"].append("Missing required elements")

        # 检查重复的元素ID
        element_ids = set()
        for element_id, element in template.elements.items():
            if not element_id or not isinstance(element, dict):
                result["is_valid"] = False
                result["errors"].append("Invalid element")
                continue
            
            if "element_id" not in element or not element["element_id"]:
                result["is_valid"] = False
                result["errors"].append("Invalid element")
                continue

            # 检查元素ID是否重复
            if element["element_id"] in element_ids:
                result["is_valid"] = False
                result["errors"].append("Duplicate element ID")
                break
            element_ids.add(element["element_id"])
            
            if "element_type" not in element:
                result["is_valid"] = False
                result["errors"].append("Invalid element")
                continue

            # 验证元素类型
            if element["element_type"] not in self.valid_element_types:
                result["is_valid"] = False
                result["errors"].append("Invalid element type")
                continue
                
            if "content" not in element or not isinstance(element["content"], dict):
                result["is_valid"] = False
                result["errors"].append("Invalid content format")
                continue

            # 验证必需属性
            if "attributes" in element:
                if not isinstance(element["attributes"], dict):
                    result["is_valid"] = False
                    result["errors"].append("Invalid element")
                    continue
                
                if "level" not in element["attributes"]:
                    result["is_valid"] = False
                    result["errors"].append("Missing required attributes")
                    continue

                # 验证样式格式
                if "style" in element["attributes"]:
                    style = element["attributes"]["style"]
                    if not isinstance(style, dict):
                        result["is_valid"] = False
                        result["errors"].append("Invalid style format")
                        continue
                    
                    # 验证样式属性
                    for key, value in style.items():
                        if key == "size":
                            if not isinstance(value, (int, float)) and not (isinstance(value, str) and value.isdigit()):
                                result["is_valid"] = False
                                result["errors"].append("Invalid style format")
                                break

        # 验证关系
        for relation_id, relation in template.relations.items():
            if not relation_id or not isinstance(relation, dict):
                result["is_valid"] = False
                result["errors"].append("Invalid relation")
                continue
                
            if "relation_id" not in relation or not relation["relation_id"]:
                result["is_valid"] = False
                result["errors"].append("Invalid relation")
                continue
                
            if "relation_type" not in relation:
                result["is_valid"] = False
                result["errors"].append("Invalid relation")
                continue

            # 验证关系类型
            if relation["relation_type"] not in self.valid_relation_types:
                result["is_valid"] = False
                result["errors"].append("Invalid relation type")
                continue
                
            if "source_id" not in relation or "target_id" not in relation:
                result["is_valid"] = False
                result["errors"].append("Invalid relation")
                continue
                
            # 验证关系引用的元素是否存在
            if relation["source_id"] not in template.elements:
                result["is_valid"] = False
                result["errors"].append("Invalid element references")
                continue
                
            if relation["target_id"] not in template.elements:
                result["is_valid"] = False
                result["errors"].append("Invalid element references")
                continue

        # 验证循环关系
        if not self._validate_circular_relations(template):
            result["is_valid"] = False
            result["errors"].append("Circular relation detected")

        # 验证其他属性
        if template.structure is not None and not isinstance(template.structure, dict):
            result["is_valid"] = False
            result["errors"].append("Invalid structure")

        if template.style is not None and not isinstance(template.style, dict):
            result["is_valid"] = False
            result["errors"].append("Invalid style")

        if template.content is not None and not isinstance(template.content, dict):
            result["is_valid"] = False
            result["errors"].append("Invalid content")

        if template.metadata is not None:
            if not isinstance(template.metadata, dict):
                result["is_valid"] = False
                result["errors"].append("Invalid metadata")
            else:
                # 验证元数据格式
                for key, value in template.metadata.items():
                    if key == "created_at" and not re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$', str(value)):
                        result["is_valid"] = False
                        result["errors"].append("Invalid metadata format")

        # 添加警告
        if not template.description:
            result["warnings"].append("Empty description")

        # 如果启用了结构验证，则验证结构
        if self.validate_structure:
            try:
                # 获取模板的学科信息
                discipline = template.template_data.get("discipline")
                if discipline:
                    # 使用学科分析器验证结构
                    structure_result = self.discipline_analyzer.analyze_structure_features(discipline)
                    if not structure_result.get("is_valid", True):
                        result["is_valid"] = False
                        result["errors"].extend(structure_result.get("errors", []))
                        result["warnings"].extend(structure_result.get("warnings", []))
            except Exception as e:
                self.logger.error(f"Error validating template structure: {e}")
                result["is_valid"] = False
                result["errors"].append("Error validating template structure")

        return result

    def _validate_circular_relations(self, template: Template) -> bool:
        """验证模板中是否存在循环关系
        
        Args:
            template: 待验证的模板
            
        Returns:
            bool: 如果不存在循环关系返回True,否则返回False
        """
        def find_cycles(node: str, visited: set, path: set) -> bool:
            if node in path:
                return True
            if node in visited:
                return False
                
            visited.add(node)
            path.add(node)
            
            # 查找所有以当前节点为源的关系
            for relation in template.relations.values():
                if relation["source_id"] == node:
                    if find_cycles(relation["target_id"], visited, path):
                        return True
                        
            path.remove(node)
            return False
            
        visited = set()
        # 对每个未访问的节点进行深度优先搜索
        for element_id in template.elements:
            if element_id not in visited:
                if find_cycles(element_id, visited, set()):
                    return False
                    
        return True

    def validate_elements(self, template: Template) -> Tuple[bool, Dict[str, Any]]:
        """验证模板元素
        
        Args:
            template: 待验证的模板
            
        Returns:
            Tuple[bool, Dict[str, Any]]: (是否通过验证, 验证结果)
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            if not hasattr(template, 'elements'):
                results["is_valid"] = False
                results["errors"].append("Template has no elements attribute")
                return False, results
                
            for element_id, element_data in template.elements.items():
                if not element_id or not element_data:
                    results["is_valid"] = False
                    results["errors"].append(f"Invalid element: {element_id}")
                    
            return results["is_valid"], results
            
        except Exception as e:
            self.logger.error(f"Error validating elements: {e}")
            return False, {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }

    def validate_relations(self, template: Template) -> Tuple[bool, Dict[str, Any]]:
        """验证模板关系
        
        Args:
            template: 待验证的模板
            
        Returns:
            Tuple[bool, Dict[str, Any]]: (是否通过验证, 验证结果)
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            if not hasattr(template, 'relations'):
                results["is_valid"] = False
                results["errors"].append("Template has no relations attribute")
                return False, results
                
            for relation_id, relation_data in template.relations.items():
                if not relation_id or not relation_data:
                    results["is_valid"] = False
                    results["errors"].append(f"Invalid relation: {relation_id}")
                    continue
                    
                if not relation_data.get('source') or not relation_data.get('target'):
                    results["is_valid"] = False
                    results["errors"].append(f"Invalid relation endpoints: {relation_id}")
                    continue
                    
                if relation_data['source'] not in template.elements or relation_data['target'] not in template.elements:
                    results["is_valid"] = False
                    results["errors"].append(f"Invalid relation references: {relation_id}")
                    
            return results["is_valid"], results
            
        except Exception as e:
            self.logger.error(f"Error validating relations: {e}")
            return False, {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }
            
    def validate_structure(self, template: Template, discipline: str) -> Dict[str, Any]:
        """验证模板结构
        
        Args:
            template: 待验证的模板
            discipline: 学科名称
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            # 获取学科特征
            discipline_features = self.discipline_analyzer.analyze_discipline(discipline)
            structure_features = discipline_features["structure"]
            
            # 验证章节结构
            chapter_results = self._validate_chapter_structure(
                template,
                structure_features["chapter_patterns"]
            )
            if not chapter_results["is_valid"]:
                results["is_valid"] = False
                results["errors"].extend(chapter_results["errors"])
                results["warnings"].extend(chapter_results["warnings"])
            
            # 验证板块结构
            section_results = self._validate_section_structure(
                template,
                structure_features["section_patterns"]
            )
            if not section_results["is_valid"]:
                results["is_valid"] = False
                results["errors"].extend(section_results["errors"])
                results["warnings"].extend(section_results["warnings"])
            
            # 验证段落结构
            paragraph_results = self._validate_paragraph_structure(
                template,
                structure_features["paragraph_patterns"]
            )
            if not paragraph_results["is_valid"]:
                results["is_valid"] = False
                results["errors"].extend(paragraph_results["errors"])
                results["warnings"].extend(paragraph_results["warnings"])
            
            # 验证元素结构
            element_results = self._validate_element_structure(
                template,
                structure_features["element_patterns"]
            )
            if not element_results["is_valid"]:
                results["is_valid"] = False
                results["errors"].extend(element_results["errors"])
                results["warnings"].extend(element_results["warnings"])
            
            self.logger.info(f"Structure validation completed for discipline: {discipline}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating structure: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }
            
    def _validate_chapter_structure(
        self,
        template: Template,
        chapter_patterns: Dict[str, Any]
    ) -> Dict[str, Any]:
        """验证章节结构
        
        Args:
            template: 待验证的模板
            chapter_patterns: 章节模式
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            if not template.template_data.get("structure"):
                results["is_valid"] = False
                results["errors"].append("Missing template structure")
                return results
                
            chapters = template.template_data["structure"].get("chapters", [])
            required_chapters = chapter_patterns.get("required_chapters", [])
            max_chapters = chapter_patterns.get("max_chapters", float('inf'))
            
            # 验证必需章节
            for required_chapter in required_chapters:
                if not any(chapter["title"] == required_chapter for chapter in chapters):
                    results["is_valid"] = False
                    results["errors"].append(f"Missing required chapter: {required_chapter}")
            
            # 验证章节数量
            if len(chapters) > max_chapters:
                results["is_valid"] = False
                results["errors"].append(f"Too many chapters: {len(chapters)} > {max_chapters}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating chapter structure: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }

    def _validate_section_structure(
        self,
        template: Template,
        section_patterns: Dict[str, Any]
    ) -> Dict[str, Any]:
        """验证板块结构
        
        Args:
            template: 待验证的模板
            section_patterns: 板块模式
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            if not template.template_data.get("content"):
                results["is_valid"] = False
                results["errors"].append("Missing template content")
                return results
                
            min_sections = section_patterns.get("min_sections_per_chapter", 1)
            max_sections = section_patterns.get("max_sections_per_chapter", float('inf'))
            
            chapters = template.template_data["structure"].get("chapters", [])
            for chapter in chapters:
                sections = chapter.get("sections", [])
                if len(sections) < min_sections:
                    results["is_valid"] = False
                    results["errors"].append(f"Too few sections in chapter {chapter['title']}: {len(sections)} < {min_sections}")
                elif len(sections) > max_sections:
                    results["is_valid"] = False
                    results["errors"].append(f"Too many sections in chapter {chapter['title']}: {len(sections)} > {max_sections}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating section structure: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }
            
    def _validate_paragraph_structure(
        self,
        template: Template,
        paragraph_patterns: Dict[str, Any]
    ) -> Dict[str, Any]:
        """验证段落结构
        
        Args:
            template: 待验证的模板
            paragraph_patterns: 段落模式
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            if not template.template_data.get("content"):
                results["is_valid"] = False
                results["errors"].append("Missing template content")
                return results
                
            min_paragraphs = paragraph_patterns.get("min_paragraphs_per_section", 1)
            max_paragraphs = paragraph_patterns.get("max_paragraphs_per_section", float('inf'))
            
            chapters = template.template_data["structure"].get("chapters", [])
            for chapter in chapters:
                for section in chapter.get("sections", []):
                    paragraphs = section.get("paragraphs", [])
                    if len(paragraphs) < min_paragraphs:
                        results["is_valid"] = False
                        results["errors"].append(
                            f"Too few paragraphs in section {section['title']} of chapter {chapter['title']}: "
                            f"{len(paragraphs)} < {min_paragraphs}"
                        )
                    elif len(paragraphs) > max_paragraphs:
                        results["is_valid"] = False
                        results["errors"].append(
                            f"Too many paragraphs in section {section['title']} of chapter {chapter['title']}: "
                            f"{len(paragraphs)} > {max_paragraphs}"
                        )
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating paragraph structure: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }

    def _validate_element_structure(
        self,
        template: Template,
        element_patterns: Dict[str, Any]
    ) -> Dict[str, Any]:
        """验证元素结构
        
        Args:
            template: 待验证的模板
            element_patterns: 元素模式
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            if not template.template_data.get("elements"):
                results["is_valid"] = False
                results["errors"].append("Missing template elements")
                return results
                
            required_elements = element_patterns.get("required_elements", [])
            max_elements = element_patterns.get("max_elements", float('inf'))
            
            elements = template.template_data["elements"]
            
            # 验证必需元素
            for required_element in required_elements:
                if not any(element["type"] == required_element for element in elements.values()):
                    results["is_valid"] = False
                    results["errors"].append(f"Missing required element type: {required_element}")
            
            # 验证元素数量
            if len(elements) > max_elements:
                results["is_valid"] = False
                results["errors"].append(f"Too many elements: {len(elements)} > {max_elements}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating element structure: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }

    def validate_content(self, template: Template, rules: Dict[str, Any] = None) -> Dict[str, Any]:
        """验证模板内容
        
        Args:
            template: 待验证的模板
            rules: 验证规则（可选）
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            if not template.template_data.get("content"):
                results["is_valid"] = False
                results["errors"].append("Missing template content")
                return results
            
            # 验证内容完整性
            chapters = template.template_data["structure"].get("chapters", [])
            for chapter in chapters:
                if not chapter.get("title"):
                    results["is_valid"] = False
                    results["errors"].append("Chapter missing title")
                    continue
                    
                for section in chapter.get("sections", []):
                    if not section.get("title"):
                        results["is_valid"] = False
                        results["errors"].append(f"Section missing title in chapter {chapter['title']}")
                        continue
                        
                    for paragraph in section.get("paragraphs", []):
                        if not paragraph.get("content"):
                            results["is_valid"] = False
                            results["errors"].append(
                                f"Paragraph missing content in section {section['title']} "
                                f"of chapter {chapter['title']}"
                            )
            
            # 如果提供了规则，进行额外验证
            if rules:
                min_sections = rules.get("min_sections_per_chapter", 1)
                max_sections = rules.get("max_sections_per_chapter", float('inf'))
                
                for chapter in chapters:
                    sections = chapter.get("sections", [])
                    if len(sections) < min_sections:
                        results["is_valid"] = False
                        results["errors"].append(
                            f"Too few sections in chapter {chapter['title']}: "
                            f"{len(sections)} < {min_sections}"
                        )
                    elif len(sections) > max_sections:
                        results["is_valid"] = False
                        results["errors"].append(
                            f"Too many sections in chapter {chapter['title']}: "
                            f"{len(sections)} > {max_sections}"
                        )
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating content: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }

    def _validate_metadata(self, template: Template) -> Dict[str, Any]:
        """验证模板元数据
        
        Args:
            template: 待验证的模板
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            metadata = template.template_data.get("metadata", {})
            required_fields = ["title", "author", "version", "created_at", "updated_at"]
            
            for field in required_fields:
                if not metadata.get(field):
                    results["is_valid"] = False
                    results["errors"].append(f"Missing required metadata field: {field}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating metadata: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }

    def _validate_relationships(self, template: Template) -> Dict[str, Any]:
        """验证模板关系
        
        Args:
            template: 待验证的模板
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            relationships = template.template_data.get("relationships", {})
            elements = template.template_data.get("elements", {})
            
            for rel_id, rel_data in relationships.items():
                if not rel_data.get("source") or not rel_data.get("target"):
                    results["is_valid"] = False
                    results["errors"].append(f"Relationship {rel_id} missing source or target")
                    continue
                    
                source = rel_data["source"]
                target = rel_data["target"]
                
                if source not in elements:
                    results["is_valid"] = False
                    results["errors"].append(f"Relationship {rel_id} has invalid source: {source}")
                
                if target not in elements:
                    results["is_valid"] = False
                    results["errors"].append(f"Relationship {rel_id} has invalid target: {target}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating relationships: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }

    def _validate_cross_references(self, template: Template) -> Dict[str, Any]:
        """验证模板交叉引用
        
        Args:
            template: 待验证的模板
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            # 获取所有元素和引用
            elements = template.template_data.get("elements", {})
            references = template.template_data.get("references", {})
            
            # 收集所有元素ID
            element_ids = set(elements.keys())
            
            # 验证每个引用
            for ref_id, ref in references.items():
                # 验证引用基本结构
                if not isinstance(ref, dict):
                    results["is_valid"] = False
                    results["errors"].append(f"引用 {ref_id} 必须是字典类型")
                    continue
                    
                # 验证引用ID
                if "id" not in ref:
                    results["is_valid"] = False
                    results["errors"].append(f"引用 {ref_id} 缺少ID")
                    continue
                elif not isinstance(ref["id"], str):
                    results["is_valid"] = False
                    results["errors"].append(f"引用 {ref_id} 的ID必须是字符串类型")
                    continue
                    
                # 验证引用类型
                if "type" not in ref:
                    results["is_valid"] = False
                    results["errors"].append(f"引用 {ref_id} 缺少类型")
                    continue
                elif not isinstance(ref["type"], str):
                    results["is_valid"] = False
                    results["errors"].append(f"引用 {ref_id} 的类型必须是字符串类型")
                    continue
                elif ref["type"] not in ["cite", "link", "include"]:
                    results["warnings"].append(f"引用 {ref_id} 使用了可能不受支持的引用类型: {ref['type']}")
                    
                # 验证源元素
                if "source" not in ref:
                    results["is_valid"] = False
                    results["errors"].append(f"引用 {ref_id} 缺少源元素")
                    continue
                elif not isinstance(ref["source"], str):
                    results["is_valid"] = False
                    results["errors"].append(f"引用 {ref_id} 的源元素必须是字符串类型")
                    continue
                elif ref["source"] not in element_ids:
                    results["is_valid"] = False
                    results["errors"].append(f"引用 {ref_id} 引用了不存在的源元素: {ref['source']}")
                    continue
                    
                # 验证目标元素
                if "target" not in ref:
                    results["is_valid"] = False
                    results["errors"].append(f"引用 {ref_id} 缺少目标元素")
                    continue
                elif not isinstance(ref["target"], str):
                    results["is_valid"] = False
                    results["errors"].append(f"引用 {ref_id} 的目标元素必须是字符串类型")
                    continue
                elif ref["target"] not in element_ids:
                    results["is_valid"] = False
                    results["errors"].append(f"引用 {ref_id} 引用了不存在的目标元素: {ref['target']}")
                    continue
                    
                # 验证源元素和目标元素不能相同
                if ref["source"] == ref["target"]:
                    results["is_valid"] = False
                    results["errors"].append(f"引用 {ref_id} 的源元素和目标元素不能相同")
                    continue
                    
                # 验证引用属性
                if "attributes" in ref:
                    attributes = ref["attributes"]
                    if not isinstance(attributes, dict):
                        results["is_valid"] = False
                        results["errors"].append(f"引用 {ref_id} 的属性必须是字典类型")
                    else:
                        # 验证引用格式
                        if "format" in attributes:
                            if not isinstance(attributes["format"], str):
                                results["is_valid"] = False
                                results["errors"].append(f"引用 {ref_id} 的格式必须是字符串类型")
                            elif attributes["format"] not in ["text", "code", "math", "table", "image"]:
                                results["warnings"].append(f"引用 {ref_id} 使用了可能不受支持的格式: {attributes['format']}")
                                
                        # 验证引用位置
                        if "position" in attributes:
                            if not isinstance(attributes["position"], str):
                                results["is_valid"] = False
                                results["errors"].append(f"引用 {ref_id} 的位置必须是字符串类型")
                            elif attributes["position"] not in ["inline", "block", "footnote"]:
                                results["warnings"].append(f"引用 {ref_id} 使用了可能不受支持的位置: {attributes['position']}")
                                
                        # 验证引用样式
                        if "style" in attributes:
                            style = attributes["style"]
                            if not isinstance(style, dict):
                                results["is_valid"] = False
                                results["errors"].append(f"引用 {ref_id} 的样式必须是字典类型")
                            else:
                                # 验证字体样式
                                if "font" in style:
                                    if not isinstance(style["font"], dict):
                                        results["is_valid"] = False
                                        results["errors"].append(f"引用 {ref_id} 的字体样式必须是字典类型")
                                    else:
                                        if "family" in style["font"]:
                                            if not isinstance(style["font"]["family"], str):
                                                results["is_valid"] = False
                                                results["errors"].append(f"引用 {ref_id} 的字体族必须是字符串类型")
                                        if "size" in style["font"]:
                                            if not isinstance(style["font"]["size"], (int, float)):
                                                results["is_valid"] = False
                                                results["errors"].append(f"引用 {ref_id} 的字体大小必须是数字类型")
                                                
                        # 验证颜色样式
                        if "color" in style:
                            if not isinstance(style["color"], str):
                                results["is_valid"] = False
                                results["errors"].append(f"引用 {ref_id} 的颜色必须是字符串类型")
                                
                # 验证引用约束
                if "constraints" in ref:
                    constraints = ref["constraints"]
                    if not isinstance(constraints, dict):
                        results["is_valid"] = False
                        results["errors"].append(f"引用 {ref_id} 的约束必须是字典类型")
                    else:
                        # 验证唯一性约束
                        if "unique" in constraints:
                            if not isinstance(constraints["unique"], bool):
                                results["is_valid"] = False
                                results["errors"].append(f"引用 {ref_id} 的唯一性约束必须是布尔类型")
                                
                        # 验证可见性约束
                        if "visible" in constraints:
                            if not isinstance(constraints["visible"], bool):
                                results["is_valid"] = False
                                results["errors"].append(f"引用 {ref_id} 的可见性约束必须是布尔类型")
                                
                        # 验证可编辑性约束
                        if "editable" in constraints:
                            if not isinstance(constraints["editable"], bool):
                                results["is_valid"] = False
                                results["errors"].append(f"引用 {ref_id} 的可编辑性约束必须是布尔类型")
                                
            # 验证引用完整性
            if references:
                # 检查是否存在循环引用
                visited = set()
                path = set()
                
                def check_cycle(ref_id: str) -> bool:
                    if ref_id in path:
                        return True
                    if ref_id in visited:
                        return False
                        
                    visited.add(ref_id)
                    path.add(ref_id)
                    
                    ref = references.get(ref_id)
                    if ref and "target" in ref:
                        if ref["target"] in visited:
                            if check_cycle(ref["target"]):
                                return True
                                
                    path.remove(ref_id)
                    return False
                    
                for ref_id in references:
                    if ref_id not in visited:
                        if check_cycle(ref_id):
                            results["is_valid"] = False
                            results["errors"].append("存在循环引用")
                            break
                            
            # 记录验证结果
            if results["is_valid"]:
                self.logger.info("模板交叉引用验证通过")
            else:
                self.logger.error("模板交叉引用验证失败")
                for error in results["errors"]:
                    self.logger.error(f"错误: {error}")
                for warning in results["warnings"]:
                    self.logger.warning(f"警告: {warning}")
                
        except Exception as e:
            results["is_valid"] = False
            results["errors"].append(f"交叉引用验证过程发生异常: {str(e)}")
            self.logger.error(f"交叉引用验证异常: {str(e)}")
            
        return results

    def _validate_formatting(self, template: Template) -> Dict[str, Any]:
        """验证模板格式
        
        Args:
            template: 待验证的模板
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            formatting = template.template_data.get("formatting", {})
            required_fields = ["font", "font_size", "line_spacing", "margins"]
            
            for field in required_fields:
                if not formatting.get(field):
                    results["is_valid"] = False
                    results["errors"].append(f"Missing required formatting field: {field}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating formatting: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }

    def _validate_completeness(self, template: Template) -> Dict[str, Any]:
        """验证模板完整性
        
        Args:
            template: 待验证的模板
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            required_sections = [
                "metadata",
                "structure",
                "content",
                "elements",
                "relationships",
                "references",
                "formatting"
            ]
            
            for section in required_sections:
                if not template.template_data.get(section):
                    results["is_valid"] = False
                    results["errors"].append(f"Missing required template section: {section}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating completeness: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }

    def _validate_consistency(self, template: Template) -> Dict[str, Any]:
        """验证模板一致性
        
        Args:
            template: 待验证的模板
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            # 验证结构和内容的一致性
            structure = template.template_data.get("structure", {})
            content = template.template_data.get("content", {})
            
            # 验证章节一致性
            structure_chapters = {chapter["id"] for chapter in structure.get("chapters", [])}
            content_chapters = set(content.get("chapters", {}).keys())
            
            missing_chapters = structure_chapters - content_chapters
            extra_chapters = content_chapters - structure_chapters
            
            if missing_chapters:
                results["is_valid"] = False
                results["errors"].append(f"Chapters in structure but not in content: {missing_chapters}")
            
            if extra_chapters:
                results["is_valid"] = False
                results["errors"].append(f"Chapters in content but not in structure: {extra_chapters}")
            
            # 验证元素引用一致性
            elements = template.template_data.get("elements", {})
            relationships = template.template_data.get("relationships", {})
            references = template.template_data.get("references", {})
            
            element_ids = set(elements.keys())
            
            # 检查关系中的元素引用
            for rel in relationships.values():
                if rel.get("source") not in element_ids:
                    results["is_valid"] = False
                    results["errors"].append(f"Relationship references non-existent element: {rel.get('source')}")
                if rel.get("target") not in element_ids:
                    results["is_valid"] = False
                    results["errors"].append(f"Relationship references non-existent element: {rel.get('target')}")
            
            # 检查引用中的元素引用
            for ref in references.values():
                if ref.get("source") not in element_ids:
                    results["is_valid"] = False
                    results["errors"].append(f"Reference references non-existent element: {ref.get('source')}")
                if ref.get("target") not in element_ids:
                    results["is_valid"] = False
                    results["errors"].append(f"Reference references non-existent element: {ref.get('target')}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating consistency: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }

    def validate_element(self, element: Dict[str, Any]) -> Dict[str, Any]:
        """验证单个元素
        
        Args:
            element: 待验证的元素
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            if not element:
                results["is_valid"] = False
                results["errors"].append("Element cannot be empty")
                return results
                
            if not element.get("element_id"):
                results["is_valid"] = False
                results["errors"].append("Element must have an ID")
                
            if not element.get("element_type"):
                results["is_valid"] = False
                results["errors"].append("Element must have a type")
                
            if not element.get("content"):
                results["is_valid"] = False
                results["errors"].append("Element must have content")
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating element: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }
            
    def validate_relation(self, relation: Dict[str, Any]) -> Dict[str, Any]:
        """验证单个关系
        
        Args:
            relation: 待验证的关系
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            if not relation:
                results["is_valid"] = False
                results["errors"].append("Relation cannot be empty")
                return results
                
            if not relation.get("relation_id"):
                results["is_valid"] = False
                results["errors"].append("Relation must have an ID")
                
            if not relation.get("source_id"):
                results["is_valid"] = False
                results["errors"].append("Relation must have a source ID")
                
            if not relation.get("target_id"):
                results["is_valid"] = False
                results["errors"].append("Relation must have a target ID")
                
            if not relation.get("relation_type"):
                results["is_valid"] = False
                results["errors"].append("Relation must have a type")
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating relation: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }
            
    def validate_template_content(self, template: Template) -> Dict[str, Any]:
        """验证模板内容
        
        Args:
            template: 待验证的模板
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            if not template.content:
                results["is_valid"] = False
                results["errors"].append("Template must have content")
                return results
                
            # 验证内容格式
            if not isinstance(template.content, dict):
                results["is_valid"] = False
                results["errors"].append("Content must be a dictionary")
                
            # 验证内容完整性
            if not template.content.get("title"):
                results["is_valid"] = False
                results["errors"].append("Content must have a title")
                
            # 验证内容一致性
            if template.content.get("version") != template.version:
                results["warnings"].append("Content version does not match template version")
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating template content: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            }
            
    def validate_template_structure(self, template: Template) -> Dict[str, Any]:
        """验证模板结构
        
        Args:
            template: 待验证的模板
            
        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            results = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            if not template.structure:
                results["is_valid"] = False
                results["errors"].append("Template must have structure")
                return results
                
            # 验证结构格式
            if not isinstance(template.structure, dict):
                results["is_valid"] = False
                results["errors"].append("Structure must be a dictionary")
                
            # 验证章节结构
            if not template.structure.get("chapters"):
                results["is_valid"] = False
                results["errors"].append("Structure must have chapters")
                
            # 验证元素结构
            if not template.elements:
                results["is_valid"] = False
                results["errors"].append("Template must have elements")
                
            # 验证关系结构
            if not template.relations:
                results["is_valid"] = False
                results["errors"].append("Template must have relations")
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating template structure: {e}")
            return {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": []
            } 