"""Template Feedback Management Module

This module implements the user feedback functionality for paper templates, including feedback collection, analysis and processing.
"""

from typing import Dict, List, Any, Optional
import logging
import json
import os
from datetime import datetime
from dataclasses import dataclass
from .base.template import Template
import uuid

@dataclass
class FeedbackItem:
    """Feedback Item Data Class"""
    feedback_id: str
    template_id: str
    user_id: str
    timestamp: datetime
    category: str
    content: str
    rating: int
    status: str
    tags: List[str] = None
    response: Optional[str] = None
    response_time: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'feedback_id': self.feedback_id,
            'template_id': self.template_id,
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat(),
            'category': self.category,
            'content': self.content,
            'rating': self.rating,
            'status': self.status,
            'tags': self.tags or [],
            'response': self.response,
            'response_time': self.response_time.isoformat() if self.response_time else None,
            'metadata': self.metadata or {}
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FeedbackItem':
        """从字典创建实例"""
        if 'timestamp' in data:
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        if 'response_time' in data and data['response_time']:
            data['response_time'] = datetime.fromisoformat(data['response_time'])
        return cls(**data)

class TemplateFeedbackManager:
    """Template Feedback Manager Class"""
    
    VALID_CATEGORIES = ['usability', 'content', 'structure', 'format', 'other']
    
    def __init__(self, storage_dir: str = "data/template_feedback"):
        """Initialize feedback manager
        
        Args:
            storage_dir: Feedback storage directory
        """
        self.logger = logging.getLogger(__name__)
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
    def submit_feedback(self,
                       template_id: str,
                       category: str,
                       rating: int,
                       comment: str = "",
                       tags: List[str] = None,
                       metadata: Dict[str, Any] = None) -> str:
        """Submit feedback for a template
        
        Args:
            template_id: Template ID
            category: Feedback category
            rating: Rating (1-5)
            comment: Comment text
            tags: List of tags
            metadata: Additional metadata
            
        Returns:
            str: Feedback ID
        """
        try:
            # 验证输入
            if not template_id:
                raise ValueError("Template ID cannot be empty")
                
            valid_categories = ["usability", "content", "structure", "format", "other", "bug"]
            if category not in valid_categories:
                raise ValueError(f"Invalid category. Must be one of: {', '.join(valid_categories)}")
                
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValueError("Rating must be an integer between 1 and 5")
                
            # 生成反馈ID
            feedback_id = str(uuid.uuid4())
            
            # 创建反馈数据
            feedback_data = {
                'feedback_id': feedback_id,
                'template_id': template_id,
                'category': category,
                'rating': rating,
                'content': comment,
                'tags': tags or [],
                'metadata': metadata or {},
                'submission_time': datetime.now().isoformat()
            }
            
            # 保存反馈
            feedback_path = os.path.join(self.storage_dir, f"{feedback_id}.json")
            with open(feedback_path, 'w', encoding='utf-8') as f:
                json.dump(feedback_data, f, ensure_ascii=False, indent=2)
                
            return feedback_id
            
        except Exception as e:
            self.logger.error(f"Error submitting feedback: {e}")
            raise
            
    def get_feedback(self, feedback_id: str) -> Dict[str, Any]:
        """Get feedback by ID
        
        Args:
            feedback_id: Feedback ID
            
        Returns:
            Dict[str, Any]: Feedback data
        """
        try:
            if not feedback_id:
                raise ValueError("Feedback ID cannot be empty")
                
            # 获取反馈文件路径
            feedback_file = os.path.join(self.storage_dir, f"{feedback_id}.json")
            
            if not os.path.exists(feedback_file):
                raise ValueError(f"Feedback {feedback_id} not found")
                
            # 读取反馈
            with open(feedback_file, 'r', encoding='utf-8') as f:
                feedback_data = json.load(f)
                
            # 确保字段名称一致
            feedback_data['id'] = feedback_data['feedback_id']
            feedback_data['comment'] = feedback_data['content']
                
            return feedback_data
            
        except Exception as e:
            self.logger.error(f"Error getting feedback: {e}")
            raise
            
    def list_feedback(self,
                     template_id: str = None,
                     category: str = None,
                     tags: List[str] = None) -> List[Dict[str, Any]]:
        """List feedback
        
        Args:
            template_id: Optional template ID to filter by
            category: Optional category to filter by
            tags: Optional list of tags to filter by
            
        Returns:
            List[Dict[str, Any]]: List of feedback dictionaries
        """
        try:
            feedback_list = []
            
            # 遍历所有反馈文件
            for filename in os.listdir(self.storage_dir):
                if not filename.endswith('.json'):
                    continue
                    
                feedback_path = os.path.join(self.storage_dir, filename)
                with open(feedback_path, 'r', encoding='utf-8') as f:
                    feedback_data = json.load(f)
                    
                # 应用过滤器
                if template_id and feedback_data['template_id'] != template_id:
                    continue
                    
                if category and feedback_data['category'] != category:
                    continue
                    
                if tags:
                    feedback_tags = set(feedback_data.get('tags', []))
                    if not all(tag in feedback_tags for tag in tags):
                        continue
                        
                feedback_list.append(feedback_data)
                
            return feedback_list
            
        except Exception as e:
            self.logger.error(f"Error listing feedback: {e}")
            raise
            
    def respond_to_feedback(self,
                          feedback_id: str,
                          response: str) -> None:
        """Respond to feedback
        
        Args:
            feedback_id: Feedback ID
            response: Response text
        """
        try:
            if not feedback_id:
                raise ValueError("Feedback ID cannot be empty")
            if not response:
                raise ValueError("Response cannot be empty")
                
            # 获取反馈文件路径
            feedback_file = os.path.join(self.storage_dir, f"{feedback_id}.json")
            
            if not os.path.exists(feedback_file):
                raise KeyError(f"Feedback {feedback_id} not found")
                
            # 读取反馈
            with open(feedback_file, 'r', encoding='utf-8') as f:
                feedback_data = json.load(f)
                
            # 更新响应
            feedback_data['response'] = response
            feedback_data['response_time'] = datetime.now().isoformat()
            feedback_data['status'] = 'responded'
            
            # 保存更新的反馈
            with open(feedback_file, 'w', encoding='utf-8') as f:
                json.dump(feedback_data, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"Responded to feedback {feedback_id}")
            
        except Exception as e:
            self.logger.error(f"Error responding to feedback: {e}")
            raise
            
    def analyze_feedback(self,
                        template_id: str,
                        start_time: str = None,
                        end_time: str = None) -> Dict[str, Any]:
        """Analyze feedback
        
        Args:
            template_id: Template ID
            start_time: Optional start time in ISO format
            end_time: Optional end time in ISO format
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        try:
            if not template_id:
                raise ValueError("Template ID cannot be empty")
                
            # 获取所有反馈
            feedback_list = self.list_feedback(template_id=template_id)
            
            # 过滤时间范围
            if start_time or end_time:
                filtered_list = []
                for feedback in feedback_list:
                    submission_time = feedback['submission_time']
                    if start_time and submission_time < start_time:
                        continue
                    if end_time and submission_time > end_time:
                        continue
                    filtered_list.append(feedback)
                feedback_list = filtered_list
            
            if not feedback_list:
                return {
                    'average_rating': 0.0,
                    'total_feedback': 0,
                    'category_ratings': {},
                    'category_distribution': {},
                    'rating_distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                    'tag_frequency': {}
                }
                
            # 计算统计数据
            total_rating = 0
            category_ratings = {}
            category_distribution = {}
            rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            tag_frequency = {}
            
            for feedback in feedback_list:
                # 更新总评分
                total_rating += feedback['rating']
                
                # 更新分类评分
                category = feedback['category']
                if category not in category_ratings:
                    category_ratings[category] = {'total': 0, 'count': 0}
                    category_distribution[category] = 0
                category_ratings[category]['total'] += feedback['rating']
                category_ratings[category]['count'] += 1
                category_distribution[category] += 1
                
                # 更新评分分布
                rating = feedback['rating']
                rating_distribution[rating] += 1
                
                # 更新标签频率
                for tag in feedback.get('tags', []):
                    if tag not in tag_frequency:
                        tag_frequency[tag] = 0
                    tag_frequency[tag] += 1
                    
            # 计算平均评分
            total_feedback = len(feedback_list)
            average_rating = total_rating / total_feedback if total_feedback > 0 else 0.0
            
            # 计算分类平均评分
            for category in category_ratings:
                category_ratings[category]['average'] = (
                    category_ratings[category]['total'] / category_ratings[category]['count']
                )
                
            return {
                'average_rating': round(average_rating, 2),
                'total_feedback': total_feedback,
                'category_ratings': category_ratings,
                'category_distribution': category_distribution,
                'rating_distribution': rating_distribution,
                'tag_frequency': tag_frequency
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing feedback: {e}")
            raise
            
    def get_feedback_statistics(self, template_id: str) -> Dict[str, Any]:
        """Get feedback statistics
        
        Args:
            template_id: Template ID
            
        Returns:
            Dict[str, Any]: Statistics data
        """
        return self.analyze_feedback(template_id)
            
    def delete_feedback(self, feedback_id: str) -> None:
        """Delete feedback
        
        Args:
            feedback_id: Feedback ID
        """
        try:
            if not feedback_id:
                raise ValueError("Feedback ID cannot be empty")
                
            # 获取反馈文件路径
            feedback_file = os.path.join(self.storage_dir, f"{feedback_id}.json")
            
            if not os.path.exists(feedback_file):
                raise ValueError(f"Feedback {feedback_id} not found")
                
            # 删除反馈文件
            os.remove(feedback_file)
            self.logger.info(f"Deleted feedback {feedback_id}")
            
        except Exception as e:
            self.logger.error(f"Error deleting feedback: {e}")
            raise
            
    def import_feedback(self, feedback_data: List[Dict[str, Any]]) -> List[str]:
        """Import feedback from a list of dictionaries
        
        Args:
            feedback_data: List of feedback dictionaries
            
        Returns:
            List[str]: List of imported feedback IDs
        """
        if not isinstance(feedback_data, list):
            raise ValueError("Feedback data must be a list")
            
        feedback_ids = []
        for feedback in feedback_data:
            if not isinstance(feedback, dict):
                raise ValueError("Each feedback item must be a dictionary")
                
            # 验证必需字段
            required_fields = ['template_id', 'category', 'rating']
            for field in required_fields:
                if field not in feedback:
                    raise ValueError(f"Missing required field: {field}")
                    
            # 获取内容
            content = feedback.get('content', feedback.get('comment', ''))
            
            # 提交反馈
            feedback_id = self.submit_feedback(
                template_id=feedback['template_id'],
                category=feedback['category'],
                rating=feedback['rating'],
                comment=content,
                tags=feedback.get('tags', []),
                metadata=feedback.get('metadata', {})
            )
            feedback_ids.append(feedback_id)
            
        return feedback_ids
        
    def export_feedback(self, template_id: str = None) -> List[Dict[str, Any]]:
        """Export feedback as a list of dictionaries
        
        Args:
            template_id: Optional template ID to filter by
            
        Returns:
            List[Dict[str, Any]]: List of feedback dictionaries
        """
        feedback_list = self.list_feedback(template_id=template_id)
        
        # 转换字段名称
        exported_feedback = []
        for feedback in feedback_list:
            exported_item = {
                'feedback_id': feedback['feedback_id'],
                'template_id': feedback['template_id'],
                'category': feedback['category'],
                'rating': feedback['rating'],
                'comment': feedback['content'],
                'tags': feedback.get('tags', []),
                'metadata': feedback.get('metadata', {}),
                'submission_time': feedback['submission_time']
            }
            exported_feedback.append(exported_item)
            
        return exported_feedback 