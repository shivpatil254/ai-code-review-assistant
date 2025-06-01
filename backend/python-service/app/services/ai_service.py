import asyncio
import random
from typing import List, Dict, Any
from .azure_service import AzureIntegrationService  # ADD THIS IMPORT

class AIService:
    """AI service for intelligent code suggestions"""
    
    def __init__(self):
        self.azure_service = AzureIntegrationService()  # ADD THIS LINE
        # ... rest of your existing __init__ code ...
        self.patterns = {
            "security": [
                "Implement input validation to prevent injection attacks",
                "Use parameterized queries to prevent SQL injection",
                "Sanitize user input before processing",
                "Implement proper authentication and authorization",
                "Use HTTPS for all sensitive data transmission"
            ],
            "performance": [
                "Consider caching frequently accessed data",
                "Optimize database queries with proper indexing",
                "Use lazy loading for better performance",
                "Implement pagination for large datasets",
                "Consider using async/await for I/O operations"
            ],
            "maintainability": [
                "Extract complex logic into separate functions",
                "Add comprehensive documentation and comments",
                "Follow SOLID principles for better design",
                "Implement proper logging for debugging",
                "Use design patterns where appropriate"
            ],
            "testing": [
                "Add unit tests for all public methods",
                "Implement integration tests for API endpoints",
                "Use mocking for external dependencies",
                "Aim for at least 80% code coverage",
                "Consider test-driven development (TDD)"
            ]
        }
    
    async def get_suggestions(
        self,
        code: str,
        language: str,
        issues: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate AI-powered suggestions based on code analysis"""
        
        # Get Azure insights
        sentiment_result = await self.azure_service.analyze_code_sentiment(code)
        key_phrases = await self.azure_service.extract_key_phrases(code)
        complexity_result = await self.azure_service.analyze_code_complexity(code)
        
        suggestions = []
        
        # Add suggestions based on sentiment
        if sentiment_result['sentiment'] == 'negative':
            suggestions.append("Consider addressing TODO/FIXME comments to improve code quality")
            suggestions.append("Refactor sections with technical debt markers")
        elif sentiment_result['sentiment'] == 'positive':
            suggestions.append("Good use of testing and documentation practices")
        
        # Add suggestions based on complexity
        suggestions.append(complexity_result['recommendation'])
        
        # Add suggestions based on key phrases
        if "object-oriented programming" in key_phrases:
            suggestions.append("Ensure SOLID principles are followed in class design")
        if "asynchronous programming" in key_phrases:
            suggestions.append("Consider using asyncio best practices and proper error handling")
        if "API development" in key_phrases:
            suggestions.append("Implement API versioning and comprehensive documentation")
        
        # Analyze issues and provide targeted suggestions (existing code)
        issue_types = set()
        for issue in issues:
            if "security" in issue.get("message", "").lower():
                issue_types.add("security")
            elif "performance" in issue.get("message", "").lower():
                issue_types.add("performance")
            else:
                issue_types.add("maintainability")
        
        # Add suggestions based on issues found
        for issue_type in issue_types:
            if issue_type in self.patterns:
                suggestions.extend(random.sample(
                    self.patterns[issue_type],
                    min(2, len(self.patterns[issue_type]))
                ))
        
        # Add language-specific suggestions with Azure insights
        if language == "python":
            suggestions.append("Consider using Python 3.11+ for better performance")
            if "async" not in code and complexity_result['complexity_score'] > 15:
                suggestions.append("Consider using async/await for I/O-bound operations")
        elif language == "java":
            suggestions.append("Use Spring Boot 3.0+ for modern Java development")
            if "@Service" not in code and "@Component" not in code and "Spring" in str(key_phrases):
                suggestions.append("Consider using Spring annotations for dependency injection")
        elif language in ["javascript", "typescript"]:
            suggestions.append("Use modern ES6+ features for cleaner code")
            if "angular" in code.lower():
                suggestions.append("Follow Angular best practices for component design")
        
        # Ensure we don't have duplicates and limit to top suggestions
        unique_suggestions = list(dict.fromkeys(suggestions))  # Preserve order while removing duplicates
        return unique_suggestions[:7]  # Return top 7 suggestions