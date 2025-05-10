"""Rule Validator Module"""

import re
import logging

class RuleValidator:
    """Rule Validator Class"""
    
    def __init__(self):
        """初始化规则验证器"""
        self.validation_results = {}
        self.logger = logging.getLogger(__name__)
    
    def validate_rule(self, rule_name: str, rule_data: dict, content: str = None) -> dict:
        """验证规则
        
        Args:
            rule_name: 规则名称
            rule_data: 规则数据
            content: 要验证的内容
            
        Returns:
            dict: 验证结果
            
        Raises:
            ValueError: 规则数据无效
        """
        if not rule_data or "type" not in rule_data:
            raise ValueError(f"Invalid rule data: {rule_data}")
            
        result = {
            "is_valid": False,
            "details": {},
            "rule": rule_data
        }
        
        # 根据规则类型进行验证
        if rule_data["type"] == "format":
            result = self._validate_format_rule(rule_data, content)
            
        # 存储验证结果
        self.validation_results[rule_name] = result
        return result
    
    def _validate_format_rule(self, rule_data: dict, content: str) -> dict:
        """验证格式规则
        
        Args:
            rule_data: 规则数据
            content: 要验证的内容
            
        Returns:
            dict: 验证结果
        """
        result = {
            "is_valid": False,
            "details": {},
            "rule": rule_data
        }
        
        if "pattern" in rule_data:
            pattern = rule_data["pattern"]
            matches = re.findall(pattern, content)
            result["is_valid"] = len(matches) > 0
            result["details"]["matches"] = matches
            
        return result
    
    def remove_validation(self, rule_name: str) -> None:
        """删除验证结果
        
        Args:
            rule_name: 规则名称
            
        Raises:
            ValueError: 规则不存在
        """
        if rule_name not in self.validation_results:
            raise ValueError(f"Rule '{rule_name}' does not exist")
            
        del self.validation_results[rule_name]
    
    def get_validation_result(self, rule_name: str) -> dict:
        """获取验证结果
        
        Args:
            rule_name: 规则名称
            
        Returns:
            dict: 验证结果
            
        Raises:
            ValueError: 规则不存在
        """
        if rule_name not in self.validation_results:
            raise ValueError(f"Rule '{rule_name}' does not exist")
            
        return self.validation_results[rule_name]
    
    def update_validation(self, rule_name: str, rule_data: dict) -> None:
        """更新验证结果
        
        Args:
            rule_name: 规则名称
            rule_data: 规则数据
            
        Raises:
            ValueError: 规则不存在
        """
        if rule_name not in self.validation_results:
            raise ValueError(f"Rule '{rule_name}' does not exist")
            
        self.validation_results[rule_name]["rule"] = rule_data 