from typing import Dict, List, Any
import logging
import networkx as nx

class SpectrumInterface:
    """知识谱系接口类"""
    
    def __init__(self):
        """初始化知识谱系接口"""
        self.logger = logging.getLogger(__name__)
        self.spectra: Dict[str, nx.DiGraph] = {}
        
    def create_spectrum(self, spectrum_name: str, categories: List[str]) -> nx.DiGraph:
        """创建知识谱系
        
        Args:
            spectrum_name: 谱系名称
            categories: 类别列表
            
        Returns:
            nx.DiGraph: 创建的谱系
            
        Raises:
            ValueError: 当谱系名称已存在时抛出
        """
        if spectrum_name in self.spectra:
            raise ValueError(f"谱系 {spectrum_name} 已存在")
            
        spectrum = nx.DiGraph()
        # 添加类别节点
        for category in categories:
            spectrum.add_node(category)
        spectrum.categories = categories  # 为了测试用例的验证
            
        self.spectra[spectrum_name] = spectrum
        self.logger.info(f"创建谱系 {spectrum_name}")
        return spectrum
        
    def get_spectrum(self, spectrum_name: str) -> nx.DiGraph:
        """获取知识谱系
        
        Args:
            spectrum_name: 谱系名称
            
        Returns:
            nx.DiGraph: 获取的谱系
            
        Raises:
            ValueError: 当谱系不存在时抛出
        """
        if spectrum_name not in self.spectra:
            raise ValueError(f"谱系 {spectrum_name} 不存在")
            
        return self.spectra[spectrum_name]
        
    def update_spectrum(self, spectrum_name: str, new_categories: List[str]) -> nx.DiGraph:
        """更新知识谱系
        
        Args:
            spectrum_name: 谱系名称
            new_categories: 新的类别列表
            
        Returns:
            nx.DiGraph: 更新后的谱系
            
        Raises:
            ValueError: 当谱系不存在时抛出
        """
        if spectrum_name not in self.spectra:
            raise ValueError(f"谱系 {spectrum_name} 不存在")
            
        spectrum = self.spectra[spectrum_name]
        # 清除旧节点
        spectrum.clear()
        # 添加新类别节点
        for category in new_categories:
            spectrum.add_node(category)
        spectrum.categories = new_categories  # 为了测试用例的验证
            
        self.logger.info(f"更新谱系 {spectrum_name}")
        return spectrum
        
    def delete_spectrum(self, spectrum_name: str) -> None:
        """删除知识谱系
        
        Args:
            spectrum_name: 谱系名称
            
        Raises:
            ValueError: 当谱系不存在时抛出
        """
        if spectrum_name not in self.spectra:
            raise ValueError(f"谱系 {spectrum_name} 不存在")
            
        del self.spectra[spectrum_name]
        self.logger.info(f"删除谱系 {spectrum_name}")
        
    def analyze_spectrum(self, spectrum_name: str) -> Dict[str, Any]:
        """分析知识谱系
        
        Args:
            spectrum_name: 谱系名称
            
        Returns:
            Dict[str, Any]: 分析结果
            
        Raises:
            ValueError: 当谱系不存在时抛出
        """
        if spectrum_name not in self.spectra:
            raise ValueError(f"谱系 {spectrum_name} 不存在")
            
        spectrum = self.spectra[spectrum_name]
        analysis = {
            "category_count": len(spectrum.nodes),
            "hierarchy_depth": nx.dag_longest_path_length(spectrum) if spectrum.nodes else 0
        }
        self.logger.info(f"分析谱系 {spectrum_name}")
        return analysis
        
    def get_relationships(self, spectrum_name: str) -> Dict[str, Any]:
        """获取谱系关系
        
        Args:
            spectrum_name: 谱系名称
            
        Returns:
            Dict[str, Any]: 关系信息
            
        Raises:
            ValueError: 当谱系不存在时抛出
        """
        if spectrum_name not in self.spectra:
            raise ValueError(f"谱系 {spectrum_name} 不存在")
            
        spectrum = self.spectra[spectrum_name]
        relationships = {
            "edges": list(spectrum.edges()),
            "node_degrees": dict(spectrum.degree())
        }
        self.logger.info(f"获取谱系关系 {spectrum_name}")
        return relationships
        
    def visualize_spectrum(self, spectrum_name: str) -> Dict[str, Any]:
        """可视化知识谱系
        
        Args:
            spectrum_name: 谱系名称
            
        Returns:
            Dict[str, Any]: 可视化结果
            
        Raises:
            ValueError: 当谱系不存在时抛出
        """
        if spectrum_name not in self.spectra:
            raise ValueError(f"谱系 {spectrum_name} 不存在")
            
        spectrum = self.spectra[spectrum_name]
        visualization = {
            "node_count": spectrum.number_of_nodes(),
            "edge_count": spectrum.number_of_edges(),
            "layout": nx.spring_layout(spectrum)
        }
        self.logger.info(f"可视化谱系 {spectrum_name}")
        return visualization 