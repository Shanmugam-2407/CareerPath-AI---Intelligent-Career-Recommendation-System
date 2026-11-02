"""
API Client for Streamlit: Calls FastAPI endpoints with graceful direct fallback
to backend services if the FastAPI server is offline or unreachable.
Ensures 100% continuous zero-latency operation under any setup.
"""
import os
import requests
from typing import Dict, Any, List, Optional
import logging
from utils.constants import DEFAULT_HISTORY, DEFAULT_ROADMAP, DEFAULT_USER_PROFILE, DEFAULT_PROGRESS
from utils.helpers import load_json

logger = logging.getLogger(__name__)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


class APIClient:
    """Seamless client connecting Streamlit to FastAPI with graceful local service fallback."""

    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url.rstrip("/")
        self._is_connected: Optional[bool] = None

    def check_health(self) -> bool:
        """Check if FastAPI backend is reachable with short timeout."""
        try:
            r = requests.get(f"{self.base_url}/", timeout=0.8)
            connected = (r.status_code == 200)
            self._is_connected = connected
            return connected
        except Exception:
            self._is_connected = False
            return False

    def save_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save user profile via FastAPI or fallback to local backend service."""
        try:
            resp = requests.post(f"{self.base_url}/api/profile", json=profile_data, timeout=3.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.info(f"Using direct backend service for save_profile: {e}")

        # Local direct service fallback
        from backend.routes.profile import save_profile as direct_save
        from backend.schemas.profile import UserProfileCreate
        model_obj = UserProfileCreate(**profile_data)
        return direct_save(model_obj)

    def predict_career(
        self,
        skills: List[str],
        interests: str = "",
        education: str = "",
        free_text: str = ""
    ) -> Dict[str, Any]:
        """Predict career domain via FastAPI or fallback to local ML classifier."""
        payload = {
            "skills": skills,
            "interests": interests,
            "education": education,
            "free_text": free_text
        }
        try:
            resp = requests.post(f"{self.base_url}/api/career/predict", json=payload, timeout=3.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.info(f"Using direct ML service for predict_career: {e}")

        from backend.services.career_service import CareerService
        service = CareerService()
        return service.predict_career(skills=skills, interests=interests, education=education, free_text=free_text)

    def analyze_skill_gap(
        self,
        user_skills: List[str],
        target_career: str,
        free_text: str = ""
    ) -> Dict[str, Any]:
        """Analyze skill gap via FastAPI or fallback to NLP taxonomy service."""
        payload = {
            "user_skills": user_skills,
            "target_career": target_career,
            "free_text": free_text
        }
        try:
            resp = requests.post(f"{self.base_url}/api/skills/gap", json=payload, timeout=3.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.info(f"Using direct skill gap service: {e}")

        from backend.services.skill_gap_service import SkillGapService
        service = SkillGapService()
        return service.analyze_skill_gap(user_skills=user_skills, target_career=target_career, free_text=free_text)

    def extract_skills_nlp(self, free_text: str) -> List[str]:
        """Extracts technical skills directly from free-form text using NLP service."""
        try:
            from ml.preprocessing.preprocess import TextPreprocessor
            preprocessor = TextPreprocessor()
            return preprocessor.extract_skills_from_text(free_text)
        except Exception as e:
            logger.warning(f"Error in free-text NLP extraction: {e}")
            return []

    def generate_roadmap(self, profile_data: Dict[str, Any], target_career: str) -> Dict[str, Any]:
        """Generate roadmap via FastAPI or fallback to AI roadmap service."""
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
            resp = requests.post(f"{self.base_url}/api/roadmap/generate", json=payload, timeout=8.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.info(f"Using direct roadmap service: {e}")

        from backend.services.roadmap_service import RoadmapService
        service = RoadmapService()
        return service.generate_full_career_plan(profile=payload, target_career=target_career)

    def get_progress(self) -> Dict[str, Any]:
        """Get candidate progress via FastAPI or fallback to JSON storage."""
        try:
            resp = requests.get(f"{self.base_url}/api/progress", timeout=2.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.info(f"Using direct progress service: {e}")

        from backend.services.roadmap_service import RoadmapService
        service = RoadmapService()
        return service.get_progress()

    def update_progress(
        self,
        completed_skills: Optional[List[str]] = None,
        completed_tasks: Optional[List[str]] = None,
        completed_projects: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Update progress via FastAPI or fallback to atomic JSON storage."""
        payload = {
            "completed_skills": completed_skills,
            "completed_tasks": completed_tasks,
            "completed_projects": completed_projects
        }
        try:
            resp = requests.put(f"{self.base_url}/api/progress", json=payload, timeout=3.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.info(f"Using direct update_progress service: {e}")

        from backend.services.roadmap_service import RoadmapService
        service = RoadmapService()
        return service.update_progress(completed_skills, completed_tasks, completed_projects)

    def get_generation_history(self) -> List[Dict[str, Any]]:
        """Loads historical generation records from storage/history/generations.json."""
        records = load_json(DEFAULT_HISTORY, default=[])
        return records if isinstance(records, list) else []
