"""
Pydantic schemas for career predictions, skill analysis, and skill-gap endpoints.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class CareerPredictRequest(BaseModel):
    skills: List[str] = Field(default_factory=list, description="Candidate skills")
    interests: Optional[str] = Field(default="", description="Candidate interests")
    education: Optional[str] = Field(default="", description="Candidate degree or background")
    free_text: Optional[str] = Field(default="", description="Additional unstructured prompt")


class DomainRanking(BaseModel):
    domain: str
    probability: float
    percentage: str


class CareerPredictResponse(BaseModel):
    recommended_career: str
    confidence_score: float
    rankings: List[DomainRanking]
    model_used: str
    normalized_skills: List[str]


class SkillAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=2, description="Text containing technical skill mentions")


class SkillAnalysisResponse(BaseModel):
    raw_text: str
    extracted_skills: List[str]
    count: int


class SkillGapRequest(BaseModel):
    user_skills: List[str] = Field(default_factory=list)
    target_career: str = Field(..., min_length=2)
    free_text: Optional[str] = Field(default="")


class SkillGapResponse(BaseModel):
    target_career: str
    canonical_domain: str
    required_skills: List[str]
    already_known: List[str]
    missing_skills: List[str]
    additional_skills: List[str]
    match_percentage: float
    known_count: int
    missing_count: int
    total_required_count: int
    next_step: str
