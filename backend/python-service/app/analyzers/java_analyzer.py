import re
from typing import List, Dict, Any
from .base import BaseAnalyzer

class JavaAnalyzer(BaseAnalyzer):
    """Java code analyzer"""
    
    def __init__(self):
        super().__init__()
        self.patterns = {
            # Security
            r"Runtime\.exec": ("Potential command injection", "error"),
            r"new\s+File\s*\(": ("Consider using Path API", "info"),
            
            # Spring specific
            r"@RequestMapping.*method\s*=": ("Use @GetMapping/@PostMapping", "info"),
            r"@Autowired\s+private": ("Consider constructor injection", "warning"),
            
            # Best practices
            r"System\.out\.print": ("Use logging framework", "warning"),
            r"catch\s*\(\s*Exception\s+": ("Too broad exception handling", "warning"),
            r"public\s+static\s+[^v][^o][^i][^d]": ("Avoid public static fields", "warning"),
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