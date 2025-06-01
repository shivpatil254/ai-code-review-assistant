from abc import ABC, abstractmethod
from typing import List, Dict, Any
import ast
import re

class BaseAnalyzer(ABC):
    """Base class for language-specific analyzers"""
    
    def __init__(self):
        self.issues = []
        self.metrics = {
            "lines_of_code": 0,
            "cyclomatic_complexity": 1.0,
            "maintainability_index": 100.0,
            "code_duplication": 0.0
        }
    
    @abstractmethod
    def analyze(self, code: str) -> Dict[str, Any]:
        """Analyze code and return issues and metrics"""
        pass
    
    def calculate_score(self) -> float:
        """Calculate overall code quality score"""
        base_score = 100
        
        # Deduct points for issues
        for issue in self.issues:
            if issue["severity"] == "error":
                base_score -= 10
            elif issue["severity"] == "warning":
                base_score -= 5
            else:
                base_score -= 2
        
        # Factor in metrics
        complexity_penalty = max(0, (self.metrics["cyclomatic_complexity"] - 10) * 2)
        base_score -= complexity_penalty
        
        return max(0, min(100, base_score))