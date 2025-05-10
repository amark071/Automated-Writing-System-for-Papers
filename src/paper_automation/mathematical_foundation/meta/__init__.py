"""
元分析理论模块

包含以下系统：
1. 系统完备性分析
2. 系统一致性检验
3. 系统结构分析
4. 系统关系验证
5. 系统优化评估
6. 系统演化预测
7. 范畴论系统
8. 同调代数系统
9. 代数K理论系统
10. 代数表示论系统
11. 模论系统
12. 模糊逻辑系统
13. 直觉主义逻辑系统
14. 模态逻辑系统
15. 多值逻辑系统
16. 非经典逻辑系统
"""

from .meta_analysis import *

__all__ = [
    'CompletenessAnalyzer',
    'ConsistencyChecker',
    'StructureAnalyzer',
    'RelationValidator',
    'OptimizationEvaluator',
    'EvolutionPredictor',
    'CategoryTheorySystem',
    'HomologicalAlgebraSystem',
    'AlgebraicKTheorySystem',
    'RepresentationTheorySystem',
    'ModuleTheorySystem',
    'FuzzyLogicSystem',
    'IntuitionisticLogicSystem',
    'ModalLogicSystem',
    'ManyValuedLogicSystem',
    'NonClassicalLogicSystem'
]
