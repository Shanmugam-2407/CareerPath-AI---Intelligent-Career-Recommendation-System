"""
Portfolio project generation API routes.
"""
from fastapi import APIRouter, HTTPException
from backend.schemas.roadmap import ProjectsGenerateRequest
from backend.services.ai_service import AIService

router = APIRouter(prefix="/api/projects", tags=["Portfolio Projects"])
ai_service = AIService()


@router.post("/generate")
def generate_portfolio_projects(req: ProjectsGenerateRequest):
    """Generates tiered Mini, Intermediate, and Capstone projects."""
    try:
        projects = ai_service.generate_projects(
            target_career=req.target_career,
            known_skills=req.known_skills,
            missing_skills=req.missing_skills,
            experience_level=req.experience_level
        )
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate projects: {str(e)}")

