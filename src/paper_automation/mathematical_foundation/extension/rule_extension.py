from typing import Dict, List, Any, Optional, Callable, Set
from abc import ABC, abstractmethod

class Rule(ABC):
    """规则基类"""
    
    def __init__(self, name: str, condition: Callable[[Any], bool], action: Callable[[Any], Any]):
        self.name = name
        self.condition = condition
        self.action = action
        
    def is_valid(self) -> bool:
        return self.condition is not None and self.action is not None

class RuleSet:
    """规则集合类"""
    
    def __init__(self, name: str):
        self.name = name
        self.rules = {}
        
    def add_rule(self, rule: Rule):
        self.rules[rule.name] = rule
        
    def add_rule_group(self, name: str, group: 'RuleGroup'):
        if not group.is_group():
            raise ValueError('Invalid group structure')
        self.rule_groups[name] = group
        
    def compose_rules(self, rule1: Rule, rule2: Rule) -> Optional[Rule]:
        def composed_condition(x: Any) -> bool:
            return rule1.condition(x) and rule2.condition(rule1.action(x))
            
        def composed_action(x: Any) -> Any:
            return rule2.action(rule1.action(x))
            
        composed_rule = Rule(
            name=f"{rule1.name}_compose_{rule2.name}",
            condition=composed_condition,
            action=composed_action
        )
        
        if composed_rule.is_valid():
            return composed_rule
        return None
        
    def find_rule_chain(self, start: Any, target: Any) -> Optional[List[Rule]]:
        def dfs(current: Any, visited: Set[Any], path: List[Rule]) -> Optional[List[Rule]]:
            if current == target:
                return path
                
            visited.add(current)
            
            for rule in self.rules.values():
                if not rule.condition(current):
                    continue
                    
                next_state = rule.action(current)
                if next_state in visited:
                    continue
                    
                new_path = path + [rule]
                result = dfs(next_state, visited, new_path)
                if result:
                    return result
                    
            visited.remove(current)
            return None
            
        return dfs(start, set(), [])

class RuleGroup:
    """规则组类"""
    
    def __init__(self, name: str):
        self.name = name
        self.rules = {}
        
    def is_group(self) -> bool:
        return True

class Morphism:
    """态射类"""
    
    def __init__(self, name: str, source: RuleSet, target: RuleSet, mapping: Callable[[Any], Any]):
        self.name = name
        self.source = source
        self.target = target
        self.mapping = mapping
        
    def is_homomorphism(self) -> bool:
        return True

class RuleExtension:
    """规则扩展类"""
    
    def __init__(self, name: str):
        self.name = name
        self.rule_sets = {}
        self.extension_morphisms = {}
        
    def add_rule_set(self, rule_set: RuleSet):
        self.rule_sets[rule_set.name] = rule_set
        
    def add_extension_morphism(self, name: str, morphism: Morphism):
        if not morphism.is_homomorphism():
            raise ValueError('Invalid homomorphism')
        self.extension_morphisms[name] = morphism
        
    def extend_rules(self, source_set: str, target_set: str) -> Optional[RuleSet]:
        if source_set not in self.rule_sets or target_set not in self.rule_sets:
            return None
            
        source = self.rule_sets[source_set]
        target = self.rule_sets[target_set]
        
        extended_set = RuleSet(f"{source_set}_extended_to_{target_set}")
        
        for rule in source.rules.values():
            extended_set.add_rule(rule)
            
        for morphism in self.extension_morphisms.values():
            if morphism.source != source or morphism.target != target:
                continue
                
            for rule in target.rules.values():
                def extended_condition(x: Any) -> bool:
                    return rule.condition(morphism.mapping(x))
                    
                def extended_action(x: Any) -> Any:
                    return morphism.mapping(rule.action(morphism.mapping(x)))
                    
                extended_rule = Rule(
                    name=f"{rule.name}_extended",
                    condition=extended_condition,
                    action=extended_action
                )
                
                if extended_rule.is_valid():
                    extended_set.add_rule(extended_rule)
                    
        return extended_set
        
    def discover_new_rules(self, rule_set: str) -> List[Rule]:
        if rule_set not in self.rule_sets:
            return []
            
        rules = self.rule_sets[rule_set].rules
        new_rules = []
        
        # 规则组合
        for rule1 in rules.values():
            for rule2 in rules.values():
                if rule1 == rule2:
                    continue
                    
                composed = self.rule_sets[rule_set].compose_rules(rule1, rule2)
                if composed and composed.name not in rules:
                    new_rules.append(composed)
                    
        # 规则链发现
        for rule in rules.values():
            for x in rule.domain:
                for y in rule.codomain:
                    chain = self.rule_sets[rule_set].find_rule_chain(x, y)
                    if chain and len(chain) > 1:
                        def chain_condition(z: Any) -> bool:
                            return all(r.condition(z) for r in chain)
                            
                        def chain_action(z: Any) -> Any:
                            result = z
                            for r in chain:
                                result = r.action(result)
                            return result
                            
                        new_rule = Rule(
                            name=f"chain_{x}_to_{y}",
                            condition=chain_condition,
                            action=chain_action
                        )
                        
                        if new_rule.is_valid() and new_rule.name not in rules:
                            new_rules.append(new_rule)
                            
        return new_rules
        
    def analyze_extension(self) -> Dict[str, Any]:
        analysis = {
            'rule_sets': len(self.rule_sets),
            'total_rules': sum(len(rs.rules) for rs in self.rule_sets.values()),
            'morphisms': len(self.extension_morphisms),
            'extensions': []
        }
        
        for source_name in self.rule_sets:
            for target_name in self.rule_sets:
                if source_name == target_name:
                    continue
                    
                extended_set = self.extend_rules(source_name, target_name)
                if extended_set:
                    extension_info = {
                        'source': source_name,
                        'target': target_name,
                        'original_rules': len(self.rule_sets[source_name].rules),
                        'extended_rules': len(extended_set.rules),
                        'new_rules': len(extended_set.rules) - len(self.rule_sets[source_name].rules)
                    }
                    analysis['extensions'].append(extension_info)
                    
        return analysis
