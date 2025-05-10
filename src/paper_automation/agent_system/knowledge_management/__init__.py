"""知识管理系统

该模块提供了论文自动化写作系统的知识管理功能，包括：
1. 文献管理 (literature)
   - 文献收集器
   - 文献解析器
   - 文献分类器
2. 知识图谱 (knowledge_graph)
   - 基础图谱
   - 学科图谱
3. 规则引擎 (rules)
   - 规则引擎核心
   - 规则定义器
   - 规则应用器
   - 规则验证器
4. 知识表示 (representation)
   - 知识矩阵接口
   - 知识谱系接口
   - 知识映射接口
"""

from .literature import collector, literature_parser, classifier
from .knowledge_graph import base, discipline
from .rules import engine, definer, applier, validator
from .representation import MatrixInterface, SpectrumInterface, MappingInterface

__all__ = [
    # 文献管理
    'collector',
    'literature_parser',
    'classifier',
    
    # 知识图谱
    'base',
    'discipline',
    
    # 规则引擎
    'engine',
    'definer',
    'applier',
    'validator',
    
    # 知识表示
    'MatrixInterface',
    'SpectrumInterface',
    'MappingInterface'
] 