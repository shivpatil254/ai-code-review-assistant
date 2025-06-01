import os
import asyncio
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AzureIntegrationService:
    """Mock Azure Cognitive Services integration"""
    
    def __init__(self):
        self.azure_key = os.getenv("AZURE_COGNITIVE_SERVICES_KEY", "demo-key")
        self.azure_endpoint = os.getenv("AZURE_COGNITIVE_SERVICES_ENDPOINT", "https://demo.cognitiveservices.azure.com")
        logger.info(f"Azure service initialized with endpoint: {self.azure_endpoint}")
        
    async def analyze_code_sentiment(self, code: str) -> Dict[str, Any]:
        """Analyze code quality using Azure Text Analytics (mock)"""
        # In production, this would call Azure Cognitive Services
        await asyncio.sleep(0.1)  # Simulate API call
        
        # Mock sentiment analysis based on code patterns
        negative_patterns = ["TODO", "FIXME", "HACK", "BUG", "XXX", "DEPRECATED"]
        positive_patterns = ["test", "unittest", "docstring", "type hint", "async", "logger"]
        
        negative_count = sum(1 for pattern in negative_patterns if pattern in code)
        positive_count = sum(1 for pattern in positive_patterns if pattern.lower() in code.lower())
        
        if negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.9, 0.5 + (negative_count * 0.1))
        elif positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.9, 0.5 + (positive_count * 0.1))
        else:
            sentiment = "neutral"
            confidence = 0.7
            
        return {
            "sentiment": sentiment,
            "confidence_scores": {
                "positive": confidence if sentiment == "positive" else 0.1,
                "neutral": confidence if sentiment == "neutral" else 0.2,
                "negative": confidence if sentiment == "negative" else 0.1
            },
            "detected_patterns": {
                "negative": negative_count,
                "positive": positive_count
            }
        }
    
    async def extract_key_phrases(self, code: str) -> List[str]:
        """Extract key programming concepts using Azure (mock)"""
        await asyncio.sleep(0.1)
        
        # Mock key phrase extraction based on code patterns
        key_phrases = []
        
        # Python patterns
        if "class" in code and "def" in code:
            key_phrases.append("object-oriented programming")
        if "async" in code or "await" in code:
            key_phrases.append("asynchronous programming")
        if "@" in code and "def" in code:
            key_phrases.append("decorators")
        if "lambda" in code:
            key_phrases.append("functional programming")
            
        # Java patterns
        if "public class" in code:
            key_phrases.append("Java class definition")
        if "@Autowired" in code:
            key_phrases.append("Spring dependency injection")
        if "@RestController" in code:
            key_phrases.append("REST API controller")
            
        # JavaScript patterns
        if "const" in code or "let" in code:
            key_phrases.append("modern JavaScript")
        if "=>" in code:
            key_phrases.append("arrow functions")
        if "async function" in code:
            key_phrases.append("async JavaScript")
            
        # Testing patterns
        if "test" in code.lower() or "assert" in code:
            key_phrases.append("unit testing")
            
        # API patterns
        if "api" in code.lower() or "endpoint" in code.lower():
            key_phrases.append("API development")
            
        return list(set(key_phrases))  # Remove duplicates
    
    async def detect_language_azure(self, code: str) -> Dict[str, float]:
        """Detect programming language using Azure (mock) with confidence scores"""
        await asyncio.sleep(0.1)
        
        # Language detection based on patterns
        scores = {
            "python": 0.0,
            "java": 0.0,
            "javascript": 0.0,
            "typescript": 0.0
        }
        
        # Python indicators
        if "def " in code:
            scores["python"] += 0.3
        if "import " in code and "from " in code:
            scores["python"] += 0.2
        if "__init__" in code or "self." in code:
            scores["python"] += 0.2
        if "print(" in code:
            scores["python"] += 0.1
            
        # Java indicators
        if "public class" in code or "private" in code:
            scores["java"] += 0.3
        if "System.out" in code:
            scores["java"] += 0.2
        if "@Override" in code or "@Autowired" in code:
            scores["java"] += 0.3
            
        # JavaScript/TypeScript indicators
        if "function" in code or "const " in code:
            scores["javascript"] += 0.2
        if "=>" in code:
            scores["javascript"] += 0.2
        if ": string" in code or ": number" in code:
            scores["typescript"] += 0.4
            scores["javascript"] += 0.1
            
        # Normalize scores
        total = sum(scores.values())
        if total > 0:
            for lang in scores:
                scores[lang] = scores[lang] / total
                
        return scores
    
    async def analyze_code_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity using Azure (mock)"""
        await asyncio.sleep(0.1)
        
        lines = code.split('\n')
        
        # Count various complexity indicators
        complexity_indicators = {
            "nested_loops": 0,
            "conditionals": 0,
            "functions": 0,
            "classes": 0,
            "imports": 0
        }
        
        indent_level = 0
        max_indent = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Track indentation (complexity indicator)
            if line and line[0] == ' ':
                indent_level = len(line) - len(line.lstrip())
                max_indent = max(max_indent, indent_level)
            
            # Count patterns
            if 'for ' in stripped or 'while ' in stripped:
                complexity_indicators["nested_loops"] += 1
            if 'if ' in stripped or 'elif ' in stripped:
                complexity_indicators["conditionals"] += 1
            if 'def ' in stripped or 'function ' in stripped:
                complexity_indicators["functions"] += 1
            if 'class ' in stripped:
                complexity_indicators["classes"] += 1
            if 'import ' in stripped:
                complexity_indicators["imports"] += 1
        
        # Calculate complexity score
        complexity_score = (
            complexity_indicators["nested_loops"] * 3 +
            complexity_indicators["conditionals"] * 2 +
            complexity_indicators["functions"] +
            complexity_indicators["classes"] * 2 +
            (max_indent // 4) * 2  # Penalize deep nesting
        )
        
        return {
            "complexity_score": complexity_score,
            "indicators": complexity_indicators,
            "max_nesting_level": max_indent // 4,
            "recommendation": self._get_complexity_recommendation(complexity_score)
        }
    
    def _get_complexity_recommendation(self, score: int) -> str:
        """Get recommendation based on complexity score"""
        if score < 10:
            return "Code has low complexity - good job!"
        elif score < 20:
            return "Code has moderate complexity - consider refactoring complex methods"
        elif score < 30:
            return "Code has high complexity - refactoring recommended"
        else:
            return "Code has very high complexity - consider breaking into smaller modules"