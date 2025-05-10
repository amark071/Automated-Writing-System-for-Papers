"""
模板评估器模块
用于评估论文模板的质量和适用性
"""

import logging
from dataclasses import dataclass
from ...base.template import Template

@dataclass
class EvaluationResult:
    """评估结果数据类"""
    template_id: str
    score: float
    metrics: dict[str, float]
    feedback: list[str]

class TemplateEvaluator:
    """模板评估器类"""
    
    def __init__(self):
        """初始化评估器"""
        self.logger = logging.getLogger(__name__)
        self.metrics: dict[str, float] = {}
        
    def evaluate_template(self, template: Template) -> EvaluationResult | None:
        """评估模板
        
        Args:
            template: 待评估的模板
            
        Returns:
            EvaluationResult | None: 评估结果
        """
        try:
            # 计算各项指标
            self.metrics = {
                'content_quality': self._evaluate_content(template),
                'style_consistency': self._evaluate_style(template),
                'structure_quality': self._evaluate_structure(template),
                'metadata_completeness': self._evaluate_metadata(template)
            }
            
            # 计算总分
            score = sum(self.metrics.values()) / len(self.metrics)
            
            # 生成反馈
            feedback = self._generate_feedback()
            
            return EvaluationResult(
                template_id=template.template_id,
                score=score,
                metrics=self.metrics,
                feedback=feedback
            )
            
        except Exception as e:
            self.logger.error(f"Failed to evaluate template: {str(e)}")
            return None
            
    def _evaluate_content(self, template: Template) -> float:
        """评估内容质量
        
        Args:
            template: 模板对象
            
        Returns:
            float: 内容质量得分
        """
        score = 0.0
        content = template.content
        
        # 评估内容完整性
        if content and isinstance(content, dict):
            required_sections = {'abstract', 'introduction', 'methodology', 'results', 'conclusion'}
            existing_sections = set(content.keys())
            completeness = len(required_sections & existing_sections) / len(required_sections)
            score += completeness * 0.5
            
        # 评估内容长度
        total_length = sum(len(str(v)) for v in content.values())
        if total_length > 1000:
            score += 0.3
        elif total_length > 500:
            score += 0.2
            
        # 评估格式规范
        if all(isinstance(v, (str, dict)) for v in content.values()):
            score += 0.2
            
        return min(score, 1.0)
        
    def _evaluate_style(self, template: Template) -> float:
        """评估样式一致性
        
        Args:
            template: 模板对象
            
        Returns:
            float: 样式一致性得分
        """
        score = 0.0
        style = template.style
        
        # 评估样式完整性
        if style and isinstance(style, dict):
            required_styles = {'font', 'color', 'spacing', 'alignment'}
            existing_styles = set(style.keys())
            completeness = len(required_styles & existing_styles) / len(required_styles)
            score += completeness * 0.4
            
        # 评估样式一致性
        if all(isinstance(v, (str, int, float, dict)) for v in style.values()):
            score += 0.3
            
        # 评估样式规范性
        if all(k.islower() and '_' in k for k in style.keys()):
            score += 0.3
            
        return min(score, 1.0)
        
    def _evaluate_structure(self, template: Template) -> float:
        """评估结构质量
        
        Args:
            template: 模板对象
            
        Returns:
            float: 结构质量得分
        """
        score = 0.0
        content = template.content
        
        # 评估层次结构
        if content and isinstance(content, dict):
            has_sections = any(isinstance(v, dict) for v in content.values())
            if has_sections:
                score += 0.5
                
            # 评估章节顺序
            sections = list(content.keys())
            if sections == sorted(sections):
                score += 0.3
                
        # 评估结构完整性
        if template.metadata.get('toc'):
            score += 0.2
            
        return min(score, 1.0)
        
    def _evaluate_metadata(self, template: Template) -> float:
        """评估元数据完整性
        
        Args:
            template: 模板对象
            
        Returns:
            float: 元数据完整性得分
        """
        score = 0.0
        metadata = template.metadata
        
        # 评估必要字段
        if metadata and isinstance(metadata, dict):
            required_fields = {'author', 'date', 'version', 'keywords'}
            existing_fields = set(metadata.keys())
            completeness = len(required_fields & existing_fields) / len(required_fields)
            score += completeness * 0.6
            
        # 评估字段格式
        if all(isinstance(v, (str, int, float)) for v in metadata.values()):
            score += 0.2
            
        # 评估更新时间
        if metadata.get('last_updated'):
            score += 0.2
            
        return min(score, 1.0)
        
    def _generate_feedback(self) -> list[str]:
        """生成评估反馈
        
        Returns:
            list[str]: 反馈列表
        """
        feedback = []
        
        # 内容质量反馈
        content_score = self.metrics.get('content_quality', 0)
        if content_score < 0.6:
            feedback.append("内容质量需要提高，建议补充必要章节")
        elif content_score < 0.8:
            feedback.append("内容质量良好，可以考虑进一步完善")
            
        # 样式一致性反馈
        style_score = self.metrics.get('style_consistency', 0)
        if style_score < 0.6:
            feedback.append("样式一致性较差，需要统一格式")
        elif style_score < 0.8:
            feedback.append("样式基本统一，建议检查细节")
            
        # 结构质量反馈
        structure_score = self.metrics.get('structure_quality', 0)
        if structure_score < 0.6:
            feedback.append("文档结构需要优化，建议调整章节顺序")
        elif structure_score < 0.8:
            feedback.append("文档结构合理，可以考虑添加目录")
            
        # 元数据完整性反馈
        metadata_score = self.metrics.get('metadata_completeness', 0)
        if metadata_score < 0.6:
            feedback.append("元数据不完整，请补充必要信息")
        elif metadata_score < 0.8:
            feedback.append("元数据基本完整，建议更新时间戳")
            
        return feedback 