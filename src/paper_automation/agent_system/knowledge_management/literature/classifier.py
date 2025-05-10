"""文献分类器模块
"""
from typing import Dict, List, Any, Optional
import logging

class LiteratureClassifier:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def classify_by_discipline(self, paper_data: Dict[str, Any]) -> str:
        """根据论文数据进行学科分类"""
        try:
            if not paper_data or not isinstance(paper_data, dict):
                raise ValueError("Invalid paper data")
                
            # 简单的分类逻辑
            keywords = paper_data.get("keywords", [])
            title = paper_data.get("title", "").lower()
            abstract = paper_data.get("abstract", "").lower()
            
            # 计算机科学相关关键词
            cs_keywords = ["computer science", "machine learning", "artificial intelligence",
                         "deep learning", "neural networks", "computer vision"]
                         
            # 检查是否包含计算机科学关键词
            for keyword in cs_keywords:
                if (keyword in keywords or 
                    keyword in title or 
                    keyword in abstract):
                    return "Computer Science"
                    
            return "Unknown"
            
        except Exception as e:
            self.logger.error(f"Error in discipline classification: {e}")
            raise
            
    def classify_by_topic(self, paper_data: Dict[str, Any]) -> str:
        """根据论文数据进行主题分类"""
        try:
            if not paper_data or not isinstance(paper_data, dict):
                raise ValueError("Invalid paper data")
                
            # 简单的主题分类逻辑
            keywords = paper_data.get("keywords", [])
            title = paper_data.get("title", "").lower()
            abstract = paper_data.get("abstract", "").lower()
            
            # 深度学习相关关键词
            dl_keywords = ["deep learning", "neural networks", "cnn", "rnn", "lstm"]
            
            # 检查是否包含深度学习关键词
            for keyword in dl_keywords:
                if (keyword in keywords or 
                    keyword in title or 
                    keyword in abstract):
                    return "Deep Learning"
                    
            return "Unknown"
            
        except Exception as e:
            self.logger.error(f"Error in topic classification: {e}")
            raise
            
    def classify_by_type(self, paper_data: Dict[str, Any]) -> str:
        """根据论文数据进行类型分类"""
        try:
            if not paper_data or not isinstance(paper_data, dict):
                raise ValueError("Invalid paper data")
                
            # 获取论文类型
            paper_type = paper_data.get("type", "").lower()
            title = paper_data.get("title", "").lower()
            abstract = paper_data.get("abstract", "").lower()
            
            # 检查是否为综述论文
            review_keywords = ["review", "survey", "overview"]
            for keyword in review_keywords:
                if (keyword == paper_type or 
                    keyword in title or 
                    keyword in abstract):
                    return "Review"
                    
            return "Research"
            
        except Exception as e:
            self.logger.error(f"Error in type classification: {e}")
            raise
            
    def classify_paper(self, paper_data: Dict[str, Any]) -> Dict[str, str]:
        """对论文进行多重分类
        
        Args:
            paper_data (Dict[str, Any]): 论文数据，必须包含 title 和 abstract 字段
            
        Returns:
            Dict[str, str]: 分类结果，包含 discipline、topic 和 type
            
        Raises:
            ValueError: 当输入数据无效或缺少必要字段时
        """
        if not paper_data or not isinstance(paper_data, dict):
            raise ValueError("Invalid paper data")
            
        if "title" not in paper_data or "abstract" not in paper_data:
            raise ValueError("Paper data must contain title and abstract")
            
        return {
            "discipline": self.classify_by_discipline(paper_data),
            "topic": self.classify_by_topic(paper_data),
            "type": self.classify_by_type(paper_data)
        }
        
    def classify_with_confidence(self, paper_data: Dict[str, Any]) -> Dict[str, Any]:
        """对论文进行分类并返回置信度
        
        Args:
            paper_data (Dict[str, Any]): 论文数据
            
        Returns:
            Dict[str, Any]: 分类结果和置信度
        """
        classification = self.classify_paper(paper_data)
        
        # 简单的置信度计算
        confidence = 0.8 if classification["discipline"] != "Unknown" else 0.5
        
        return {
            "classification": classification,
            "confidence": confidence
        } 