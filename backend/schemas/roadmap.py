"""
Pydantic schemas for roadmaps, daily tasks, tiered projects, and progress tracking.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class RoadmapGenerateRequest(BaseModel):
    name: str = Field(..., min_length=2)
    education: str = Field(...)
    experience_level: str = Field(default="Beginner")
    target_career: str = Field(...)
    study_hours: float = Field(default=3.0, ge=0.5, le=16.0)
    timeline_months: int = Field(default=6, ge=1, le=36)
    skills: List[str] = Field(default_factory=list)
    free_text: Optional[str] = Field(default="")


class WeekPlan(BaseModel):
    week: int
    title: str
    topics: List[str]
    key_milestone: str


class MonthModule(BaseModel):
    month: int
    title: str
    focus_skills: List[str]
    learning_objective: str
    weeks: List[WeekPlan]


class RoadmapDetail(BaseModel):
    candidate_name: str
    target_career: str
    timeline_months: int
    weekly_study_hours: float
    overview: str
    monthly_modules: List[MonthModule]


class TaskItem(BaseModel):
    task_title: str
    task_type: str
    description: str
    estimated_duration: str
    difficulty: str
    topic: str
    expected_outcome: str


class ProjectItem(BaseModel):
    level: str
    project_title: str
    problem_statement: str
    objective: str
    features: List[str]
    dataset_requirement: str
    technologies: List[str]
    ml_ai_approach: str
    development_steps: List[str]
    expected_output: str
    resume_value: str


class TasksGenerateRequest(BaseModel):
    target_career: str
    study_hours: float = Field(default=3.0)
    current_topic: str = Field(default="Core Engineering")
    missing_skills: List[str] = Field(default_factory=list)


class ProjectsGenerateRequest(BaseModel):
    target_career: str
    known_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    experience_level: str = Field(default="Beginner")


class ProgressUpdateRequest(BaseModel):
    completed_skills: Optional[List[str]] = None
    completed_tasks: Optional[List[str]] = None
    completed_projects: Optional[List[str]] = None


class ProgressResponse(BaseModel):
    plan_id: Optional[str] = None
    target_career: Optional[str] = None
    overall_completion_percentage: float
    completed_skills: List[str] = Field(default_factory=list)
    remaining_skills: List[str] = Field(default_factory=list)
    completed_tasks: List[str] = Field(default_factory=list)
    completed_projects: List[str] = Field(default_factory=list)
    last_updated: Optional[str] = None
    adaptive_recommendation: Optional[Dict[str, Any]] = None

