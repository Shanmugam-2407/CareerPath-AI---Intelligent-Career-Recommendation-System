"""
Roadmap Service: Handles end-to-end roadmap synthesis, daily tasks, tiered project generation,
and manages persistence in storage/roadmaps/, storage/progress/, and storage/history/.
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from backend.services.ai_service import AIService
from backend.services.skill_gap_service import SkillGapService
from utils.constants import DEFAULT_ROADMAP, DEFAULT_PROGRESS, DEFAULT_HISTORY, DEFAULT_USER_PROFILE
from utils.helpers import save_json, load_json, update_json


class RoadmapService:
    """Manages generation, storage, and retrieval of roadmaps, tasks, and progress."""

    def __init__(self):
        self.ai_service = AIService()
        self.skill_gap_service = SkillGapService()

    def generate_full_career_plan(
        self,
        profile: Dict[str, Any],
        target_career: str,
        skill_gap: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Synthesizes the complete end-to-end plan:
        - Monthly/weekly personalized roadmap
        - Daily study tasks
        - Tiered projects (Mini, Intermediate, Capstone)
        - AI explanation
        - Saves to local storage
        """
        user_skills = profile.get("skills", [])
        hours = float(profile.get("study_hours", 3.0))
        timeline = int(profile.get("timeline_months", 6))
        education = profile.get("education", "Undergraduate")
        experience = profile.get("experience_level", "Beginner")
        name = profile.get("name", "Candidate")

        # 1. Compute skill gap if not provided
        if not skill_gap:
            skill_gap = self.skill_gap_service.analyze_skill_gap(
                user_skills=user_skills,
                target_career=target_career,
                free_text=profile.get("free_text", "")
            )

        known_skills = skill_gap.get("already_known", [])
        missing_skills = skill_gap.get("missing_skills", [])

        # 2. AI generates structured roadmap
        roadmap_data = self.ai_service.generate_roadmap(
            name=name,
            education=education,
            experience_level=experience,
            target_career=target_career,
            available_hours_per_day=hours,
            timeline_months=timeline,
            known_skills=known_skills,
            missing_skills=missing_skills
        )

        # 3. AI generates initial daily tasks
        first_topic = missing_skills[0] if missing_skills else "Advanced Concepts"
        tasks_data = self.ai_service.generate_tasks(
            target_career=target_career,
            available_hours_per_day=hours,
            current_topic=first_topic,
            missing_skills=missing_skills
        )

        # 4. AI generates 3-tier projects
        projects_data = self.ai_service.generate_projects(
            target_career=target_career,
            known_skills=known_skills,
            missing_skills=missing_skills,
            experience_level=experience
        )

        # 5. AI generates explanation
        explanation = self.ai_service.explain_recommendation(
            target_career=target_career,
            confidence_score=0.88,
            known_skills=known_skills,
            missing_skills=missing_skills
        )

        # 6. Bundle full payload
        plan_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()
        full_plan = {
            "plan_id": plan_id,
            "created_at": created_at,
            "user_name": name,
            "target_career": target_career,
            "available_hours_per_day": hours,
            "timeline_months": timeline,
            "skill_gap": skill_gap,
            "roadmap": roadmap_data,
            "daily_tasks": tasks_data.get("tasks", []),
            "projects": projects_data.get("projects", []),
            "ai_explanation": explanation
        }

        # Save to storage/roadmaps/roadmap.json
        save_json(DEFAULT_ROADMAP, full_plan)

        # Initialize progress file
        initial_progress = {
            "plan_id": plan_id,
            "target_career": target_career,
            "last_updated": created_at,
            "completed_skills": known_skills,
            "remaining_skills": missing_skills,
            "completed_tasks": [],
            "completed_projects": [],
            "overall_completion_percentage": round((len(known_skills) / (len(known_skills) + len(missing_skills) or 1)) * 100, 1)
        }
        save_json(DEFAULT_PROGRESS, initial_progress)

        # Append to history
        history = load_json(DEFAULT_HISTORY, default=[])
        if not isinstance(history, list):
            history = []
        history.insert(0, {
            "plan_id": plan_id,
            "target_career": target_career,
            "created_at": created_at,
            "match_percentage": skill_gap.get("match_percentage", 0)
        })
        save_json(DEFAULT_HISTORY, history[:50])  # keep last 50

        return full_plan

    def get_current_roadmap(self) -> Dict[str, Any]:
        """Loads currently active roadmap from JSON storage."""
        return load_json(DEFAULT_ROADMAP, default={})

    def get_progress(self) -> Dict[str, Any]:
        """Loads current candidate progress from JSON storage."""
        prog = load_json(DEFAULT_PROGRESS, default={})
        if not prog:
            return {
                "overall_completion_percentage": 0,
                "completed_skills": [],
                "remaining_skills": [],
                "completed_tasks": [],
                "completed_projects": [],
                "adaptive_recommendation": {
                    "action": "Getting Started",
                    "recommendation": "Configure your profile and generate your personalized roadmap to begin tracking progress."
                }
            }

        # Dynamically inject adaptive recommendation
        adaptive = self.ai_service.get_adaptive_recommendation(
            completed_skills=prog.get("completed_skills", []),
            completed_tasks_count=len(prog.get("completed_tasks", [])),
            target_career=prog.get("target_career", "Data Science")
        )
        prog["adaptive_recommendation"] = adaptive
        return prog

    def update_progress(
        self,
        completed_skills: Optional[List[str]] = None,
        completed_tasks: Optional[List[str]] = None,
        completed_projects: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Updates progress tracking metrics and calculates new completion percentage."""
        prog = load_json(DEFAULT_PROGRESS, default={})
        if not prog:
            prog = {"completed_skills": [], "remaining_skills": [], "completed_tasks": [], "completed_projects": []}

        if completed_skills is not None:
            prog["completed_skills"] = sorted(list(set(completed_skills)))
            # Recalculate remaining
            roadmap = self.get_current_roadmap()
            all_req = roadmap.get("skill_gap", {}).get("required_skills", [])
            prog["remaining_skills"] = [s for s in all_req if s not in prog["completed_skills"]]

        if completed_tasks is not None:
            prog["completed_tasks"] = sorted(list(set(completed_tasks)))

        if completed_projects is not None:
            prog["completed_projects"] = sorted(list(set(completed_projects)))

        # Calculate overall weighted completion percentage:
        # Skills 50%, Tasks 25%, Projects 25%
        roadmap = self.get_current_roadmap()
        all_req = roadmap.get("skill_gap", {}).get("required_skills", [])
        total_skills = len(all_req) or 1
        skill_score = min(len(prog["completed_skills"]) / total_skills, 1.0) * 50

        total_tasks = len(roadmap.get("daily_tasks", [])) or 1
        task_score = min(len(prog.get("completed_tasks", [])) / total_tasks, 1.0) * 25

        total_projects = len(roadmap.get("projects", [])) or 1
        proj_score = min(len(prog.get("completed_projects", [])) / total_projects, 1.0) * 25

        total_pct = round(skill_score + task_score + proj_score, 1)
        prog["overall_completion_percentage"] = min(total_pct, 100.0)
        prog["last_updated"] = datetime.now(timezone.utc).isoformat()

        save_json(DEFAULT_PROGRESS, prog)
        return self.get_progress()

    def get_history(self) -> List[Dict[str, Any]]:
        """Returns generation history."""
        hist = load_json(DEFAULT_HISTORY, default=[])
        return hist if isinstance(hist, list) else []

