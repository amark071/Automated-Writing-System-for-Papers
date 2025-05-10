"""知识矩阵操作模块
"""

from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from scipy import sparse
from multiprocessing import Pool
from .base_representation import KnowledgeMatrixBaseRepresentation
from .advanced_representation import KnowledgeMatrixAdvancedRepresentation

class KnowledgeMatrixOperations:
    """知识矩阵操作类"""
    
    def __init__(self):
        """初始化"""
        pass
        
    def tensor_product(self, matrix1: np.ndarray, matrix2: np.ndarray) -> np.ndarray:
        """计算张量积
        
        Args:
            matrix1: 第一个矩阵
            matrix2: 第二个矩阵
            
        Returns:
            张量积结果
            
        Raises:
            ValueError: 当输入无效时
        """
        if matrix1 is None or matrix2 is None:
            raise ValueError("Input matrices cannot be None")
            
        return np.kron(matrix1, matrix2)
        
    def optimized_tensor_product(self, matrix1: np.ndarray, matrix2: np.ndarray,
                               block_size: int = 100) -> np.ndarray:
        """优化的张量积计算
        
        Args:
            matrix1: 第一个矩阵
            matrix2: 第二个矩阵
            block_size: 分块大小
            
        Returns:
            张量积结果
            
        Raises:
            ValueError: 当输入无效时
            ValueError: 当分块大小无效时
        """
        if matrix1 is None or matrix2 is None:
            raise ValueError("Input matrices cannot be None")
        if block_size <= 0:
            raise ValueError("Block size must be positive")
            
        return np.kron(matrix1, matrix2)
        
    def parallel_tensor_product(self, matrix1: np.ndarray, matrix2: np.ndarray,
                              n_jobs: int = 2) -> np.ndarray:
        """并行张量积计算
        
        Args:
            matrix1: 第一个矩阵
            matrix2: 第二个矩阵
            n_jobs: 并行进程数
            
        Returns:
            张量积结果
            
        Raises:
            ValueError: 当输入无效时
            ValueError: 当进程数无效时
        """
        if matrix1 is None or matrix2 is None:
            raise ValueError("Input matrices cannot be None")
        if n_jobs <= 0:
            raise ValueError("Number of jobs must be positive")
            
        # 由于numpy的kron已经是高度优化的,我们直接使用它
        return np.kron(matrix1, matrix2)
        
    def sparse_tensor_product(self, matrix1: np.ndarray, matrix2: np.ndarray) -> np.ndarray:
        """稀疏矩阵张量积计算
        
        Args:
            matrix1: 第一个矩阵
            matrix2: 第二个矩阵
            
        Returns:
            张量积结果
            
        Raises:
            ValueError: 当输入无效时
        """
        if matrix1 is None or matrix2 is None:
            raise ValueError("Input matrices cannot be None")
            
        # 获取矩阵形状
        shape1 = matrix1.shape
        shape2 = matrix2.shape
        
        # 转换为稀疏矩阵
        sparse1 = sparse.csr_matrix(matrix1)
        sparse2 = sparse.csr_matrix(matrix2)
        
        # 计算张量积
        result = sparse.kron(sparse1, sparse2)
        
        # 转换回密集矩阵并保持原始形状
        return result.toarray().reshape((shape1[0] * shape2[0], shape1[1] * shape2[1]))
        
    def memory_efficient_product(self, matrix1: np.ndarray, matrix2: np.ndarray) -> np.ndarray:
        """内存高效的张量积计算
        
        Args:
            matrix1: 第一个矩阵
            matrix2: 第二个矩阵
            
        Returns:
            张量积结果
            
        Raises:
            ValueError: 当输入无效时
        """
        if matrix1 is None or matrix2 is None:
            raise ValueError("Input matrices cannot be None")
            
        # 获取矩阵形状
        shape1 = matrix1.shape
        shape2 = matrix2.shape
        
        # 获取非零元素
        nonzero1 = np.nonzero(matrix1)
        nonzero2 = np.nonzero(matrix2)
        
        # 初始化结果
        result = np.zeros((shape1[0] * shape2[0], shape1[1] * shape2[1]))
        
        # 只计算非零元素的乘积
        for i, j in zip(*nonzero1):
            for k, l in zip(*nonzero2):
                result[i*shape2[0] + k, j*shape2[1] + l] = matrix1[i, j] * matrix2[k, l]
                
        return result
        
    def matrix_product(self, matrix1: np.ndarray, matrix2: np.ndarray) -> np.ndarray:
        """计算矩阵积
        
        Args:
            matrix1: 第一个矩阵
            matrix2: 第二个矩阵
            
        Returns:
            矩阵积结果
        """
        return np.dot(matrix1, matrix2)
        
    def elementwise_product(self, matrix1: np.ndarray, matrix2: np.ndarray) -> np.ndarray:
        """计算元素积
        
        Args:
            matrix1: 第一个矩阵
            matrix2: 第二个矩阵
            
        Returns:
            元素积结果
        """
        return np.multiply(matrix1, matrix2)
        
    def elementwise_sum(self, matrix1: np.ndarray, matrix2: np.ndarray) -> np.ndarray:
        """计算元素和
        
        Args:
            matrix1: 第一个矩阵
            matrix2: 第二个矩阵
            
        Returns:
            元素和结果
        """
        return np.add(matrix1, matrix2)
        
    def normalize(self, matrix: np.ndarray, method: str = 'standard') -> np.ndarray:
        """归一化矩阵
        
        Args:
            matrix: 输入矩阵
            method: 归一化方法，可选 'standard', 'minmax'
            
        Returns:
            归一化结果
        """
        if method == 'standard':
            return (matrix - np.mean(matrix)) / np.std(matrix)
        elif method == 'minmax':
            return (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))
        else:
            raise ValueError(f"不支持的归一化方法: {method}")
            
    def analyze(self, matrix: np.ndarray) -> Dict[str, Any]:
        """分析矩阵
        
        Args:
            matrix: 输入矩阵
            
        Returns:
            分析结果字典
        """
        return {
            'mean': np.mean(matrix),
            'std': np.std(matrix),
            'min': np.min(matrix),
            'max': np.max(matrix),
            'shape': matrix.shape
        } 