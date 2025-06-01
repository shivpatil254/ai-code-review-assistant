from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class LanguageEnum(str, Enum):
    python = "python"
    java = "java"
    javascript = "javascript"
    typescript = "typescript"

class SeverityEnum(str, Enum):
    error = "error"
    warning = "warning"
    info = "info"

class CodeIssue(BaseModel):
    line: int
    column: Optional[int] = None
    message: str
    severity: SeverityEnum
    rule: Optional[str] = None
    suggestion: Optional[str] = None

class CodeMetrics(BaseModel):
    lines_of_code: int
    cyclomatic_complexity: float
    maintainability_index: float
    code_duplication: float
    test_coverage: Optional[float] = None
    dependencies: Optional[List[str]] = []

class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Source code to analyze")
    language: LanguageEnum
    filename: Optional[str] = "untitled"
    enable_ai: bool = True
    
    @validator('code')
    def validate_code(cls, v):
        if not v.strip():
            raise ValueError('Code cannot be empty')
        return v

class CodeAnalysisResponse(BaseModel):
    filename: str
    language: str
    score: float = Field(..., ge=0, le=100)
    issues: List[CodeIssue]
    metrics: CodeMetrics
    ai_suggestions: List[str]
    analysis_time: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ReviewHistory(BaseModel):
    id: int
    filename: str
    language: str
    score: float
    issues_count: int
    created_at: datetime
    
    class Config:
        orm_mode = True
        
    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            filename=obj.filename,
            language=obj.language,
            score=obj.score,
            issues_count=len(obj.issues) if obj.issues else 0,
            created_at=obj.created_at
        )