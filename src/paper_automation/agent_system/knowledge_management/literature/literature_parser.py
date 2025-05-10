"""
文献解析模块，用于解析PDF文献并提取相关信息。
"""
from typing import Dict, List, Any, Optional, Tuple, Union
import logging
from dataclasses import dataclass
import os
import PyPDF2
import json
from .collector import LiteratureMetadata

@dataclass
class ParsedPaper:
    """解析后的论文数据结构"""
    metadata: Dict[str, Any]
    content: Dict[str, Any]
    citations: List[Dict[str, Any]]
    keywords: List[str]

class LiteratureParser:
    """文献解析器类，用于解析PDF文献并提取相关信息"""
    
    def __init__(self, base_dir: Optional[str] = None, min_year: int = 1900):
        """
        初始化文献解析器
        
        Args:
            base_dir: PDF文件存储的基础目录
            min_year: 最小年份限制
        """
        self.base_dir = base_dir
        self.logger = logging.getLogger(__name__)
        self.parsed_papers: Dict[str, ParsedPaper] = {}
        self.min_year = min_year
        
    def _is_valid_paper(self, paper_data: Dict[str, Any]) -> bool:
        """检查论文是否有效
        
        Args:
            paper_data: 论文数据
            
        Returns:
            bool: 论文是否有效
        """
        # 检查输入类型
        if paper_data is None:
            self.logger.warning("论文数据为空")
            return False
        
        if not isinstance(paper_data, dict):
            self.logger.warning(f"论文数据类型无效: {type(paper_data)}")
            return False
        
        # 检查必要字段
        required_fields = ["title", "authors", "year", "abstract"]
        for field in required_fields:
            if not paper_data.get(field):
                self.logger.warning(f"论文缺少必要字段: {field}")
                return False
                
        # 检查年份
        if paper_data.get("year", 0) < self.min_year:
            self.logger.warning(f"论文年份过早: {paper_data.get('year')}")
            return False
            
        # 检查作者数量
        if len(paper_data.get("authors", [])) == 0:
            self.logger.warning("论文没有作者信息")
            return False
            
        # 检查摘要长度（中文按字符计算，英文按单词计算）
        abstract = paper_data.get("abstract", "")
        if not abstract:
            self.logger.warning("论文摘要为空")
            return False
        
        # 如果摘要包含中文字符，按字符计算长度
        if any("\u4e00" <= char <= "\u9fff" for char in abstract):
            if len(abstract) < 50:  # 中文摘要至少50个字
                self.logger.warning("中文摘要过短")
                return False
        else:
            # 英文摘要按单词计算，至少30个单词
            if len(abstract.split()) < 30:
                self.logger.warning("英文摘要过短")
                return False
            
        return True
    
    def parse_paper(self, paper_data: Dict[str, Any]) -> Optional[ParsedPaper]:
        """
        解析论文数据
        
        Args:
            paper_data: 论文数据字典
            
        Returns:
            Optional[ParsedPaper]: 解析后的论文，如果论文无效则返回None
        """
        if not self._is_valid_paper(paper_data):
            return None
            
        try:
            # 解析元数据
            metadata = self.parse_metadata(paper_data)
            
            # 解析内容
            content = self.parse_content(paper_data)
            
            # 解析引用
            citations = self.parse_citations(paper_data)
            
            # 解析关键词
            keywords = self.parse_keywords(paper_data)
            
            # 创建解析后的论文对象
            parsed_paper = ParsedPaper(
                metadata=metadata,
                content=content,
                citations=citations,
                keywords=keywords
            )
            
            # 缓存解析结果
            self.parsed_papers[paper_data["title"]] = parsed_paper
            
            return parsed_paper
            
        except Exception as e:
            self.logger.error(f"解析论文失败: {str(e)}")
            return None
    
    def parse_metadata(self, paper_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析论文元数据
        
        Args:
            paper_data: 论文原始数据
            
        Returns:
            Dict[str, Any]: 解析后的元数据
        """
        return {
            "title": paper_data.get("title", ""),
            "authors": paper_data.get("authors", []),
            "year": paper_data.get("year", 0),
            "journal": paper_data.get("journal", ""),
            "doi": paper_data.get("doi", ""),
            "url": paper_data.get("url", ""),
            "abstract": paper_data.get("abstract", ""),
            "keywords": paper_data.get("keywords", []),
            "citations": paper_data.get("citations", 0),
            "references": paper_data.get("references", []),
            "pdf_path": paper_data.get("pdf_path", ""),
            "source": paper_data.get("source", ""),
            "venue": paper_data.get("venue", "")
        }
    
    def parse_content(self, paper_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析论文内容
        
        Args:
            paper_data: 论文原始数据
            
        Returns:
            Dict[str, Any]: 解析后的内容
        """
        return {
            "abstract": paper_data.get("abstract", ""),
            "full_text": paper_data.get("content", ""),
            "sections": paper_data.get("sections", []),
            "figures": paper_data.get("figures", []),
            "tables": paper_data.get("tables", []),
            "equations": paper_data.get("equations", [])
        }
    
    def parse_citations(self, paper_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """解析论文引用
        
        Args:
            paper_data: 论文原始数据
            
        Returns:
            List[Dict[str, Any]]: 解析后的引用列表
        """
        citations = paper_data.get("references", [])
        if not citations and "citations" in paper_data:
            if isinstance(paper_data["citations"], list):
                citations = paper_data["citations"]
            else:
                citations = []
        return citations
    
    def parse_keywords(self, paper_data: Dict[str, Any]) -> List[str]:
        """解析论文关键词
        
        Args:
            paper_data: 论文原始数据
            
        Returns:
            List[str]: 解析后的关键词列表
        """
        return paper_data.get("keywords", [])
        
    def save_parsed_paper(self, paper_id: str, paper: Optional[ParsedPaper]) -> None:
        """保存解析后的论文
        
        Args:
            paper_id: 论文ID
            paper: 解析后的论文对象
            
        Raises:
            ValueError: 当论文ID无效或论文对象无效时
        """
        if not paper_id or not isinstance(paper_id, str):
            raise ValueError("Invalid paper ID")
            
        if not paper or not isinstance(paper, ParsedPaper):
            raise ValueError("Invalid parsed paper")
            
        self.parsed_papers[paper_id] = paper
        
    def load_parsed_paper(self, paper_id: str) -> Optional[ParsedPaper]:
        """加载解析后的论文
        
        Args:
            paper_id: 论文ID
            
        Returns:
            Optional[ParsedPaper]: 解析后的论文对象，如果不存在则返回None
            
        Raises:
            ValueError: 当论文ID无效时
        """
        if not paper_id or not isinstance(paper_id, str):
            raise ValueError("Invalid paper ID")
            
        return self.parsed_papers.get(paper_id)
        
    def analyze_paper(self, paper_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析论文数据
        
        Args:
            paper_data: 论文数据字典
            
        Returns:
            Dict[str, Any]: 分析结果字典
            
        Raises:
            ValueError: 当论文数据无效时
        """
        try:
            if not self._is_valid_paper(paper_data):
                raise ValueError("Invalid paper data")
                
            analysis = {}
            
            # 分析元数据完整性
            metadata = self.parse_metadata(paper_data)
            analysis["metadata_completeness"] = len(metadata) / 5
            
            # 分析内容结构
            content = self.parse_content(paper_data)
            analysis["content_structure"] = {
                "has_abstract": "abstract" in content,
                "has_full_text": "full_text" in content,
                "has_sections": "sections" in content
            }
            
            # 分析引用
            citations = self.parse_citations(paper_data)
            analysis["citation_analysis"] = {
                "total_citations": len(citations),
                "citation_completeness": sum(1 for c in citations if c["title"] and c["authors"]) / len(citations) if citations else 0
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing paper: {str(e)}")
            raise ValueError(f"Error analyzing paper: {str(e)}")
            
    def search_local_pdfs(self, query: str, year_range: Optional[Tuple[int, int]] = None, limit: int = 10) -> List[LiteratureMetadata]:
        """搜索本地PDF文件
        
        Args:
            query: 搜索关键词
            year_range: 年份范围元组 (start_year, end_year)
            limit: 返回结果数量限制
            
        Returns:
            List[LiteratureMetadata]: 匹配的PDF文件元数据列表
        """
        if not self.base_dir:
            return []
            
        try:
            results = []
            for filename in os.listdir(self.base_dir):
                if not filename.endswith(".pdf"):
                    continue
                    
                metadata = self._extract_metadata_from_pdf(
                    os.path.join(self.base_dir, filename)
                )
                if not metadata:
                    continue
                    
                if year_range:
                    if metadata["year"] < year_range[0] or metadata["year"] > year_range[1]:
                        continue
                        
                if (query.lower() in metadata["title"].lower() or 
                    query.lower() in metadata["abstract"].lower()):
                    results.append(metadata)
                    
                if len(results) >= limit:
                    break
                    
            return results
            
        except Exception as e:
            self.logger.error(f"Error searching local PDFs: {str(e)}")
            return []
            
    def get_pdf_full_text(self, metadata: Dict[str, Any]) -> Optional[str]:
        """获取PDF文件的完整文本内容
        
        Args:
            metadata: 论文元数据字典
            
        Returns:
            Optional[str]: PDF文件的文本内容，获取失败返回None
        """
        if not metadata.get("pdf_path"):
            return None
            
        try:
            with open(metadata["pdf_path"], "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
                
        except Exception as e:
            self.logger.error(f"Error getting PDF full text: {str(e)}")
            return None
            
    def _extract_metadata_from_pdf(self, pdf_path: str) -> Optional[Dict[str, Any]]:
        """从PDF文件中提取元数据
        
        Args:
            pdf_path: PDF文件路径
            
        Returns:
            Optional[Dict[str, Any]]: 提取的元数据字典，提取失败返回None
        """
        try:
            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                first_page = reader.pages[0]
                text = first_page.extract_text()
                
                # 提取标题
                title = ""
                for line in text.split("\n"):
                    if line.strip():
                        title = line.strip()
                        break
                        
                # 提取作者
                authors = []
                for line in text.split("\n"):
                    if line.strip() and title not in line:
                        authors.append(line.strip())
                        
                # 提取年份
                year = 0
                for line in text.split("\n"):
                    if line.strip() and line.strip().isdigit():
                        year = int(line.strip())
                        break
                        
                # 提取摘要
                abstract = ""
                for line in text.split("\n"):
                    if "abstract" in line.lower() or "摘要" in line:
                        abstract = line.strip()
                        break
                        
                return {
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "abstract": abstract,
                    "pdf_path": pdf_path
                }
                
        except Exception as e:
            self.logger.error(f"Error extracting metadata from PDF: {str(e)}")
            return None
            
    def _check_metadata_completeness(self, metadata: Dict[str, Any]) -> Dict[str, bool]:
        """检查元数据完整性
        
        Args:
            metadata: 元数据字典
            
        Returns:
            Dict[str, bool]: 元数据完整性检查结果字典
        """
        return {
            "title": bool(metadata.get("title")),
            "authors": bool(metadata.get("authors")),
            "year": bool(metadata.get("year")),
            "abstract": bool(metadata.get("abstract")),
            "keywords": bool(metadata.get("keywords")),
            "citations": bool(metadata.get("citations")),
            "references": bool(metadata.get("references")),
            "pdf_path": bool(metadata.get("pdf_path")),
            "source": bool(metadata.get("source")),
            "venue": bool(metadata.get("venue"))
        }
        
    def _analyze_content_structure(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """分析内容结构
        
        Args:
            content: 内容字典
            
        Returns:
            Dict[str, Any]: 内容结构分析结果字典
        """
        return {
            "section_count": len(content.get("sections", [])),
            "figure_count": len(content.get("figures", [])),
            "table_count": len(content.get("tables", [])),
            "equation_count": len(content.get("equations", [])),
            "word_count": len(content.get("full_text", "").split()),
            "character_count": len(content.get("full_text", ""))
        }
        
    def _analyze_citations(self, citations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析引用信息
        
        Args:
            citations: 引用列表
            
        Returns:
            Dict[str, Any]: 引用分析结果字典
        """
        return {
            "total_citations": len(citations),
            "citation_years": [citation.get("year", 0) for citation in citations],
            "citation_authors": [citation.get("authors", []) for citation in citations],
            "citation_venues": [citation.get("venue", "") for citation in citations]
        }
        
    def _analyze_keywords(self, keywords: List[str]) -> Dict[str, Any]:
        """分析关键词
        
        Args:
            keywords: 关键词列表
            
        Returns:
            Dict[str, Any]: 关键词分析结果字典
        """
        return {
            "total_keywords": len(keywords),
            "keyword_frequency": {keyword: keywords.count(keyword) for keyword in set(keywords)}
        }