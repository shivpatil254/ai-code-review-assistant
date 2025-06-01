import time
import asyncio
from typing import Dict, Any, Optional, List
from ..analyzers.python_analyzer import PythonAnalyzer
from ..analyzers.java_analyzer import JavaAnalyzer
from ..analyzers.javascript_analyzer import JavaScriptAnalyzer
from .ai_service import AIService

class CodeAnalysisService:
    """Main service for code analysis"""
    
    def __init__(self):
        self.analyzers = {
            "python": PythonAnalyzer(),
            "java": JavaAnalyzer(),
            "javascript": JavaScriptAnalyzer(),
            "typescript": JavaScriptAnalyzer(),  # Reuse JS analyzer
        }
        self.ai_service = AIService()
    
    async def analyze(
        self,
        code: str,
        language: str,
        filename: Optional[str] = None,
        enable_ai: bool = True
    ) -> Dict[str, Any]:
        """Perform comprehensive code analysis"""
        start_time = time.time()
        
        # Get appropriate analyzer
        analyzer = self.analyzers.get(language.lower())
        if not analyzer:
            raise ValueError(f"Unsupported language: {language}")
        
        # Perform basic analysis
        result = analyzer.analyze(code)
        
        # Add AI suggestions if enabled
        if enable_ai:
            ai_suggestions = await self.ai_service.get_suggestions(
                code=code,
                language=language,
                issues=result["issues"]
            )
            result["ai_suggestions"] = ai_suggestions
        else:
            result["ai_suggestions"] = self._get_generic_suggestions(language)
        
        # Add metadata
        result["filename"] = filename or "untitled"
        result["language"] = language
        result["analysis_time"] = time.time() - start_time
        
        return result
    
    def detect_language(self, filename: str) -> str:
        """Auto-detect language from file extension"""
        extensions = {
            ".py": "python",
            ".java": "java",
            ".js": "javascript",
            ".ts": "typescript",
            ".jsx": "javascript",
            ".tsx": "typescript"
        }
        
        for ext, lang in extensions.items():
            if filename.lower().endswith(ext):
                return lang
        
        return "python"  # Default
    
    def _get_generic_suggestions(self, language: str) -> List[str]:
        """Get generic suggestions based on language"""
        suggestions = {
            "python": [
                "Consider adding type hints for better code documentation",
                "Use virtual environments for dependency management",
                "Follow PEP 8 style guidelines",
                "Add comprehensive unit tests with pytest",
                "Consider using dataclasses for data structures"
            ],
            "java": [
                "Follow Java naming conventions",
                "Use dependency injection for better testability",
                "Consider using Optional to handle null values",
                "Add JavaDoc comments to public methods",
                "Use Spring Boot best practices for REST APIs"
            ],
            "javascript": [
                "Use TypeScript for better type safety",
                "Follow Angular style guide for consistent code",
                "Implement proper error handling with try-catch",
                "Use async/await instead of callbacks",
                "Consider using RxJS for reactive programming"
            ]
        }
        
        return suggestions.get(language, [
            "Follow language-specific best practices",
            "Add comprehensive documentation",
            "Implement proper error handling",
            "Write unit tests for critical functions"
        ])