"""
规则扩展理论模块

包含以下系统：
1. 规则发现算法
2. 规则验证机制
3. 规则演化系统
4. 规则冲突处理
5. 置换群系统
6. 理想环系统
7. 域扩张系统
8. 格论系统
9. 偏序关系系统
10. 序代数系统
11. 偏序集系统
12. 格论系统
13. 序关系系统
14. 范畴论系统
15. 范畴代数系统
"""

from .rule_extension import *

__all__ = [
    'RuleDiscoveryAlgorithm',
    'RuleValidationMechanism',
    'RuleEvolutionSystem',
    'RuleConflictHandler',
    'PermutationGroupSystem',
    'IdealRingSystem',
    'FieldExtensionSystem',
    'LatticeTheorySystem',
    'PartialOrderSystem',
    'OrderAlgebraSystem',
    'PosetSystem',
    'LatticeSystem',
    'OrderRelationSystem',
    'CategoryTheorySystem',
    'CategoryAlgebraSystem'
]
