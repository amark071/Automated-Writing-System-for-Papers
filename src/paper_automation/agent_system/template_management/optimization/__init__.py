"""模板优化模块

该模块提供了论文模板的优化、监控和评估功能，包括：
1. 模板优化：优化模板的结构、关系和内容
2. 性能监控：监控模板的使用情况和性能指标
3. 质量评估：评估模板的质量和适用性
"""

from .optimizer import TemplateOptimizer
from .monitor import TemplateMonitor, MonitoringMetrics
from .evaluator import TemplateEvaluator, EvaluationResult

__all__ = [
    'TemplateOptimizer',
    'TemplateMonitor',
    'MonitoringMetrics',
    'TemplateEvaluator',
    'EvaluationResult'
] 