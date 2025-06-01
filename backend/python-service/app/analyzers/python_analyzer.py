import ast
import re
from typing import List, Dict, Any
from .base import BaseAnalyzer

class PythonAnalyzer(BaseAnalyzer):
    """Advanced Python code analyzer"""
    
    def __init__(self):
        super().__init__()
        self.security_patterns = {
            r"eval\s*\(": ("Avoid using eval() - security risk", "error"),
            r"exec\s*\(": ("Avoid using exec() - security risk", "error"),
            r"__import__": ("Dynamic imports can be security risk", "warning"),
            r"pickle\.loads": ("Pickle can execute arbitrary code", "warning"),
            r"subprocess.*shell\s*=\s*True": ("Shell injection risk", "error"),
        }
        
        self.quality_patterns = {
            r"except\s*:": ("Avoid bare except clauses", "warning"),
            r"except\s+Exception\s*:": ("Too broad exception handling", "warning"),
            r"from\s+\S+\s+import\s+\*": ("Avoid wildcard imports", "warning"),
            r"TODO|FIXME|XXX": ("Unresolved comment", "info"),
            r"print\s*\(": ("Consider using logging instead of print", "info"),
        }
        
        self.pep8_patterns = {
            r"^\s*\t": ("Use spaces instead of tabs", "warning"),
            r".{80,}": ("Line too long (PEP 8: 79 chars)", "info"),
            r"[a-z]+[A-Z]": ("Use snake_case for variables", "info"),
        }
    
    def analyze(self, code: str) -> Dict[str, Any]:
        """Perform comprehensive Python code analysis"""
        self.issues = []
        lines = code.split('\n')
        self.metrics["lines_of_code"] = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        
        # Security analysis
        self._check_patterns(code, self.security_patterns)
        
        # Code quality analysis
        self._check_patterns(code, self.quality_patterns)
        
        # PEP 8 compliance
        for i, line in enumerate(lines, 1):
            for pattern, (message, severity) in self.pep8_patterns.items():
                if re.search(pattern, line):
                    self.issues.append({
                        "line": i,
                        "message": message,
                        "severity": severity,
                        "rule": "PEP8"
                    })
        
        # AST-based analysis
        try:
            tree = ast.parse(code)
            self._analyze_ast(tree)
        except SyntaxError as e:
            self.issues.append({
                "line": e.lineno or 1,
                "message": f"Syntax error: {e.msg}",
                "severity": "error",
                "rule": "syntax"
            })
        
        # Calculate metrics
        self._calculate_complexity(code)
        
        return {
            "issues": self.issues,
            "metrics": self.metrics,
            "score": self.calculate_score()
        }
    
    def _check_patterns(self, code: str, patterns: Dict[str, tuple]):
        """Check code against regex patterns"""
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern, (message, severity) in patterns.items():
                if re.search(pattern, line):
                    self.issues.append({
                        "line": i,
                        "message": message,
                        "severity": severity,
                        "rule": pattern.split('\\')[0]
                    })
    
    def _analyze_ast(self, tree: ast.AST):
        """Perform AST-based analysis"""
        class Visitor(ast.NodeVisitor):
            def __init__(self, analyzer):
                self.analyzer = analyzer
                self.function_count = 0
                self.class_count = 0
            
            def visit_FunctionDef(self, node):
                self.function_count += 1
                # Check for missing docstring
                if not ast.get_docstring(node):
                    self.analyzer.issues.append({
                        "line": node.lineno,
                        "message": f"Function '{node.name}' missing docstring",
                        "severity": "info",
                        "rule": "docstring"
                    })
                
                # Check function complexity
                if len(node.body) > 20:
                    self.analyzer.issues.append({
                        "line": node.lineno,
                        "message": f"Function '{node.name}' is too complex",
                        "severity": "warning",
                        "rule": "complexity"
                    })
                
                self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                self.class_count += 1
                if not ast.get_docstring(node):
                    self.analyzer.issues.append({
                        "line": node.lineno,
                        "message": f"Class '{node.name}' missing docstring",
                        "severity": "info",
                        "rule": "docstring"
                    })
                self.generic_visit(node)
        
        visitor = Visitor(self)
        visitor.visit(tree)
    
    def _calculate_complexity(self, code: str):
        """Calculate cyclomatic complexity and other metrics"""
        # Simple complexity calculation
        complexity = 1
        complexity += code.count('if ')
        complexity += code.count('elif ')
        complexity += code.count('else:')
        complexity += code.count('for ')
        complexity += code.count('while ')
        complexity += code.count('except ')
        
        self.metrics["cyclomatic_complexity"] = complexity
        
        # Maintainability index (simplified)
        loc = self.metrics["lines_of_code"]
        if loc > 0:
            self.metrics["maintainability_index"] = max(0, 100 - (complexity * 2) - (loc / 10))
