from typing import List, Dict, Optional, Any, Tuple, Union
from dataclasses import dataclass
import logging
from abc import ABC, abstractmethod
import json
import os

@dataclass
class LiteratureMetadata:
    """文献元数据类"""
    title: str
    authors: List[str]
    year: int
    journal: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[List[str]] = None
    citations: Optional[int] = None
    references: Optional[List[str]] = None
    pdf_path: Optional[str] = None
    source: Optional[str] = None
    venue: Optional[str] = None

class LiteratureSource(ABC):
    """文献来源抽象基类"""
    
    def __init__(self):
        """初始化文献来源"""
        self.logger = logging.getLogger(__name__)
    
    @abstractmethod
    def search(self, query: str, year_range: Optional[Tuple[int, int]] = None, limit: int = 10) -> List[LiteratureMetadata]:
        """搜索文献"""
        pass
    
    @abstractmethod
    def get_full_text(self, metadata: LiteratureMetadata) -> Optional[str]:
        """获取文献全文"""
        pass
    
    @abstractmethod
    def get_citations(self, metadata: Union[str, LiteratureMetadata]) -> List[LiteratureMetadata]:
        """获取文献引用"""
        pass

class LiteratureCollector:
    """文献收集器类"""
    
    def __init__(self):
        self.sources: Dict[str, LiteratureSource] = {}
        self.collected_papers: Dict[str, List[Dict[str, Any]]] = {}
        self.logger = logging.getLogger(__name__)
    
    def add_source(self, name: str, source: LiteratureSource) -> None:
        """添加文献来源"""
        self.sources[name] = source
        self.logger.info(f"Added literature source: {name}")
    
    def collect_papers(self, query: str, year_range: Tuple[int, int], sources: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """收集文献"""
        if not query:
            raise ValueError("Query cannot be empty")
            
        if year_range[0] > year_range[1]:
            raise ValueError("Invalid year range")
            
        papers = []
        source_list = sources if sources else list(self.sources.keys())
        
        for source_name in source_list:
            if source_name in self.sources:
                source_papers = self.sources[source_name].search(query, year_range)
                papers.extend([self._metadata_to_dict(p) for p in source_papers])
        
        return papers
    
    def filter_papers(self, papers: List[Dict[str, Any]], min_citations: Optional[int] = None) -> List[Dict[str, Any]]:
        """过滤文献"""
        filtered_papers = papers.copy()
        
        if min_citations is not None:
            filtered_papers = [p for p in filtered_papers if p.get("citations", 0) >= min_citations]
            
        return filtered_papers
    
    def save_papers(self, query: str, papers: List[Dict[str, Any]]) -> None:
        """保存文献"""
        self.collected_papers[query] = papers
        
    def load_papers(self, query: str) -> List[Dict[str, Any]]:
        """加载文献"""
        if query not in self.collected_papers:
            raise ValueError(f"No papers found for query: {query}")
        return self.collected_papers[query]
    
    def get_collection_statistics(self, query: str) -> Dict[str, Any]:
        """获取收集统计信息"""
        if query not in self.collected_papers:
            return {}
            
        papers = self.collected_papers[query]
        
        # 计算年份分布
        year_distribution = {}
        for paper in papers:
            year = paper.get("year")
            if year:
                year_distribution[year] = year_distribution.get(year, 0) + 1
                
        # 计算引用分布
        citation_distribution = {}
        for paper in papers:
            citations = paper.get("citations", 0)
            citation_distribution[citations] = citation_distribution.get(citations, 0) + 1
            
        return {
            "total_papers": len(papers),
            "year_distribution": year_distribution,
            "citation_distribution": citation_distribution
        }
    
    def _metadata_to_dict(self, metadata: LiteratureMetadata) -> Dict[str, Any]:
        """将元数据转换为字典"""
        return {
            "title": metadata.title,
            "authors": metadata.authors,
            "year": metadata.year,
            "journal": metadata.journal,
            "doi": metadata.doi,
            "url": metadata.url,
            "abstract": metadata.abstract,
            "keywords": metadata.keywords,
            "citations": metadata.citations,
            "references": metadata.references,
            "pdf_path": metadata.pdf_path,
            "source": metadata.source,
            "venue": metadata.venue
        }
    
    def _dict_to_metadata(self, data: Dict[str, Any]) -> LiteratureMetadata:
        """将字典转换为元数据"""
        return LiteratureMetadata(
            title=data["title"],
            authors=data["authors"],
            year=data["year"],
            journal=data.get("journal"),
            doi=data.get("doi"),
            url=data.get("url"),
            abstract=data.get("abstract"),
            keywords=data.get("keywords"),
            citations=data.get("citations"),
            references=data.get("references"),
            pdf_path=data.get("pdf_path"),
            source=data.get("source"),
            venue=data.get("venue")
        )

    def search(self, query: str, source: Optional[str] = None, limit: int = 10) -> List[LiteratureMetadata]:
        """搜索文献"""
        try:
            if source and source in self.sources:
                return self.sources[source].search(query, limit)
            else:
                results = []
                for src in self.sources.values():
                    results.extend(src.search(query, limit))
                return results[:limit]
        except Exception as e:
            self.logger.error(f"Error searching literature: {str(e)}")
            return []
    
    def get_full_text(self, metadata: LiteratureMetadata) -> Optional[str]:
        """获取文献全文"""
        try:
            if metadata.source and metadata.source in self.sources:
                return self.sources[metadata.source].get_full_text(metadata)
            return None
        except Exception as e:
            self.logger.error(f"Error getting full text: {str(e)}")
            return None
    
    def get_citations(self, metadata: LiteratureMetadata) -> List[LiteratureMetadata]:
        """获取文献引用"""
        try:
            if metadata.source and metadata.source in self.sources:
                return self.sources[metadata.source].get_citations(metadata)
            return []
        except Exception as e:
            self.logger.error(f"Error getting citations: {str(e)}")
            return []
    
    def save_metadata(self, metadata: LiteratureMetadata, path: str) -> bool:
        """保存文献元数据"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self._metadata_to_dict(metadata), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            self.logger.error(f"Error saving metadata: {str(e)}")
            return False
    
    def load_metadata(self, path: str) -> Optional[LiteratureMetadata]:
        """加载文献元数据"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self._dict_to_metadata(data)
        except Exception as e:
            self.logger.error(f"Error loading metadata: {str(e)}")
            return None 