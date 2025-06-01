import re
from typing import List, Dict, Any
from .base import BaseAnalyzer

class JavaScriptAnalyzer(BaseAnalyzer):
    """JavaScript/TypeScript code analyzer"""
    
    def __init__(self):
        super().__init__()
        self.patterns = {
            # Security
            r"eval\s*\(": ("Avoid eval() - security risk", "error"),
            r"innerHTML\s*=": ("Potential XSS vulnerability", "warning"),
            r"document\.write": ("Avoid document.write", "warning"),
            
            # Angular specific
            r"any\s*\)": ("Avoid using 'any' type", "warning"),
            r"subscribe\s*\([^)]*\)(?!.*unsubscribe)": ("Potential memory leak", "warning"),
            
            # Best practices
            r"var\s+": ("Use let or const instead of var", "warning"),
            r"console\.log": ("Remove console.log", "info"),
            r"==(?!=)": ("Use === instead of ==", "warning"),
        }
    
    def analyze(self, code: str) -> Dict[str, Any]:
        self.issues = []
        lines = code.split('\n')
        self.metrics["lines_of_code"] = len([l for l in lines if l.strip() and not l.strip().startswith('//')])
        
        for i, line in enumerate(lines, 1):
            for pattern, (message, severity) in self.patterns.items():
                if re.search(pattern, line):
                    self.issues.append({
                        "line": i,
                        "message": message,
                        "severity": severity,
                        "rule": "best-practice"
                    })
        
        return {
            "issues": self.issues,
            "metrics": self.metrics,
            "score": self.calculate_score()
        }