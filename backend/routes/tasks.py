"""
Task generation API routes.
"""
from fastapi import APIRouter, HTTPException
from backend.schemas.roadmap import TasksGenerateRequest
from backend.services.ai_service import AIService

router = APIRouter(prefix="/api/tasks", tags=["Daily Tasks"])
ai_service = AIService()


@router.post("/generate")
def generate_daily_tasks(req: TasksGenerateRequest):
    """Generates structured daily tasks divided into Theory, Coding, and Practice."""
    try:
        tasks = ai_service.generate_tasks(
            target_career=req.target_career,
            available_hours_per_day=req.study_hours,
            current_topic=req.current_topic,
            missing_skills=req.missing_skills
        )
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate tasks: {str(e)}")
