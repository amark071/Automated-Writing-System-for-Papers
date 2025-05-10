"""
模板监控器模块
用于监控论文模板的使用情况和性能指标
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from ...base.template import Template

@dataclass
class MonitoringMetrics:
    """监控指标数据类"""
    template_id: str
    usage_count: int
    error_count: int
    average_score: float
    last_used: datetime
    performance_metrics: dict[str, float]

class TemplateMonitor:
    """模板监控器类"""
    
    def __init__(self):
        """初始化监控器"""
        self.logger = logging.getLogger(__name__)
        self.metrics: dict[str, MonitoringMetrics] = {}
        
    def start_monitoring(self, template: Template) -> bool:
        """开始监控模板
        
        Args:
            template: 待监控的模板
            
        Returns:
            bool: 是否成功开始监控
        """
        try:
            if template.template_id not in self.metrics:
                self.metrics[template.template_id] = MonitoringMetrics(
                    template_id=template.template_id,
                    usage_count=0,
                    error_count=0,
                    average_score=0.0,
                    last_used=datetime.now(),
                    performance_metrics={}
                )
                self.logger.info(f"Started monitoring template: {template.template_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {str(e)}")
            return False
            
    def stop_monitoring(self, template_id: str) -> bool:
        """停止监控模板
        
        Args:
            template_id: 模板ID
            
        Returns:
            bool: 是否成功停止监控
        """
        try:
            if template_id in self.metrics:
                del self.metrics[template_id]
                self.logger.info(f"Stopped monitoring template: {template_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to stop monitoring: {str(e)}")
            return False
            
    def record_usage(self, template_id: str) -> bool:
        """记录模板使用情况
        
        Args:
            template_id: 模板ID
            
        Returns:
            bool: 是否成功记录
        """
        try:
            if template_id in self.metrics:
                metrics = self.metrics[template_id]
                metrics.usage_count += 1
                metrics.last_used = datetime.now()
                self.logger.info(f"Recorded usage for template: {template_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to record usage: {str(e)}")
            return False
            
    def record_error(self, template_id: str) -> bool:
        """记录模板错误
        
        Args:
            template_id: 模板ID
            
        Returns:
            bool: 是否成功记录
        """
        try:
            if template_id in self.metrics:
                metrics = self.metrics[template_id]
                metrics.error_count += 1
                self.logger.info(f"Recorded error for template: {template_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to record error: {str(e)}")
            return False
            
    def update_score(self, template_id: str, score: float) -> bool:
        """更新模板评分
        
        Args:
            template_id: 模板ID
            score: 新的评分
            
        Returns:
            bool: 是否成功更新
        """
        try:
            if template_id in self.metrics:
                metrics = self.metrics[template_id]
                old_score = metrics.average_score
                usage_count = metrics.usage_count
                
                # 计算新的平均分
                metrics.average_score = (old_score * usage_count + score) / (usage_count + 1)
                self.logger.info(f"Updated score for template: {template_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to update score: {str(e)}")
            return False
            
    def update_performance_metrics(self,
                                 template_id: str,
                                 metrics: dict[str, float]) -> bool:
        """更新性能指标
        
        Args:
            template_id: 模板ID
            metrics: 性能指标
            
        Returns:
            bool: 是否成功更新
        """
        try:
            if template_id in self.metrics:
                self.metrics[template_id].performance_metrics.update(metrics)
                self.logger.info(f"Updated performance metrics for template: {template_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to update performance metrics: {str(e)}")
            return False
            
    def get_metrics(self, template_id: str) -> MonitoringMetrics | None:
        """获取监控指标
        
        Args:
            template_id: 模板ID
            
        Returns:
            MonitoringMetrics | None: 监控指标
        """
        return self.metrics.get(template_id)
        
    def get_all_metrics(self) -> dict[str, MonitoringMetrics]:
        """获取所有监控指标
        
        Returns:
            dict[str, MonitoringMetrics]: 所有监控指标
        """
        return self.metrics.copy() 