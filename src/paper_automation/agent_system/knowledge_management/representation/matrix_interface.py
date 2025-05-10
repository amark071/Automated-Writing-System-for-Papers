from typing import Dict, List, Any, Tuple
import logging
import numpy as np

class MatrixInterface:
    """知识矩阵接口类"""
    
    def __init__(self):
        """初始化知识矩阵接口"""
        self.logger = logging.getLogger(__name__)
        self.matrices: Dict[str, np.ndarray] = {}
        
    def create_matrix(self, matrix_name: str, dimensions: Tuple[int, int]) -> np.ndarray:
        """创建知识矩阵
        
        Args:
            matrix_name: 矩阵名称
            dimensions: 矩阵维度元组 (行数, 列数)
            
        Returns:
            np.ndarray: 创建的矩阵
            
        Raises:
            ValueError: 当矩阵名称已存在时抛出
        """
        if matrix_name in self.matrices:
            raise ValueError(f"矩阵 {matrix_name} 已存在")
            
        matrix = np.zeros(dimensions)
        self.matrices[matrix_name] = matrix
        self.logger.info(f"创建矩阵 {matrix_name}, 维度 {dimensions}")
        return matrix
        
    def get_matrix(self, matrix_name: str) -> np.ndarray:
        """获取知识矩阵
        
        Args:
            matrix_name: 矩阵名称
            
        Returns:
            np.ndarray: 获取的矩阵
            
        Raises:
            ValueError: 当矩阵不存在时抛出
        """
        if matrix_name not in self.matrices:
            raise ValueError(f"矩阵 {matrix_name} 不存在")
            
        return self.matrices[matrix_name]
        
    def update_matrix(self, matrix_name: str, new_dimensions: Tuple[int, int]) -> np.ndarray:
        """更新知识矩阵
        
        Args:
            matrix_name: 矩阵名称
            new_dimensions: 新的矩阵维度
            
        Returns:
            np.ndarray: 更新后的矩阵
            
        Raises:
            ValueError: 当矩阵不存在时抛出
        """
        if matrix_name not in self.matrices:
            raise ValueError(f"矩阵 {matrix_name} 不存在")
            
        new_matrix = np.zeros(new_dimensions)
        old_matrix = self.matrices[matrix_name]
        min_rows = min(old_matrix.shape[0], new_dimensions[0])
        min_cols = min(old_matrix.shape[1], new_dimensions[1])
        new_matrix[:min_rows, :min_cols] = old_matrix[:min_rows, :min_cols]
        
        self.matrices[matrix_name] = new_matrix
        self.logger.info(f"更新矩阵 {matrix_name}, 新维度 {new_dimensions}")
        return new_matrix
        
    def delete_matrix(self, matrix_name: str) -> None:
        """删除知识矩阵
        
        Args:
            matrix_name: 矩阵名称
            
        Raises:
            ValueError: 当矩阵不存在时抛出
        """
        if matrix_name not in self.matrices:
            raise ValueError(f"矩阵 {matrix_name} 不存在")
            
        del self.matrices[matrix_name]
        self.logger.info(f"删除矩阵 {matrix_name}")
        
    def perform_operation(self, matrix_name: str, operation: str) -> np.ndarray:
        """执行矩阵运算
        
        Args:
            matrix_name: 矩阵名称
            operation: 运算类型
            
        Returns:
            np.ndarray: 运算结果
            
        Raises:
            ValueError: 当矩阵不存在或运算类型不支持时抛出
        """
        if matrix_name not in self.matrices:
            raise ValueError(f"矩阵 {matrix_name} 不存在")
            
        matrix = self.matrices[matrix_name]
        if operation == "transpose":
            return matrix.T
        else:
            raise ValueError(f"不支持的运算类型: {operation}")
            
    def analyze_matrix(self, matrix_name: str) -> Dict[str, Any]:
        """分析知识矩阵
        
        Args:
            matrix_name: 矩阵名称
            
        Returns:
            Dict[str, Any]: 分析结果
            
        Raises:
            ValueError: 当矩阵不存在时抛出
        """
        if matrix_name not in self.matrices:
            raise ValueError(f"矩阵 {matrix_name} 不存在")
            
        matrix = self.matrices[matrix_name]
        analysis = {
            "rank": np.linalg.matrix_rank(matrix),
            "eigenvalues": np.linalg.eigvals(matrix)
        }
        self.logger.info(f"分析矩阵 {matrix_name}")
        return analysis
        
    def visualize_matrix(self, matrix_name: str) -> Dict[str, Any]:
        """可视化知识矩阵
        
        Args:
            matrix_name: 矩阵名称
            
        Returns:
            Dict[str, Any]: 可视化结果
            
        Raises:
            ValueError: 当矩阵不存在时抛出
        """
        if matrix_name not in self.matrices:
            raise ValueError(f"矩阵 {matrix_name} 不存在")
            
        matrix = self.matrices[matrix_name]
        visualization = {
            "shape": matrix.shape,
            "sparsity": np.count_nonzero(matrix) / matrix.size,
            "histogram": np.histogram(matrix.flatten(), bins=10)
        }
        self.logger.info(f"可视化矩阵 {matrix_name}")
        return visualization 