"""基础模板模块

该模块提供了论文模板的基础类，包括：
1. 模板类 (Template)
2. 模板元素类 (TemplateElement)
3. 模板关系类 (TemplateRelation)
"""

from .template import Template, Element, Paragraph, Section, Chapter
from .template_element import TemplateElement
from .template_relation import TemplateRelation

__all__ = [
    'Template',
    'Element',
    'Paragraph',
    'Section',
    'Chapter',
    'TemplateElement',
    'TemplateRelation'
] 