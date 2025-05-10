"""研究范畴矩阵运算模块"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from scipy import sparse
import multiprocessing as mp
from functools import partial
from .base_representation import ResearchCategoryBaseRepresentation
from .advanced_representation import ResearchCategoryAdvancedRepresentation

class ResearchCategoryMatrixOperations:
    """研究范畴矩阵运算类"""
    
    def __init__(self, use_sparse: bool = False, num_processes: Optional[int] = None):
        """初始化矩阵运算类
        
        Args:
            use_sparse: 是否使用稀疏矩阵
            num_processes: 并行处理的进程数，默认为CPU核心数
        """
        self.use_sparse = use_sparse
        self.num_processes = num_processes or mp.cpu_count()
        
    def tensor_product(self, matrix1: Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation],
                      matrix2: Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation]) -> np.ndarray:
        """计算张量积
        
        Args:
            matrix1: 第一个矩阵
            matrix2: 第二个矩阵
            
        Returns:
            张量积结果矩阵
            
        Raises:
            ValueError: 如果矩阵维度不兼容
        """
        if self.use_sparse:
            return self._sparse_tensor_product(matrix1, matrix2)
        else:
            return self._dense_tensor_product(matrix1, matrix2)
            
    def _dense_tensor_product(self, matrix1: Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation],
                            matrix2: Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation]) -> np.ndarray:
        """计算密集矩阵的张量积
        
        Args:
            matrix1: 第一个矩阵
            matrix2: 第二个矩阵
            
        Returns:
            张量积结果矩阵
        """
        # 使用numpy的tensordot函数计算张量积
        return np.tensordot(matrix1.data, matrix2.data, axes=0)
        
    def _sparse_tensor_product(self, matrix1: Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation],
                             matrix2: Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation]) -> sparse.csr_matrix:
        """计算稀疏矩阵的张量积
        
        Args:
            matrix1: 第一个矩阵
            matrix2: 第二个矩阵
            
        Returns:
            张量积结果稀疏矩阵
        """
        # 将密集矩阵转换为稀疏矩阵
        sparse1 = sparse.csr_matrix(matrix1.data)
        sparse2 = sparse.csr_matrix(matrix2.data)
        
        # 计算稀疏矩阵的张量积
        return sparse.kron(sparse1, sparse2)
        
    def parallel_operation(self, matrices: List[Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation]],
                         operation: str) -> np.ndarray:
        """并行执行矩阵运算
        
        Args:
            matrices: 矩阵列表
            operation: 运算类型 ('add', 'multiply', 'divide')
            
        Returns:
            运算结果矩阵
            
        Raises:
            ValueError: 如果运算类型不支持
        """
        if operation not in ['add', 'multiply', 'divide']:
            raise ValueError(f'不支持的运算类型: {operation}')
            
        # 创建进程池
        with mp.Pool(processes=self.num_processes) as pool:
            # 根据运算类型选择操作函数
            if operation == 'add':
                op_func = np.add
            elif operation == 'multiply':
                op_func = np.multiply
            else:  # divide
                op_func = np.divide
                
            # 并行执行运算
            result = pool.map(partial(self._apply_operation, op_func=op_func), matrices)
            
        # 合并结果
        return np.sum(result, axis=0)
        
    def _apply_operation(self, matrix: Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation],
                        op_func: callable) -> np.ndarray:
        """应用运算函数
        
        Args:
            matrix: 输入矩阵
            op_func: 运算函数
            
        Returns:
            运算结果
        """
        return op_func(matrix.data, matrix.data)
        
    def optimize_memory(self, matrix: Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation],
                       threshold: float = 0.1) -> Union[np.ndarray, sparse.csr_matrix]:
        """优化矩阵内存使用
        
        Args:
            matrix: 输入矩阵
            threshold: 稀疏阈值，小于此值的元素将被视为0
            
        Returns:
            优化后的矩阵
        """
        if self.use_sparse:
            # 转换为稀疏矩阵
            sparse_matrix = sparse.csr_matrix(matrix.data)
            # 移除小于阈值的元素
            sparse_matrix.data[sparse_matrix.data < threshold] = 0
            sparse_matrix.eliminate_zeros()
            return sparse_matrix
        else:
            # 对于密集矩阵，直接返回
            return matrix.data
            
    def batch_operation(self, matrices: List[Union[ResearchCategoryBaseRepresentation, ResearchCategoryAdvancedRepresentation]],
                       batch_size: int = 100) -> List[np.ndarray]:
        """批量处理矩阵运算
        
        Args:
            matrices: 矩阵列表
            batch_size: 批处理大小
            
        Returns:
            处理结果列表
        """
        results = []
        for i in range(0, len(matrices), batch_size):
            batch = matrices[i:i + batch_size]
            # 对每个批次执行并行运算
            batch_result = self.parallel_operation(batch, 'add')
            results.append(batch_result)
        return results 