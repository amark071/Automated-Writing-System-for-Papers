"""
数学基础层

包含以下模块：
1. 映射理论 (mapping)
2. 规则扩展理论 (extension)
3. 动态交互理论 (dynamic)
4. 元分析理论 (meta)
"""

from .mapping import mapping_theory
from .extension import rule_extension
from .dynamic import basic_dynamic, advanced_dynamic, probability_algebra, dynamic_analysis
from .meta import meta_analysis

__all__ = [
    'mapping_theory',
    'rule_extension',
    'basic_dynamic',
    'advanced_dynamic',
    'probability_algebra',
    'dynamic_analysis',
    'meta_analysis'
]
