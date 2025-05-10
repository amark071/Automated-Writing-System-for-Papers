"""
文献管理模块，用于管理论文文献的收集、解析、分类等功能。
"""

from .literature_parser import LiteratureParser, ParsedPaper
from .classifier import LiteratureClassifier
from .collector import LiteratureMetadata

__all__ = [
    "LiteratureParser",
    "ParsedPaper",
    "LiteratureClassifier",
    "LiteratureMetadata"
]

# 版本信息
__version__ = "1.0.0"
__author__ = "Paper Automation Team"
__description__ = "文献管理模块，提供论文文献的收集、解析、分类等功能" 