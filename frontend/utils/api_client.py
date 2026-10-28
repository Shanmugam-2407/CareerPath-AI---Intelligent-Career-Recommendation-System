"""
API Client for Streamlit: Calls FastAPI endpoints with graceful fallback to backend services
if FastAPI backend is offline.
"""
import os
import requests
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


class APIClient:
    """Seamless client connecting Streamlit to FastAPI with graceful local service fallback."""

    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url.rstrip("/")

    def check_health(self) -> bool:
        """Check if FastAPI backend is reachable."""
        try:
            r = requests.get(f"{self.base_url}/", timeout=1.5)
            return r.status_code == 200
        except Exception:
            return False

    def save_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save user profile via FastAPI or fallback."""
        try:
            resp = requests.post(f"{self.base_url}/api/profile", json=profile_data, timeout=5.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.warning(f"FastAPI unreachable ({e}). Using direct backend service fallback.")

        # Local service fallback
        from backend.routes.profile import save_profile as direct_save
        from backend.schemas.profile import UserProfileCreate
        model_obj = UserProfileCreate(**profile_data)
        return direct_save(model_obj)

    def predict_career(self, skills: List[str], interests: str = "", education: str = "", free_text: str = "") -> Dict[str, Any]:
        """Predict career domain via FastAPI or fallback."""
        payload = {
            "skills": skills,
            "interests": interests,
            "education": education,
            "free_text": free_text
        }
        try:
            resp = requests.post(f"{self.base_url}/api/career/predict", json=payload, timeout=5.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.warning(f"FastAPI unreachable ({e}). Using direct backend service fallback.")

        from backend.services.career_service import CareerService
        service = CareerService()
        return service.predict_career(skills=skills, interests=interests, education=education, free_text=free_text)

    def analyze_skill_gap(self, user_skills: List[str], target_career: str, free_text: str = "") -> Dict[str, Any]:
        """Analyze skill gap via FastAPI or fallback."""
        payload = {
            "user_skills": user_skills,
            "target_career": target_career,
            "free_text": free_text
        }
        try:
            resp = requests.post(f"{self.base_url}/api/skills/gap", json=payload, timeout=5.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.warning(f"FastAPI unreachable ({e}). Using direct backend service fallback.")

        from backend.services.skill_gap_service import SkillGapService
        service = SkillGapService()
        return service.analyze_skill_gap(user_skills=user_skills, target_career=target_career, free_text=free_text)

    def generate_roadmap(self, profile_data: Dict[str, Any], target_career: str) -> Dict[str, Any]:
        """Generate roadmap via FastAPI or fallback."""
        payload = {
            "name": profile_data.get("name", "Candidate"),
            "education": profile_data.get("education", "Degree"),
            "experience_level": profile_data.get("experience_level", "Beginner"),
            "target_career": target_career,
            "study_hours": float(profile_data.get("study_hours", 3.0)),
            "timeline_months": int(profile_data.get("timeline_months", 6)),
            "skills": profile_data.get("skills", []),
            "free_text": profile_data.get("free_text", "")
        }
        try:
            resp = requests.post(f"{self.base_url}/api/roadmap/generate", json=payload, timeout=10.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.warning(f"FastAPI unreachable ({e}). Using direct backend service fallback.")

        from backend.services.roadmap_service import RoadmapService
        service = RoadmapService()
        return service.generate_full_career_plan(profile=payload, target_career=target_career)

    def get_progress(self) -> Dict[str, Any]:
        """Get candidate progress via FastAPI or fallback."""
        try:
            resp = requests.get(f"{self.base_url}/api/progress", timeout=5.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.warning(f"FastAPI unreachable ({e}). Using direct backend service fallback.")

        from backend.services.roadmap_service import RoadmapService
        service = RoadmapService()
        return service.get_progress()

    def update_progress(self, completed_skills=None, completed_tasks=None, completed_projects=None) -> Dict[str, Any]:
        """Update progress via FastAPI or fallback."""
        payload = {
            "completed_skills": completed_skills,
            "completed_tasks": completed_tasks,
            "completed_projects": completed_projects
        }
        try:
            resp = requests.put(f"{self.base_url}/api/progress", json=payload, timeout=5.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.warning(f"FastAPI unreachable ({e}). Using direct backend service fallback.")

        from backend.services.roadmap_service import RoadmapService
        service = RoadmapService()
        return service.update_progress(completed_skills, completed_tasks, completed_projects)
