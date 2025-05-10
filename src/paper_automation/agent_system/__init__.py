"""
智能代理层，负责论文自动化写作系统的核心功能实现。

主要组件：
1. 论文代理系统 (paper_agent)
   - ContentAgent: 内容代理，负责协调各个章节代理生成论文内容
   - IntroductionAgent: 引言代理，负责生成论文的引言部分
   - LiteratureAgent: 文献综述代理，负责生成论文的文献综述部分
   - TheoryAgent: 理论框架代理，负责生成论文的理论框架部分
   - MethodAgent: 研究方法代理，负责生成论文的研究方法部分
   - EmpiricalAgent: 实证分析代理，负责生成论文的实证分析部分
   - DiscussionAgent: 讨论代理，负责生成论文的讨论部分
   - ConclusionAgent: 结论代理，负责生成论文的结论部分

2. 知识管理系统 (knowledge_management)
   - 文献管理
     * LiteratureCollector: 文献收集器
     * LiteratureParser: 文献解析器
     * LiteratureClassifier: 文献分类器
   - 知识图谱
     * KnowledgeGraphBuilder: 知识图谱构建器
     * KnowledgeGraphAnalyzer: 知识图谱分析器
     * KnowledgeGraphOptimizer: 知识图谱优化器
   - 规则引擎
     * RuleEngine: 规则引擎核心
     * RuleDefiner: 规则定义器
     * RuleApplier: 规则应用器
     * RuleValidator: 规则验证器

3. 模板管理系统 (template_management)
   - 基础模板
     * Template: 模板类
     * TemplateElement: 模板元素
     * TemplateRelation: 模板关系
   - 模板生成
     * TemplateParser: 模板解析器
     * TemplateGenerator: 模板生成器
     * TemplateValidator: 模板验证器
     * TemplateAdaptor: 模板适配器
   - 模板优化
     * TemplateEvaluator: 模板评估器
     * TemplateOptimizer: 模板优化器
     * PerformanceMonitor: 性能监控器
"""

from .paper_agent import (
    ContentAgent,
    IntroductionAgent,
    LiteratureAgent,
    TheoryAgent,
    MethodAgent,
    EmpiricalAgent,
    DiscussionAgent,
    ConclusionAgent
)

from .knowledge_management.literature import (
    LiteratureCollector,
    LiteratureParser,
    LiteratureClassifier
)

from .knowledge_management.knowledge_graph import (
    KnowledgeGraphBuilder,
    KnowledgeGraphAnalyzer,
    KnowledgeGraphOptimizer
)

from .knowledge_management.rules import (
    RuleEngine,
    RuleDefiner,
    RuleApplier,
    RuleValidator
)

from .template_management.base import (
    Template,
    TemplateElement,
    TemplateRelation
)

from .template_management.generation import (
    TemplateParser,
    TemplateGenerator,
    TemplateValidator,
    TemplateAdaptor
)

from .template_management.optimization import (
    TemplateEvaluator,
    TemplateOptimizer,
    PerformanceMonitor
)

__all__ = [
    # 论文代理系统
    'ContentAgent',
    'IntroductionAgent',
    'LiteratureAgent',
    'TheoryAgent',
    'MethodAgent',
    'EmpiricalAgent',
    'DiscussionAgent',
    'ConclusionAgent',
    
    # 知识管理系统 - 文献管理
    'LiteratureCollector',
    'LiteratureParser',
    'LiteratureClassifier',
    
    # 知识管理系统 - 知识图谱
    'KnowledgeGraphBuilder',
    'KnowledgeGraphAnalyzer',
    'KnowledgeGraphOptimizer',
    
    # 知识管理系统 - 规则引擎
    'RuleEngine',
    'RuleDefiner',
    'RuleApplier',
    'RuleValidator',
    
    # 模板管理系统 - 基础模板
    'Template',
    'TemplateElement',
    'TemplateRelation',
    
    # 模板管理系统 - 模板生成
    'TemplateParser',
    'TemplateGenerator',
    'TemplateValidator',
    'TemplateAdaptor',
    
    # 模板管理系统 - 模板优化
    'TemplateEvaluator',
    'TemplateOptimizer',
    'PerformanceMonitor'
] 