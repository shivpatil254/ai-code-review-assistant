# app/main.py
from sqlalchemy import func
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime

from .models import CodeReview, init_db
from .schemas import CodeAnalysisRequest, CodeAnalysisResponse, ReviewHistory
from .services.code_service import CodeAnalysisService
from .database import get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Code Review Assistant",
    description="Enterprise-grade code analysis tool with AI-powered suggestions",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
     allow_origins=[
        "http://localhost:4200",
        "http://localhost:3000",
        "https://shivpatil254.github.io",  # Add your GitHub Pages URL
        "*"  # Or temporarily allow all
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Initialize services
code_service = CodeAnalysisService()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("AI Code Review Assistant starting up...")
    logger.info("Services initialized successfully")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Code Review Assistant",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/v1/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(
    request: CodeAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze code and provide AI-powered suggestions
    
    Supports: Python, Java, JavaScript/TypeScript
    """
    try:
        # Perform analysis
        result = await code_service.analyze(
            code=request.code,
            language=request.language,
            filename=request.filename,
            enable_ai=request.enable_ai
        )
        
        # Store in database
        review = CodeReview(
            filename=request.filename or "untitled",
            language=request.language,
            code=request.code,
            score=result["score"],
            issues=result["issues"],
            metrics=result["metrics"],
            ai_suggestions=result["ai_suggestions"]
        )
        db.add(review)
        db.commit()
        
        return CodeAnalysisResponse(**result)
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze-file")
async def analyze_file(
    file: UploadFile = File(...),
    language: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Analyze uploaded code file"""
    try:
        content = await file.read()
        code = content.decode('utf-8')
        
        # Auto-detect language if not provided
        if not language:
            language = code_service.detect_language(file.filename)
        
        result = await code_service.analyze(
            code=code,
            language=language,
            filename=file.filename,
            enable_ai=True
        )
        
        # Store in database
        review = CodeReview(
            filename=file.filename,
            language=language,
            code=code,
            score=result["score"],
            issues=result["issues"],
            metrics=result["metrics"],
            ai_suggestions=result["ai_suggestions"]
        )
        db.add(review)
        db.commit()
        
        return CodeAnalysisResponse(**result)
        
    except Exception as e:
        logger.error(f"File analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/history", response_model=List[ReviewHistory])
async def get_review_history(
    skip: int = 0,
    limit: int = 10,
    language: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get code review history with pagination"""
    query = db.query(CodeReview)
    
    if language:
        query = query.filter(CodeReview.language == language)
    
    reviews = query.order_by(CodeReview.created_at.desc()).offset(skip).limit(limit).all()
    
    return [ReviewHistory.from_orm(review) for review in reviews]

@app.get("/api/v1/metrics/summary")
async def get_metrics_summary(db: Session = Depends(get_db)):
    """Get aggregated metrics summary"""
    total_reviews = db.query(CodeReview).count()
    avg_score = db.query(func.avg(CodeReview.score)).scalar() or 0
    
    language_stats = db.query(
        CodeReview.language,
        func.count(CodeReview.id).label('count'),
        func.avg(CodeReview.score).label('avg_score')
    ).group_by(CodeReview.language).all()
    
    return {
        "total_reviews": total_reviews,
        "average_score": round(avg_score, 2),
        "language_statistics": [
            {
                "language": lang,
                "count": count,
                "average_score": round(avg, 2)
            }
            for lang, count, avg in language_stats
        ]
    }

@app.delete("/api/v1/history/{review_id}")
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    """Delete a specific review"""
    review = db.query(CodeReview).filter(CodeReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.delete(review)
    db.commit()
    
    return {"message": "Review deleted successfully"}

# Error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
