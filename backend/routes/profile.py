"""
Profile API routes.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from backend.schemas.profile import UserProfileCreate, UserProfileResponse
from ml.preprocessing.preprocess import TextPreprocessor
from utils.constants import DEFAULT_USER_PROFILE
from utils.helpers import save_json, load_json
from utils.validators import sanitize_text

router = APIRouter(prefix="/api/profile", tags=["Profile"])
preprocessor = TextPreprocessor()


@router.post("", response_model=UserProfileResponse)
def save_profile(profile: UserProfileCreate):
    """Saves or updates user profile in local JSON storage."""
    try:
        # Sanitize inputs
        clean_name = sanitize_text(profile.name)
        clean_edu = sanitize_text(profile.education)
        clean_interests = sanitize_text(profile.interests)
        clean_prompt = sanitize_text(profile.free_text or "")

        # Normalize skills
        normalized_skills = preprocessor.normalize_skill_list(profile.skills)
        if clean_prompt:
            extracted = preprocessor.extract_skills_from_text(clean_prompt)
            normalized_skills = sorted(list(set(normalized_skills + extracted)))

        data = profile.model_dump()
        data["name"] = clean_name
        data["education"] = clean_edu
        data["interests"] = clean_interests
        data["free_text"] = clean_prompt
        data["normalized_skills"] = normalized_skills
        data["created_at"] = datetime.now(timezone.utc).isoformat()

        save_json(DEFAULT_USER_PROFILE, data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save profile: {str(e)}")


@router.get("", response_model=UserProfileResponse)
def get_profile():
    """Retrieves current user profile from local JSON storage."""
    profile_data = load_json(DEFAULT_USER_PROFILE, default=None)
    if not profile_data:
        raise HTTPException(status_code=404, detail="User profile not found. Please create one.")
    return profile_data

