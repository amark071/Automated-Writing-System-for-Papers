from typing import Dict, List, Optional, Tuple
import os
import re
from datetime import datetime
import jieba
import jieba.analyse
from collections import defaultdict

class PolicyProcessor:
    """政策文件处理器，用于分析和处理政策文档"""
    
    def __init__(self, policy_dir: str):
        """
        初始化政策处理器
        
        Args:
            policy_dir: 政策文件所在目录
        """
        self.policy_dir = policy_dir
        self.policies = []  # 存储所有处理后的政策
        self.keyword_index = defaultdict(list)  # 关键词索引
        self.time_index = defaultdict(list)  # 时间索引
        
    def load_policies(self) -> None:
        """加载所有政策文件"""
        for root, _, files in os.walk(self.policy_dir):
            for file in files:
                if file.startswith('policy_') and file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            policy = self._parse_policy_file(content)
                            if policy:
                                self.policies.append(policy)
                    except Exception as e:
                        print(f"处理文件 {file} 时出错: {str(e)}")
        
        # 按时间排序
        self.policies.sort(key=lambda x: x['date'])
        
        # 建立索引
        self._build_indices()
    
    def _parse_policy_file(self, content: str) -> Optional[Dict]:
        """解析单个政策文件"""
        try:
            # 提取Excel信息部分
            excel_info = re.search(r'=== Excel信息 ===\n(.*?)\n=== 网页内容 ===', 
                                 content, re.DOTALL)
            if not excel_info:
                return None
                
            excel_info = excel_info.group(1)
            
            # 提取基本信息
            title = re.search(r'标题: (.*?)\n', excel_info)
            doc_number = re.search(r'文号: (.*?)\n', excel_info)
            date_str = re.search(r'成文日期: (.*?)\n', excel_info)
            
            if not all([title, date_str]):
                return None
                
            # 解析日期
            date_str = date_str.group(1).split()[0]  # 只取日期部分
            date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # 提取正文内容
            content_match = re.search(r'=== 网页内容 ===\n(.*)', content, re.DOTALL)
            if not content_match:
                return None
            
            main_content = content_match.group(1).strip()
            
            # 提取关键词（同时从标题和正文提取）
            title_text = title.group(1)
            title_keywords = jieba.analyse.extract_tags(title_text, topK=5)
            content_keywords = jieba.analyse.extract_tags(main_content, topK=10)
            
            # 合并关键词，保持顺序（标题关键词优先）
            keywords = list(dict.fromkeys(title_keywords + content_keywords))
            
            return {
                'title': title_text,
                'doc_number': doc_number.group(1) if doc_number else None,
                'date': date,
                'content': main_content,
                'keywords': keywords,
                'title_keywords': title_keywords,  # 单独保存标题关键词
            }
            
        except Exception as e:
            print(f"解析政策文件时出错: {str(e)}")
            return None
    
    def _calculate_relevance_score(self, policy: Dict, topic_keywords: List[str]) -> float:
        """
        计算政策与主题的相关性得分
        
        Args:
            policy: 政策信息字典
            topic_keywords: 主题关键词列表
            
        Returns:
            相关性得分
        """
        score = 0.0
        
        # 标题完全匹配（最高优先级）
        if any(topic in policy['title'] for topic in topic_keywords):
            score += 10.0
        
        # 标题关键词匹配（高优先级）
        title_matches = sum(1 for kw in policy['title_keywords'] if any(topic in kw or kw in topic for topic in topic_keywords))
        score += title_matches * 2.0
        
        # 内容关键词匹配
        content_matches = sum(1 for kw in policy['keywords'] if any(topic in kw or kw in topic for topic in topic_keywords))
        score += content_matches * 0.5
        
        return score
    
    def search_by_topic(self, topic: str, limit: int = 5) -> List[Dict]:
        """
        根据主题搜索相关政策
        
        Args:
            topic: 搜索主题
            limit: 返回结果数量限制
            
        Returns:
            相关政策列表
        """
        # 对主题进行分词
        topic_keywords = jieba.analyse.extract_tags(topic)
        
        # 计算每个政策的相关性得分
        scored_policies = []
        for policy in self.policies:
            score = self._calculate_relevance_score(policy, topic_keywords)
            if score > 0:  # 只保留有相关性的政策
                scored_policies.append((policy, score))
        
        # 按相关性得分降序排序
        scored_policies.sort(key=lambda x: (-x[1], x[0]['date']))  # 相关性相同时按日期排序
        
        # 返回得分最高的政策
        return [policy for policy, _ in scored_policies[:limit]]
    
    def get_policy_evolution(self, topic: str, start_year: int = 2012) -> List[Dict]:
        """获取某个主题的政策演变脉络"""
        relevant_policies = self.search_by_topic(topic, limit=None)
        
        # 筛选时间范围内的政策并按时间排序
        timeline_policies = [
            policy for policy in relevant_policies 
            if policy['date'].year >= start_year
        ]
        timeline_policies.sort(key=lambda x: x['date'])
        
        return timeline_policies
    
    def generate_policy_background(self, topic: str) -> str:
        """生成政策背景描述"""
        # 获取政策演变脉络
        policy_timeline = self.get_policy_evolution(topic)
        
        if not policy_timeline:
            return f"近年来，国家尚未出台直接针对{topic}的专门政策文件。"
        
        # 生成背景描述
        latest_policies = policy_timeline[-3:]  # 最近的3个政策
        early_policies = policy_timeline[:-3]  # 早期政策
        
        background = f"近年来，国家高度重视{topic}相关工作。"
        
        # 添加早期政策概述
        if early_policies:
            years = sorted(set(p['date'].year for p in early_policies))
            background += f"自{years[0]}年以来，"
            background += f"先后出台了{len(early_policies)}项相关政策文件，"
            background += "为该领域发展提供了政策指引。"
        
        # 添加最新政策详述
        if latest_policies:
            background += "特别是近期，"
            for i, policy in enumerate(latest_policies):
                if i > 0:
                    background += "；" if i < len(latest_policies)-1 else "。"
                year = policy['date'].year
                background += f"{year}年发布的《{policy['title']}》"
        
        return background 