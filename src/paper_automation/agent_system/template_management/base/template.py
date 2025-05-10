from typing import Dict, List, Any, Union, Optional
import logging
from .template_element import TemplateElement
from .template_relation import TemplateRelation
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Template:
    """模板类"""
    
    template_id: str
    name: str = None
    description: str = ""
    structure: Dict[str, Any] = field(default_factory=dict)
    elements: Dict[str, Any] = field(default_factory=dict)
    relations: Dict[str, Any] = field(default_factory=dict)
    content: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    template_data: Dict[str, Any] = field(default_factory=dict)
    style: Dict[str, Any] = field(default_factory=dict)
    version: str = "1.0.0"
    discipline: str = ""
    
    def __post_init__(self):
        """初始化后的验证和设置"""
        if not self.template_id:
            raise ValueError("Template ID cannot be empty")
            
        if not self.name:
            raise ValueError("Template name cannot be empty")
            
        # 初始化元数据
        if not self.metadata:
            self.metadata = {
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "version": self.version
            }
            
        # 从 template_data 初始化其他属性
        if self.template_data:
            self.name = self.template_data.get("name", self.name)
            self.description = self.template_data.get("description", self.description)
            self.structure = self.template_data.get("structure", self.structure)
            self.elements = self.template_data.get("elements", self.elements)
            self.relations = self.template_data.get("relations", self.relations)
            self.content = self.template_data.get("content", self.content)
            self.style = self.template_data.get("style", self.style)
            self.version = self.template_data.get("version", self.version)
            
    @property
    def chapters(self) -> List[Dict[str, Any]]:
        """获取章节列表"""
        return self.structure.get("chapters", [])
        
    def add_element(self, element: Dict[str, Any]) -> bool:
        """添加元素
        
        Args:
            element: 元素数据
            
        Returns:
            bool: 是否添加成功
        """
        if not element:
            raise ValueError("Element data cannot be empty")
            
        element_id = element.get("element_id")
        if not element_id:
            raise ValueError("Element ID cannot be empty")
            
        if element_id in self.elements:
            raise ValueError(f"Element {element_id} already exists")
            
        self.elements[element_id] = element
        self.metadata["updated_at"] = datetime.now().isoformat()
        return True
        
    def get_element(self, element_id: str) -> Dict[str, Any]:
        """获取元素
        
        Args:
            element_id: 元素ID
            
        Returns:
            Dict[str, Any]: 元素数据
        """
        if not element_id:
            raise ValueError("Element ID cannot be empty")
            
        return self.elements.get(element_id, {})
        
    def remove_element(self, element_id: str) -> bool:
        """删除元素
        
        Args:
            element_id: 元素ID
            
        Returns:
            bool: 是否删除成功
        """
        if not element_id:
            raise ValueError("Element ID cannot be empty")
            
        if element_id in self.elements:
            del self.elements[element_id]
            self.metadata["updated_at"] = datetime.now().isoformat()
            
        return True
        
    def add_relation(self, relation: Dict[str, Any]) -> bool:
        """添加关系
        
        Args:
            relation: 关系数据
            
        Returns:
            bool: 是否添加成功
        """
        if not relation:
            raise ValueError("Relation data cannot be empty")
            
        relation_id = relation.get("relation_id")
        if not relation_id:
            raise ValueError("Relation ID cannot be empty")
            
        source_id = relation.get("source_id")
        target_id = relation.get("target_id")
        if not source_id or not target_id:
            raise KeyError("Source and target IDs cannot be empty")
            
        if source_id not in self.elements:
            raise KeyError(f"Source element {source_id} not found")
            
        if target_id not in self.elements:
            raise KeyError(f"Target element {target_id} not found")
            
        if relation_id in self.relations:
            raise ValueError(f"Relation {relation_id} already exists")
            
        self.relations[relation_id] = relation
        self.metadata["updated_at"] = datetime.now().isoformat()
        return True
        
    def get_relation(self, relation_id: str) -> Dict[str, Any]:
        """获取关系
        
        Args:
            relation_id: 关系ID
            
        Returns:
            Dict[str, Any]: 关系数据
        """
        if not relation_id:
            raise ValueError("Relation ID cannot be empty")
            
        return self.relations.get(relation_id, {})
        
    def remove_relation(self, relation_id: str) -> bool:
        """删除关系
        
        Args:
            relation_id: 关系ID
            
        Returns:
            bool: 是否删除成功
        """
        if not relation_id:
            raise ValueError("Relation ID cannot be empty")
            
        if relation_id in self.relations:
            del self.relations[relation_id]
            self.metadata["updated_at"] = datetime.now().isoformat()
            
        return True
        
    def validate(self) -> bool:
        """验证模板
        
        Returns:
            bool: 是否有效
        """
        try:
            if not self.template_id:
                raise ValueError("Template ID cannot be empty")
                
            if not self.name:
                raise ValueError("Template name cannot be empty")
                
            if not isinstance(self.structure, dict):
                raise ValueError("Structure must be a dictionary")
                
            if not isinstance(self.elements, dict):
                raise ValueError("Elements must be a dictionary")
                
            if not isinstance(self.relations, dict):
                raise ValueError("Relations must be a dictionary")
                
            if not isinstance(self.content, dict):
                raise ValueError("Content must be a dictionary")
                
            return True
            
        except Exception:
            return False
            
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典
        
        Returns:
            Dict[str, Any]: 字典表示
        """
        return {
            "template_id": self.template_id,
            "name": self.name,
            "description": self.description,
            "structure": self.structure,
            "elements": self.elements,
            "relations": self.relations,
            "content": self.content,
            "metadata": self.metadata,
            "template_data": self.template_data,
            "style": self.style,
            "version": self.version
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Template":
        """从字典创建模板

        Args:
            data: 字典格式的模板数据

        Returns:
            Template: 模板对象
        """
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
            
        if "template_id" not in data:
            raise ValueError("Template ID is required")
            
        return cls(
            template_id=data["template_id"],
            name=data.get("name", "未命名模板"),
            description=data.get("description", ""),
            structure=data.get("structure", {}),
            elements=data.get("elements", {}),
            relations=data.get("relations", {}),
            content=data.get("content", {}),
            metadata=data.get("metadata", {}),
            template_data=data.get("template_data", {}),
            style=data.get("style", {}),
            version=data.get("version", "1.0.0")
        )

class Element:
    def __init__(self, element_id: str, element_type: str, content: Dict[str, Any] = None):
        self.logger = logging.getLogger(__name__)
        if not element_id:
            raise ValueError("Element ID cannot be empty")
        if not element_type:
            raise ValueError("Element type cannot be empty")
        self.element_id = element_id
        self.element_type = element_type
        self.content = content or {}
        
    def validate(self) -> bool:
        """Validate element"""
        try:
            if not self.element_id or not self.element_type:
                return False
            return True
        except Exception as e:
            self.logger.error(f"Error validating element: {e}")
            return False

class Paragraph:
    def __init__(self, paragraph_id: str, content: str, style: Dict[str, Any] = None):
        self.logger = logging.getLogger(__name__)
        if not paragraph_id:
            raise ValueError("Paragraph ID cannot be empty")
        if not content:
            raise ValueError("Paragraph content cannot be empty")
        self.paragraph_id = paragraph_id
        self.content = content
        self.style = style or {}
        self.elements = []
        
    def add_element(self, element: Element) -> bool:
        """Add an element to the paragraph"""
        if not isinstance(element, Element):
            raise ValueError("Invalid element object")
        try:
            self.elements.append(element)
            self.logger.info(f"Added element: {element.element_id} to paragraph: {self.paragraph_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding element: {e}")
            return False
            
    def validate(self) -> bool:
        """Validate paragraph"""
        try:
            if not self.paragraph_id or not self.content:
                return False
            for element in self.elements:
                if not element.validate():
                    return False
            return True
        except Exception as e:
            self.logger.error(f"Error validating paragraph: {e}")
            return False

class Section:
    def __init__(self, section_id: str, title: str, content: Dict[str, Any] = None):
        self.logger = logging.getLogger(__name__)
        if not section_id:
            raise ValueError("Section ID cannot be empty")
        if not title:
            raise ValueError("Section title cannot be empty")
        self.section_id = section_id
        self.title = title
        self.content = content or {}
        self.paragraphs = []
        
    def add_paragraph(self, paragraph: Paragraph) -> bool:
        """Add a paragraph to the section"""
        if not isinstance(paragraph, Paragraph):
            raise ValueError("Invalid paragraph object")
        try:
            self.paragraphs.append(paragraph)
            self.logger.info(f"Added paragraph: {paragraph.paragraph_id} to section: {self.section_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding paragraph: {e}")
            return False
            
    def validate(self) -> bool:
        """Validate section"""
        try:
            if not self.section_id or not self.title:
                return False
            for paragraph in self.paragraphs:
                if not paragraph.validate():
                    return False
            return True
        except Exception as e:
            self.logger.error(f"Error validating section: {e}")
            return False

class Chapter:
    """Chapter class for template management"""
    
    def __init__(self, chapter_id: str, title: str, content: Dict[str, Any] = None):
        """Initialize chapter
        
        Args:
            chapter_id: Unique identifier for the chapter
            title: Chapter title
            content: Additional chapter content
        """
        self.logger = logging.getLogger(__name__)
        if not chapter_id:
            raise ValueError("Chapter ID cannot be empty")
        if not title:
            raise ValueError("Chapter title cannot be empty")
        self.chapter_id = chapter_id
        self.title = title
        self.content = content or {}
        self.sections = []
        
    def add_section(self, section: Section) -> bool:
        """Add a section to the chapter
        
        Args:
            section: Section object to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not isinstance(section, Section):
            raise ValueError("Invalid section object")
        try:
            self.sections.append(section)
            self.logger.info(f"Added section: {section.section_id} to chapter: {self.chapter_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding section: {e}")
            return False
            
    def validate(self) -> bool:
        """Validate chapter structure
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not self.chapter_id or not self.title:
                return False
            for section in self.sections:
                if not section.validate():
                    return False
            return True
        except Exception as e:
            self.logger.error(f"Error validating chapter: {e}")
            return False 