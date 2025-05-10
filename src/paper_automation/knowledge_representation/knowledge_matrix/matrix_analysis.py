"""知识矩阵分析模块
"""

from typing import Dict, List, Optional, Any
import numpy as np
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

class KnowledgeMatrixAnalysis:
    """知识矩阵分析类"""
    
    def __init__(self):
        """初始化知识矩阵分析类"""
        pass
    
    def extract_features(self, matrix: np.ndarray) -> Dict[str, Any]:
        """提取矩阵特征
        
        Args:
            matrix: 输入矩阵
            
        Returns:
            包含特征值、特征向量和奇异值的字典
            
        Raises:
            ValueError: 当输入矩阵为None时
        """
        if matrix is None:
            raise ValueError('Input matrix cannot be None')
            
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        singular_values = np.linalg.svd(matrix, compute_uv=False)
        
        return {
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'singular_values': singular_values
        }
    
    def cluster_features(self, features: Dict[str, Any]) -> Dict[str, List[int]]:
        """聚类特征
        
        Args:
            features: 特征字典
            
        Returns:
            特征聚类结果
            
        Raises:
            ValueError: 当特征字典为None时
        """
        if features is None:
            raise ValueError('Features cannot be None')
            
        eigenvalues = np.real(features['eigenvalues'])
        kmeans = KMeans(n_clusters=min(3, len(eigenvalues)))
        labels = kmeans.fit_predict(eigenvalues.reshape(-1, 1))
        
        clusters = {}
        for i, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(i)
            
        return clusters
    
    def feature_importance(self, features: Dict[str, Any]) -> Dict[str, float]:
        """计算特征重要性
        
        Args:
            features: 特征字典
            
        Returns:
            特征重要性字典
            
        Raises:
            ValueError: 当特征字典为None时
        """
        if features is None:
            raise ValueError('Features cannot be None')
            
        eigenvalues = np.abs(features['eigenvalues'])
        total = np.sum(eigenvalues)
        
        importance = {}
        for i, value in enumerate(eigenvalues):
            importance[f'feature_{i}'] = value / total if total > 0 else 0
            
        return importance
    
    def extract_relations(self, matrix: np.ndarray) -> Dict[str, Any]:
        """提取矩阵关系
        
        Args:
            matrix: 输入矩阵
            
        Returns:
            包含直接关系、间接关系和关系强度的字典
            
        Raises:
            ValueError: 当输入矩阵为None时
        """
        if matrix is None:
            raise ValueError('Input matrix cannot be None')
            
        direct_relations = np.nonzero(matrix)
        indirect_relations = np.nonzero(np.linalg.matrix_power(matrix, 2))
        strength = np.abs(matrix[direct_relations])
        
        return {
            'direct_relations': direct_relations,
            'indirect_relations': indirect_relations,
            'strength': strength
        }
    
    def cluster_relations(self, relations: Dict[str, Any]) -> Dict[str, List[int]]:
        """聚类关系
        
        Args:
            relations: 关系字典
            
        Returns:
            关系聚类结果
            
        Raises:
            ValueError: 当关系字典为None时
        """
        if relations is None:
            raise ValueError('Relations cannot be None')
            
        strength = relations['strength']
        kmeans = KMeans(n_clusters=min(3, len(strength)))
        labels = kmeans.fit_predict(strength.reshape(-1, 1))
        
        clusters = {}
        for i, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(i)
            
        return clusters
    
    def relation_importance(self, relations: Dict[str, Any]) -> Dict[str, float]:
        """计算关系重要性
        
        Args:
            relations: 关系字典
            
        Returns:
            关系重要性字典
            
        Raises:
            ValueError: 当关系字典为None时
        """
        if relations is None:
            raise ValueError('Relations cannot be None')
            
        strength = relations['strength']
        total = np.sum(strength)
        
        importance = {}
        for i, value in enumerate(strength):
            importance[f'relation_{i}'] = value / total if total > 0 else 0
            
        return importance
    
    def extract_patterns(self, matrix: np.ndarray) -> Dict[str, Any]:
        """提取矩阵模式
        
        Args:
            matrix: 输入矩阵
            
        Returns:
            包含频繁模式、稀有模式、时间模式、组件和方差比的字典
            
        Raises:
            ValueError: 当输入矩阵为None时
        """
        if matrix is None:
            raise ValueError('Input matrix cannot be None')
            
        pca = PCA()
        transformed = pca.fit_transform(matrix)
        
        frequent_patterns = np.where(pca.explained_variance_ratio_ > 0.1)[0]
        rare_patterns = np.where(pca.explained_variance_ratio_ < 0.01)[0]
        temporal_patterns = np.diff(matrix, axis=0)
        
        return {
            'frequent_patterns': frequent_patterns,
            'rare_patterns': rare_patterns,
            'temporal_patterns': temporal_patterns,
            'components': pca.components_,
            'variance_ratio': pca.explained_variance_ratio_
        }
    
    def cluster_patterns(self, patterns: Dict[str, Any]) -> Dict[str, List[int]]:
        """聚类模式
        
        Args:
            patterns: 模式字典
            
        Returns:
            模式聚类结果
            
        Raises:
            ValueError: 当模式字典为None时
        """
        if patterns is None:
            raise ValueError('Patterns cannot be None')
            
        components = patterns['components']
        kmeans = KMeans(n_clusters=min(3, len(components)))
        labels = kmeans.fit_predict(components)
        
        clusters = {}
        for i, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(i)
            
        return clusters
    
    def pattern_importance(self, patterns: Dict[str, Any]) -> Dict[str, float]:
        """计算模式重要性
        
        Args:
            patterns: 模式字典
            
        Returns:
            模式重要性字典
            
        Raises:
            ValueError: 当模式字典为None时
        """
        if patterns is None:
            raise ValueError('Patterns cannot be None')
            
        variance_ratio = patterns['variance_ratio']
        
        importance = {}
        for i, value in enumerate(variance_ratio):
            importance[f'pattern_{i}'] = value
            
        return importance
    
    def predict_patterns(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        """预测模式
        
        Args:
            patterns: 模式字典
            
        Returns:
            包含下一模式和置信度的字典
            
        Raises:
            ValueError: 当模式字典为None时
        """
        if patterns is None:
            raise ValueError('Patterns cannot be None')
            
        temporal_patterns = patterns['temporal_patterns']
        trend = np.mean(temporal_patterns, axis=0)
        confidence = 1.0 / (1.0 + np.std(temporal_patterns, axis=0))
        
        return {
            'next_patterns': trend,
            'confidence': confidence
        }
    
    def calculate_pattern_confidence(self, patterns: Dict[str, Any]) -> np.ndarray:
        """计算模式置信度
        
        Args:
            patterns: 模式字典
            
        Returns:
            模式置信度数组
            
        Raises:
            ValueError: 当模式字典为None时
        """
        if patterns is None:
            raise ValueError('Patterns cannot be None')
            
        variance_ratio = patterns['variance_ratio']
        temporal_patterns = patterns['temporal_patterns']
        temporal_stability = 1.0 / (1.0 + np.std(temporal_patterns, axis=0))
        
        confidence = np.zeros_like(variance_ratio)
        
        frequent_patterns = patterns['frequent_patterns']
        confidence[frequent_patterns] = 0.7 * variance_ratio[frequent_patterns] + 0.3 * temporal_stability[frequent_patterns]
        
        rare_patterns = patterns['rare_patterns']
        confidence[rare_patterns] = 0.3 * variance_ratio[rare_patterns] + 0.1 * temporal_stability[rare_patterns]
        
        confidence = confidence / np.sum(confidence)
        
        return confidence 