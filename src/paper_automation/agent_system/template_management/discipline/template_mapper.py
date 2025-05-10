from typing import Dict, List, Optional
import json
import logging
from pathlib import Path

class TemplateMapper:
    """模板映射器，负责管理和映射学科特定的论文模板"""

    def __init__(self, mapping_file: str):
        """初始化模板映射器
        
        Args:
            mapping_file: 映射规则配置文件的路径
        """
        self.logger = logging.getLogger(__name__)
        self.templates: Dict[str, Dict] = {}
        self.mappings: Dict[str, Dict] = {}
        self.combination_cache: Dict[tuple, float] = {}
        self._load_mapping_rules(mapping_file)

    def _load_mapping_rules(self, mapping_file: str) -> None:
        """加载映射规则配置文件
        
        Args:
            mapping_file: 映射规则配置文件的路径
        """
        try:
            with open(mapping_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # 加载组合规则
            if "combination_rules" in config:
                for rule in config["combination_rules"].get("allowed_combinations", []):
                    key = (rule["primary_type"], rule["secondary_type"])
                    self.combination_cache[key] = rule["weight"]
                    
            # 加载映射规则
            if "mapping_rules" in config:
                self.mappings = config["mapping_rules"]
                
        except Exception as e:
            self.logger.error(f"加载映射规则失败: {str(e)}")
            raise

    def _is_combination_allowed(self, primary_type: str, secondary_type: str) -> bool:
        """检查是否允许组合两种模板类型
        
        Args:
            primary_type: 主要模板类型
            secondary_type: 次要模板类型
            
        Returns:
            bool: 是否允许组合
        """
        return (primary_type, secondary_type) in self.combination_cache

    def _get_combination_weight(self, primary_type: str, secondary_type: str) -> float:
        """获取组合权重
        
        Args:
            primary_type: 主要模板类型
            secondary_type: 次要模板类型
            
        Returns:
            float: 组合权重
        """
        return self.combination_cache.get((primary_type, secondary_type), 0.0)

    def combine_templates(self, discipline: str, primary_type: str, secondary_type: str) -> Optional[Dict]:
        """组合两种模板类型
        
        Args:
            discipline: 学科名称
            primary_type: 主要模板类型
            secondary_type: 次要模板类型
            
        Returns:
            Optional[Dict]: 组合后的模板，如果组合失败则返回 None
        """
        if not self._is_combination_allowed(primary_type, secondary_type):
            return None
            
        weight = self._get_combination_weight(primary_type, secondary_type)
        
        # 获取两种模板
        primary_template = self.mappings.get(discipline, {}).get(primary_type)
        secondary_template = self.mappings.get(discipline, {}).get(secondary_type)
        
        if not primary_template or not secondary_template:
            return None
            
        # 合并特征
        combined = {
            "features": self._merge_features(
                primary_template["features"],
                secondary_template["features"],
                weight
            ),
            "template": self._merge_template_files(
                primary_template["template"],
                secondary_template["template"],
                weight
            ),
            "requirements": self._merge_requirements(
                primary_template["requirements"],
                secondary_template["requirements"],
                weight
            )
        }
        
        return combined

    def _merge_features(self, primary: Dict, secondary: Dict, weight: float) -> Dict:
        """合并特征
        
        Args:
            primary: 主要特征
            secondary: 次要特征
            weight: 组合权重
            
        Returns:
            Dict: 合并后的特征
        """
        result = primary.copy()
        for key, value in secondary.items():
            if key not in result:
                result[key] = value
            elif key == "research_type":
                # 对于研究类型，保持主要类型
                result[key] = primary[key]
            elif isinstance(value, str):
                result[key] = f"{result[key]}_{value}"
        return result

    def _merge_template_files(self, primary: Dict, secondary: Dict, weight: float) -> Dict:
        """合并模板文件
        
        Args:
            primary: 主要模板文件
            secondary: 次要模板文件
            weight: 组合权重
            
        Returns:
            Dict: 合并后的模板文件
        """
        result = {}
        for key in ["structure", "content"]:
            if key in primary and key in secondary:
                result[key] = f"combined_{primary[key]}_{secondary[key]}"
            elif key in primary:
                result[key] = primary[key]
            elif key in secondary:
                result[key] = secondary[key]
        return result

    def _merge_requirements(self, primary: Dict, secondary: Dict, weight: float) -> Dict:
        """合并要求
        
        Args:
            primary: 主要要求
            secondary: 次要要求
            weight: 组合权重
            
        Returns:
            Dict: 合并后的要求
        """
        result = {
            "required_sections": list(set(
                primary["required_sections"] + secondary["required_sections"]
            )),
            "section_order": self._merge_section_order(
                primary["section_order"],
                secondary["section_order"],
                weight
            ),
            "min_sections": max(
                primary["min_sections"],
                secondary["min_sections"]
            )
        }
        return result

    def _merge_section_order(self, primary: List[str], secondary: List[str], weight: float) -> List[str]:
        """合并章节顺序
        
        Args:
            primary: 主要章节顺序
            secondary: 次要章节顺序
            weight: 组合权重
            
        Returns:
            List[str]: 合并后的章节顺序
        """
        result = []
        seen = set()
        
        for section in primary + secondary:
            if section not in seen:
                result.append(section)
                seen.add(section)
                
        return result

    def validate_combined_template(self, discipline: str, primary_type: str, secondary_type: str, template: Dict) -> bool:
        """验证组合后的模板是否有效
        
        Args:
            discipline: 学科名称
            primary_type: 主要模板类型
            secondary_type: 次要模板类型
            template: 组合后的模板
            
        Returns:
            bool: 是否有效
        """
        # 检查基本结构
        required_keys = ["features", "template", "requirements"]
        if not all(key in template for key in required_keys):
            return False
            
        # 检查模板文件
        if not all(key in template["template"] for key in ["structure", "content"]):
            return False
            
        # 检查要求
        if not all(key in template["requirements"] for key in ["required_sections", "section_order", "min_sections"]):
            return False
            
        # 检查研究类型
        if template["features"]["research_type"] != primary_type:
            return False
            
        # 检查必需章节
        required_sections = set(template["requirements"]["required_sections"])
        if not all(section in required_sections for section in ["introduction", "conclusion"]):
            return False
            
        # 检查文件名格式
        if not template["template"]["structure"].startswith("combined_"):
            return False
            
        # 检查特征完整性
        required_features = {"research_type", "methodology", "analysis_type"}
        if not all(feature in template["features"] for feature in required_features):
            return False
            
        # 检查章节数量
        if len(template["requirements"]["required_sections"]) < template["requirements"]["min_sections"]:
            return False
            
        # 检查组合是否允许
        if not self._is_combination_allowed(primary_type, secondary_type):
            return False
            
        # 检查必需章节数量
        primary_template = self.mappings.get(discipline, {}).get(primary_type)
        secondary_template = self.mappings.get(discipline, {}).get(secondary_type)
        if primary_template and secondary_template:
            required_sections_count = len(set(
                primary_template["requirements"]["required_sections"] +
                secondary_template["requirements"]["required_sections"]
            ))
            if len(template["requirements"]["required_sections"]) < required_sections_count:
                return False
            
        return True

    def add_template(self, discipline: str, template: Dict) -> None:
        """添加学科特定的模板"""
        self.templates[discipline] = template

    def add_mapping(self, source: str, target: str, mapping: Dict) -> None:
        """添加模板间的映射关系"""
        if not source or not target or not mapping:
            raise ValueError("Invalid source, target, or mapping")
            
        if source not in self.mappings:
            self.mappings[source] = {}
        self.mappings[source][target] = mapping

    def get_template(self, discipline: str) -> Optional[Dict]:
        """获取学科特定的模板"""
        return self.templates.get(discipline)

    def map_template(self, source: str, target: str) -> Optional[Dict]:
        """将源模板映射到目标模板"""
        if not source or not target:
            return None
            
        if source not in self.mappings or target not in self.mappings[source]:
            return None
            
        source_template = self.get_template(source)
        if not source_template:
            return None
            
        mapping = self.mappings[source][target]
        return self._apply_mapping(source_template, mapping)

    def _apply_mapping(self, template: Dict, mapping: Dict) -> Dict:
        """应用映射规则到模板"""
        result = {}
        if "elements" in mapping:
            for source_key, source_value in template.items():
                if source_key in mapping["elements"]:
                    element_mapping = mapping["elements"][source_key]
                    target_key = element_mapping["target_type"]
                    result[target_key] = {
                        "type": target_key,
                        "content": f"{element_mapping['content_mapping']['prefix']}{source_value['content']}"
                    }
        return result 