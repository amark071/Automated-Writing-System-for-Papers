from typing import Dict, List, Any, Optional, Callable
from abc import ABC, abstractmethod

class DynamicSystem(ABC):
    """动态系统基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.state = {}
        self.history = []
        
    @abstractmethod
    def iterate(self) -> None:
        """执行一次迭代"""
        pass
        
    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        """获取当前状态"""
        pass
        
    def save_state(self) -> None:
        """保存当前状态到历史记录"""
        self.history.append(self.state.copy())

class IterativeOptimizer(DynamicSystem):
    """迭代优化系统"""
    
    def __init__(self, name: str, objective: Callable[[Dict[str, Any]], float]):
        super().__init__(name)
        self.objective = objective
        self.best_state = None
        self.best_value = float('inf')
        
    def iterate(self) -> None:
        current_value = self.objective(self.state)
        if current_value < self.best_value:
            self.best_value = current_value
            self.best_state = self.state.copy()
        self.save_state()
        
    def get_state(self) -> Dict[str, Any]:
        return {
            'current_state': self.state,
            'best_state': self.best_state,
            'best_value': self.best_value,
            'history_length': len(self.history)
        }

class FeedbackSystem(DynamicSystem):
    """反馈系统"""
    
    def __init__(self, name: str, feedback_fn: Callable[[Dict[str, Any]], Dict[str, Any]]):
        super().__init__(name)
        self.feedback_fn = feedback_fn
        self.feedback_history = []
        
    def iterate(self) -> None:
        feedback = self.feedback_fn(self.state)
        self.feedback_history.append(feedback)
        self.state.update(feedback)
        self.save_state()
        
    def get_state(self) -> Dict[str, Any]:
        return {
            'current_state': self.state,
            'feedback_history': self.feedback_history,
            'history_length': len(self.history)
        }

class AdaptiveSystem(DynamicSystem):
    """自适应系统"""
    
    def __init__(self, name: str, adaptation_fn: Callable[[Dict[str, Any]], Dict[str, Any]]):
        super().__init__(name)
        self.adaptation_fn = adaptation_fn
        self.adaptation_history = []
        
    def iterate(self) -> None:
        adaptation = self.adaptation_fn(self.state)
        self.adaptation_history.append(adaptation)
        self.state.update(adaptation)
        self.save_state()
        
    def get_state(self) -> Dict[str, Any]:
        return {
            'current_state': self.state,
            'adaptation_history': self.adaptation_history,
            'history_length': len(self.history)
        }

class BalanceController(DynamicSystem):
    """动态平衡控制器"""
    
    def __init__(self, name: str, balance_fn: Callable[[Dict[str, Any]], Dict[str, Any]], threshold: float):
        super().__init__(name)
        self.balance_fn = balance_fn
        self.threshold = threshold
        self.is_balanced = False
        
    def iterate(self) -> None:
        balance_state = self.balance_fn(self.state)
        deviation = sum(abs(v) for v in balance_state.values())
        self.is_balanced = deviation < self.threshold
        if not self.is_balanced:
            self.state.update(balance_state)
        self.save_state()
        
    def get_state(self) -> Dict[str, Any]:
        return {
            'current_state': self.state,
            'is_balanced': self.is_balanced,
            'history_length': len(self.history)
        }
