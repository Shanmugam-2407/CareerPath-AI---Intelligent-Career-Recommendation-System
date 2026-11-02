"""
Roadmap, Progress, and History API routes.
"""
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from backend.schemas.roadmap import (
    RoadmapGenerateRequest,
    ProgressUpdateRequest,
    ProgressResponse
)
from backend.services.roadmap_service import RoadmapService

router = APIRouter(prefix="/api", tags=["Roadmap & Progress"])
roadmap_service = RoadmapService()


@router.post("/roadmap/generate")
def generate_roadmap(req: RoadmapGenerateRequest):
    """Generates personalized roadmap, daily tasks, and tiered projects."""
    try:
        profile_dict = req.model_dump()
        full_plan = roadmap_service.generate_full_career_plan(
            profile=profile_dict,
            target_career=req.target_career
        )
        return full_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate roadmap: {str(e)}")


@router.get("/roadmap")
def get_current_roadmap():
    """Retrieves current active roadmap from storage."""
    data = roadmap_service.get_current_roadmap()
    if not data:
        raise HTTPException(status_code=404, detail="No active roadmap found. Please generate one.")
    return data


@router.get("/progress", response_model=ProgressResponse)
def get_progress():
    """Gets candidate progress and adaptive learning recommendations."""
    try:
        return roadmap_service.get_progress()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve progress: {str(e)}")


@router.put("/progress", response_model=ProgressResponse)
def update_progress(req: ProgressUpdateRequest):
    """Updates completed skills, tasks, and projects."""
    try:
        return roadmap_service.update_progress(
            completed_skills=req.completed_skills,
            completed_tasks=req.completed_tasks,
            completed_projects=req.completed_projects
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update progress: {str(e)}")


@router.get("/history", response_model=List[Dict[str, Any]])
def get_generation_history():
    """Retrieves recent career path generation history."""
    try:
        return roadmap_service.get_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load history: {str(e)}")

