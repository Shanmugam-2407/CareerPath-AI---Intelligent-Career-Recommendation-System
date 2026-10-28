"""
Career, ML prediction, and NLP skill gap routes.
"""
from fastapi import APIRouter, HTTPException
from backend.schemas.career import (
    CareerPredictRequest,
    CareerPredictResponse,
    SkillAnalysisRequest,
    SkillAnalysisResponse,
    SkillGapRequest,
    SkillGapResponse
)
from backend.services.career_service import CareerService
from backend.services.skill_gap_service import SkillGapService

router = APIRouter(prefix="/api", tags=["Career & Skills"])
career_service = CareerService()
skill_gap_service = SkillGapService()


@router.post("/career/predict", response_model=CareerPredictResponse)
def predict_career_domain(req: CareerPredictRequest):
    """Predicts career domains using trained ML model and TF-IDF vectorizer."""
    try:
        result = career_service.predict_career(
            skills=req.skills,
            interests=req.interests or "",
            education=req.education or "",
            free_text=req.free_text or ""
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ML Prediction failed: {str(e)}")


@router.post("/skills/analyze", response_model=SkillAnalysisResponse)
def analyze_skills_from_text(req: SkillAnalysisRequest):
    """Extracts and normalizes technical skills from free-form text using NLP."""
    try:
        result = career_service.analyze_free_text_skills(req.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skill analysis failed: {str(e)}")


@router.post("/skills/gap", response_model=SkillGapResponse)
def analyze_skill_gap(req: SkillGapRequest):
    """Analyzes skill gaps and computes match percentage against target career requirements."""
    try:
        result = skill_gap_service.analyze_skill_gap(
            user_skills=req.user_skills,
            target_career=req.target_career,
            free_text=req.free_text or ""
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skill gap analysis failed: {str(e)}")
