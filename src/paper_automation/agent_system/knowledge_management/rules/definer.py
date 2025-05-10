"""Rule Definer Module"""

from typing import Dict, Any
import logging
import re

class RuleDefiner:
    """Rule Definer Class"""
    
    def __init__(self):
        """初始化规则定义器"""
        self.logger = logging.getLogger(__name__)
        self.rules = {}
    
    def define_rule(self, rule_name: str, rule_data: Dict[str, Any]) -> None:
        """定义规则
        
        Args:
            rule_name: 规则名称
            rule_data: 规则数据
            
        Raises:
            ValueError: 规则已存在
        """
        if rule_name in self.rules:
            raise ValueError(f"Rule {rule_name} already exists")
            
        self.rules[rule_name] = rule_data.copy()
        self.logger.info(f"Rule defined successfully: {rule_name}")
    
    def remove_rule(self, rule_name: str) -> None:
        """删除规则
        
        Args:
            rule_name: 规则名称
            
        Raises:
            ValueError: 规则不存在
        """
        if rule_name not in self.rules:
            raise ValueError(f"Rule {rule_name} does not exist")
            
        del self.rules[rule_name]
        self.logger.info(f"Rule removed successfully: {rule_name}")
    
    def get_rule(self, rule_name: str) -> Dict[str, Any]:
        """获取规则
        
        Args:
            rule_name: 规则名称
            
        Returns:
            Dict[str, Any]: 规则数据
            
        Raises:
            ValueError: 规则不存在
        """
        if rule_name not in self.rules:
            raise ValueError(f"Rule {rule_name} does not exist")
            
        return self.rules[rule_name]
    
    def update_rule(self, rule_name: str, rule_data: Dict[str, Any]) -> None:
        """更新规则
        
        Args:
            rule_name: 规则名称
            rule_data: 规则数据
            
        Raises:
            ValueError: 规则不存在
        """
        if rule_name not in self.rules:
            raise ValueError(f"Rule {rule_name} does not exist")
            
        self.rules[rule_name] = rule_data.copy()
        self.logger.info(f"Rule updated successfully: {rule_name}")
    
    def validate_rule(self, rule_name: str) -> bool:
        """验证规则
        
        Args:
            rule_name: 规则名称
            
        Returns:
            bool: 规则是否有效
            
        Raises:
            ValueError: 规则不存在
        """
        if rule_name not in self.rules:
            raise ValueError(f"Rule {rule_name} does not exist")
            
        rule = self.rules[rule_name]
        
        # 检查必要字段
        if "type" not in rule:
            return False
            
        # 验证格式规则
        if rule["type"] == "format":
            if "pattern" not in rule:
                return False
                
            try:
                re.compile(rule["pattern"])
            except re.error:
                return False
                
        return True
    
    def compose_rules(self, composition_name: str, composition_data: Dict[str, Any]) -> None:
        """组合规则
        
        Args:
            composition_name: 组合规则名称
            composition_data: 组合规则数据
            
        Raises:
            ValueError: 组合规则已存在或规则不存在
        """
        if composition_name in self.rules:
            raise ValueError(f"Rule {composition_name} already exists")
            
        if "rules" not in composition_data:
            raise ValueError("Composition data missing rules field")
            
        # 检查所有规则是否存在
        for rule_name in composition_data["rules"]:
            if rule_name not in self.rules:
                raise ValueError(f"Rule {rule_name} does not exist")
                
        self.rules[composition_name] = composition_data.copy()
        self.logger.info(f"Rules composed successfully: {composition_name}") 