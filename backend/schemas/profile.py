"""
Pydantic schemas for user profile data and validation.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class UserProfileCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name of candidate")
    education: str = Field(..., min_length=2, max_length=150, description="Current qualification or degree")
    experience_level: str = Field(default="Beginner", description="Beginner, Intermediate, or Experienced")
    skills: List[str] = Field(default_factory=list, description="List of technical skills and programming languages")
    interests: str = Field(default="", max_length=500, description="Areas of technical passion or interest")
    career_goal: Optional[str] = Field(default="", max_length=150, description="Target job title or career goal")
    preferred_domain: Optional[str] = Field(default="", max_length=100, description="Preferred industry domain")
    study_hours: float = Field(default=3.0, ge=0.5, le=16.0, description="Available study hours per day")
    timeline_months: int = Field(default=6, ge=1, le=36, description="Target timeline in months")
    current_projects: Optional[str] = Field(default="", max_length=1000, description="Current or previous projects")
    free_text: Optional[str] = Field(default="", max_length=2000, description="Free-text career background prompt")


class UserProfileResponse(UserProfileCreate):
    normalized_skills: List[str] = Field(default_factory=list)
    created_at: Optional[str] = None

