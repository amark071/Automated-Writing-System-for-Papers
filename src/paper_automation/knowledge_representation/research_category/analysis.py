"""研究范畴矩阵分析模块"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from scipy import sparse
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from .base_representation import ResearchCategoryBaseRepresentation
from .advanced_representation import ResearchCategoryAdvancedRepresentation

class ResearchCategoryMatrixAnalysis:
    """研究范畴矩阵分析类"""
    
    def __init__(self, n_components: int = 2, random_state: int = 42):
        """初始化矩阵分析类
        
        Args:
            n_components: PCA降维的组件数
            random_state: 随机种子
        """
        self.n_components = n_components
        self.random_state = random_state
        self.pca = PCA(n_components=n_components, random_state=random_state)
        self.scaler = StandardScaler()
        
    def extract_features(self, matrix: Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation],
                        method: str = 'pca') -> np.ndarray:
        """提取矩阵特征
        
        Args:
            matrix: 输入矩阵
            method: 特征提取方法 ('pca', 'raw')
            
        Returns:
            特征矩阵
            
        Raises:
            ValueError: 如果方法不支持
        """
        if method == 'pca':
            # 标准化数据
            scaled_data = self.scaler.fit_transform(matrix.data.reshape(-1, 1))
            # 应用PCA
            return self.pca.fit_transform(scaled_data)
        elif method == 'raw':
            return matrix.data
        else:
            raise ValueError(f'不支持的特征提取方法: {method}')
            
    def cluster_analysis(self, matrix: Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation],
                        method: str = 'kmeans', n_clusters: int = 3) -> np.ndarray:
        """聚类分析
        
        Args:
            matrix: 输入矩阵
            method: 聚类方法 ('kmeans', 'dbscan')
            n_clusters: 聚类数量（仅用于K-means）
            
        Returns:
            聚类标签
            
        Raises:
            ValueError: 如果方法不支持
        """
        # 提取特征
        features = self.extract_features(matrix)
        
        if method == 'kmeans':
            # 使用K-means聚类
            kmeans = KMeans(n_clusters=n_clusters, random_state=self.random_state)
            return kmeans.fit_predict(features)
        elif method == 'dbscan':
            # 使用DBSCAN聚类
            dbscan = DBSCAN(eps=0.5, min_samples=5)
            return dbscan.fit_predict(features)
        else:
            raise ValueError(f'不支持的聚类方法: {method}')
            
    def pattern_recognition(self, matrix: Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation],
                          window_size: int = 3) -> List[Dict]:
        """模式识别
        
        Args:
            matrix: 输入矩阵
            window_size: 滑动窗口大小
            
        Returns:
            识别到的模式列表
        """
        patterns = []
        data = matrix.data
        
        # 使用滑动窗口进行模式识别
        for i in range(len(data) - window_size + 1):
            window = data[i:i + window_size]
            # 计算窗口的统计特征
            pattern = {
                'start_index': i,
                'mean': np.mean(window),
                'std': np.std(window),
                'trend': np.polyfit(range(window_size), window, 1)[0]
            }
            patterns.append(pattern)
            
        return patterns
        
    def calculate_importance(self, matrix: Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation],
                           method: str = 'variance') -> np.ndarray:
        """计算重要性
        
        Args:
            matrix: 输入矩阵
            method: 重要性计算方法 ('variance', 'entropy')
            
        Returns:
            重要性得分
            
        Raises:
            ValueError: 如果方法不支持
        """
        if method == 'variance':
            # 使用方差作为重要性指标
            return np.var(matrix.data, axis=0)
        elif method == 'entropy':
            # 使用信息熵作为重要性指标
            data = matrix.data
            # 将数据归一化到[0,1]区间
            data_norm = (data - np.min(data)) / (np.max(data) - np.min(data))
            # 计算信息熵
            entropy = -np.sum(data_norm * np.log2(data_norm + 1e-10))
            return np.array([entropy])
        else:
            raise ValueError(f'不支持的重要性计算方法: {method}')
            
    def predict(self, matrix: Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation],
               target: np.ndarray, test_size: float = 0.2) -> Tuple[np.ndarray, np.ndarray]:
        """预测功能
        
        Args:
            matrix: 输入矩阵
            target: 目标值
            test_size: 测试集比例
            
        Returns:
            预测值和真实值的元组
        """
        # 提取特征
        features = self.extract_features(matrix)
        
        # 划分训练集和测试集
        n_samples = len(features)
        n_test = int(n_samples * test_size)
        indices = np.random.permutation(n_samples)
        test_indices = indices[:n_test]
        train_indices = indices[n_test:]
        
        X_train = features[train_indices]
        y_train = target[train_indices]
        X_test = features[test_indices]
        y_test = target[test_indices]
        
        # 训练随机森林回归器
        rf = RandomForestRegressor(n_estimators=100, random_state=self.random_state)
        rf.fit(X_train, y_train)
        
        # 预测
        y_pred = rf.predict(X_test)
        
        return y_pred, y_test 