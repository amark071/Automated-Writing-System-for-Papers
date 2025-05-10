"""Rule Engine Module

This module implements the rule engine for knowledge management, which is responsible for
processing and applying rules to the knowledge graph.
"""

import logging
from typing import Dict, Any, List, Optional

from .definer import RuleDefiner
from .validator import RuleValidator
from .applier import RuleApplier

class RuleEngine:
    """Rule Engine Class"""
    
    def __init__(self):
        """初始化规则引擎"""
        self.logger = logging.getLogger(__name__)
        self.rule_definer = RuleDefiner()
        self.rule_validator = RuleValidator()
        self.rule_applier = RuleApplier()
        self.rules = {}
    
    def define_rule(self, rule_id: str, rule_data: Dict[str, Any]) -> bool:
        """定义规则
        
        Args:
            rule_id: 规则ID
            rule_data: 规则数据
            
        Returns:
            bool: 是否成功定义规则
            
        Raises:
            ValueError: 规则ID为空或规则数据无效
        """
        try:
            if not rule_id:
                raise ValueError("Rule ID cannot be empty")
                
            if not rule_data or not isinstance(rule_data, dict):
                raise ValueError("Rule data must be a non-empty dictionary")
                
            # 定义规则
            rule = self.rule_definer.define_rule(rule_data)
            if not rule:
                return False
                
            # 验证规则
            if not self.rule_validator.validate_rule(rule):
                return False
                
            # 存储规则
            self.rules[rule_id] = rule
            
            self.logger.info(f"Defined rule: {rule_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error defining rule: {e}")
            return False
    
    def get_rule(self, rule_id: str) -> Optional[Dict[str, Any]]:
        """获取规则
        
        Args:
            rule_id: 规则ID
            
        Returns:
            Optional[Dict[str, Any]]: 规则数据
        """
        try:
            return self.rules.get(rule_id)
        except Exception as e:
            self.logger.error(f"Error getting rule: {e}")
            return None
    
    def remove_rule(self, rule_id: str) -> bool:
        """删除规则
        
        Args:
            rule_id: 规则ID
            
        Returns:
            bool: 是否成功删除规则
            
        Raises:
            ValueError: 规则不存在
        """
        if rule_id not in self.rules:
            self.logger.error(f"规则不存在: {rule_id}")
            raise ValueError(f"规则不存在: {rule_id}")
            
        del self.rules[rule_id]
        self.logger.info(f"规则已删除: {rule_id}")
        return True
    
    def apply_rule(self, rule_id: str, context: Dict[str, Any]) -> bool:
        """应用规则
        
        Args:
            rule_id: 规则ID
            context: 上下文数据
            
        Returns:
            bool: 是否成功应用规则
            
        Raises:
            ValueError: 规则不存在
        """
        try:
            if rule_id not in self.rules:
                raise ValueError(f"Rule not found: {rule_id}")
                
            rule = self.rules[rule_id]
            return self.rule_applier.apply_rule(rule, context)
            
        except Exception as e:
            self.logger.error(f"Error applying rule: {e}")
            return False
    
    def apply_rules(self, context: Dict[str, Any]) -> bool:
        """应用所有规则
        
        Args:
            context: 上下文数据
            
        Returns:
            bool: 是否成功应用所有规则
        """
        try:
            success = True
            for rule_id in self.rules:
                if not self.apply_rule(rule_id, context):
                    success = False
            return success
            
        except Exception as e:
            self.logger.error(f"Error applying rules: {e}")
            return False
    
    def validate_rules(self) -> bool:
        """验证所有规则
        
        Returns:
            bool: 是否所有规则都有效
        """
        try:
            for rule_id, rule in self.rules.items():
                if not self.rule_validator.validate_rule(rule):
                    self.logger.error(f"Invalid rule: {rule_id}")
                    return False
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating rules: {e}")
            return False
    
    def add_rule(self, rule: Dict[str, Any]) -> bool:
        """添加规则
        
        Args:
            rule: 规则数据
            
        Returns:
            bool: 是否成功添加规则
            
        Raises:
            ValueError: 规则无效
        """
        if rule is None:
            self.logger.error("规则不能为空")
            raise ValueError("规则不能为空")
            
        # 检查必要字段
        required_fields = ["id", "type", "condition", "action"]
        for field in required_fields:
            if field not in rule:
                self.logger.error(f"规则缺少必要字段: {field}")
                raise ValueError(f"规则缺少必要字段: {field}")
                
        # 验证规则类型
        if rule["type"] not in ("validation", "transformation", "generation"):
            self.logger.error(f"无效的规则类型: {rule['type']}")
            raise ValueError(f"无效的规则类型: {rule['type']}")
            
        # 验证条件
        if not self._is_valid_condition(rule["condition"]):
            self.logger.error(f"无效的条件: {rule['condition']}")
            raise ValueError(f"无效的条件: {rule['condition']}")
            
        # 添加规则
        self.rules[rule["id"]] = rule
        self.logger.info(f"添加规则: {rule['id']}")
        return True
    
    def _is_valid_condition(self, condition: str) -> bool:
        """检查条件是否有效
        
        Args:
            condition: 条件字符串
            
        Returns:
            bool: 条件是否有效
        """
        valid_operators = [">", "<", ">=", "<=", "==", "!="]
        return any(op in condition for op in valid_operators)
    
    def evaluate_rules(self, context: Dict[str, Any]) -> bool:
        """评估所有规则
        
        Args:
            context: 上下文数据
            
        Returns:
            bool: 是否所有规则都满足条件
        """
        for rule_id, rule in self.rules.items():
            condition = rule["condition"]
            if not self._evaluate_condition(condition, context):
                self.logger.warning(f"规则 {rule_id} 条件不满足")
                return False
        return True
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """评估条件
        
        Args:
            condition: 条件字符串
            context: 上下文数据
            
        Returns:
            bool: 条件是否满足
            
        Raises:
            ValueError: 条件评估失败
        """
        try:
            # 替换上下文变量
            for key, value in context.items():
                condition = condition.replace(f"paper.{key}", str(value))
                
            # 评估条件
            result = eval(condition, {"__builtins__": {}}, {})
            return bool(result)
            
        except Exception as e:
            self.logger.error(f"评估条件时出错: {e}")
            raise ValueError(f"条件评估失败: {e}") 