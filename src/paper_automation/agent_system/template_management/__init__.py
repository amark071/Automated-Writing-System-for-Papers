"""模板管理系统

此模块实现了论文模板的完整管理功能，包括：
1. 基础模板管理
2. 模板生成
3. 模板优化
4. 学科模板管理
5. 版本控制
6. 反馈管理
7. 实时预览
8. 模板编辑
"""

# 基础模板
from .base.template import Template
from .base.template_element import TemplateElement
from .base.template_relation import TemplateRelation

# 模板生成
from .generation.parser import TemplateParser
from .generation.generator import TemplateGenerator
from .generation.validator import TemplateValidator
from .generation.adaptor import TemplateAdaptor

# 模板优化
from .optimization.evaluator import TemplateEvaluator
from .optimization.optimizer import TemplateOptimizer
from .optimization.monitor import TemplateMonitor

# 学科模板
from .discipline.analyzer import TemplateAnalyzer
from .discipline.template_lib import TemplateLibrary
from .discipline.mapper import TemplateMapper

# 版本控制
from .version_control import VersionControl

# 反馈管理
from .feedback import FeedbackManager, FeedbackData

# 实时预览
from .preview import PreviewManager

# 模板编辑
from .editor import TemplateEditor, EditSession, EditOperation

__all__ = [
    # 基础模板
    'Template',
    'TemplateElement',
    'TemplateRelation',
    
    # 模板生成
    'TemplateParser',
    'TemplateGenerator',
    'TemplateValidator',
    'TemplateAdaptor',
    
    # 模板优化
    'TemplateEvaluator',
    'TemplateOptimizer',
    'TemplateMonitor',
    
    # 学科模板
    'TemplateAnalyzer',
    'TemplateLibrary',
    'TemplateMapper',
    
    # 版本控制
    'VersionControl',
    
    # 反馈管理
    'FeedbackManager',
    'FeedbackData',
    
    # 实时预览
    'PreviewManager',
    
    # 模板编辑
    'TemplateEditor',
    'EditSession',
    'EditOperation'
] 