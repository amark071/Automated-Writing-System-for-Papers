"""Rule Applier Module"""

import re
import logging

class RuleApplier:
    """Rule Applier Class"""
    
    def __init__(self):
        """初始化规则应用器"""
        self.applied_rules = {}
        self.logger = logging.getLogger(__name__)
    
    def apply_rule(self, rule_name: str, rule_data: dict, content: str = None) -> str:
        """应用规则
        
        Args:
            rule_name: 规则名称
            rule_data: 规则数据
            content: 要应用规则的内容
            
        Returns:
            str: 应用规则后的内容
            
        Raises:
            ValueError: 规则数据无效或规则已存在
        """
        if not rule_data or "type" not in rule_data:
            raise ValueError(f"Invalid rule data: {rule_data}")
            
        if rule_name in self.applied_rules:
            raise ValueError(f"Rule '{rule_name}' already exists")
            
        # 根据规则类型应用规则
        if rule_data["type"] == "format":
            content = self._apply_format_rule(rule_data, content)
            
        # 存储已应用的规则
        self.applied_rules[rule_name] = rule_data
        return content
    
    def _apply_format_rule(self, rule_data: dict, content: str) -> str:
        """应用格式规则
        
        Args:
            rule_data: 规则数据
            content: 要应用规则的内容
            
        Returns:
            str: 应用规则后的内容
        """
        if "pattern" in rule_data:
            pattern = rule_data["pattern"]
            
            # 如果有替换内容，执行替换
            if "replacement" in rule_data:
                try:
                    content = re.sub(pattern, rule_data["replacement"], content)
                except re.error:
                    self.logger.warning(
                        f"Replacement failed, using original content: pattern={pattern}, "
                        f"replacement={rule_data['replacement']}"
                    )
            else:
                # 否则只进行匹配验证
                matches = re.findall(pattern, content)
                if not matches:
                    self.logger.warning(f"Format validation failed: pattern={pattern}")
                    
        return content
    
    def remove_rule(self, rule_name: str) -> None:
        """删除已应用的规则
        
        Args:
            rule_name: 规则名称
            
        Raises:
            ValueError: 规则不存在
        """
        if rule_name not in self.applied_rules:
            raise ValueError(f"Rule '{rule_name}' does not exist")
            
        del self.applied_rules[rule_name]
    
    def get_applied_rule(self, rule_name: str) -> dict:
        """获取已应用的规则
        
        Args:
            rule_name: 规则名称
            
        Returns:
            dict: 规则数据
            
        Raises:
            ValueError: 规则不存在
        """
        if rule_name not in self.applied_rules:
            raise ValueError(f"Rule '{rule_name}' does not exist")
            
        return self.applied_rules[rule_name]
    
    def update_rule(self, rule_name: str, rule_data: dict) -> None:
        """更新已应用的规则
        
        Args:
            rule_name: 规则名称
            rule_data: 规则数据
            
        Raises:
            ValueError: 规则不存在
        """
        if rule_name not in self.applied_rules:
            raise ValueError(f"Rule '{rule_name}' does not exist")
            
        self.applied_rules[rule_name] = rule_data 