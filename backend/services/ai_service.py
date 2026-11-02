"""
AI Service Abstraction: Manages AI interactions, prompt formatting, JSON response validation,
and adaptive learning suggestions without hardcoding LLM dependencies.
"""
import json
import logging
from typing import Dict, Any, List, Optional
from ai.llm_service import get_llm_provider, BaseLLMProvider
from ai.prompts.roadmap_prompt import create_roadmap_prompt
from ai.prompts.task_prompt import create_task_prompt
from ai.prompts.project_prompt import create_project_prompt

logger = logging.getLogger(__name__)


class AIService:
    """Core AI abstraction orchestrating LLM calls, validations, and adaptive logic."""

    def __init__(self, provider: Optional[BaseLLMProvider] = None):
        self.provider = provider or get_llm_provider()

    def _safe_parse_json(self, raw_text: str, default: Dict[str, Any]) -> Dict[str, Any]:
        """Safely parses JSON output from LLM, stripping markdown delimiters if present."""
        if not raw_text:
            return default
        cleaned = raw_text.strip()
        # Remove markdown code fence if wrapped
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode AI response as JSON: {e}\nRaw output: {raw_text[:200]}")
            return default

    def generate_roadmap(
        self,
        name: str,
        education: str,
        experience_level: str,
        target_career: str,
        available_hours_per_day: float,
        timeline_months: int,
        known_skills: List[str],
        missing_skills: List[str]
    ) -> Dict[str, Any]:
        """Generates a personalized, structured learning roadmap."""
        prompt = create_roadmap_prompt(
            name=name,
            education=education,
            experience_level=experience_level,
            target_career=target_career,
            available_hours_per_day=available_hours_per_day,
            timeline_months=timeline_months,
            known_skills=known_skills,
            missing_skills=missing_skills
        )
        try:
            raw_response = self.provider.generate_completion(prompt)
            data = self._safe_parse_json(raw_response, default={})
            if "monthly_modules" in data:
                return data
        except Exception as e:
            logger.error(f"Error in LLM roadmap generation: {e}")

        # Fallback to intelligent generator if external LLM failed
        from ai.llm_service import MockLLMProvider
        fallback = MockLLMProvider()
        return json.loads(fallback._generate_roadmap_json(prompt))

    def generate_tasks(
        self,
        target_career: str,
        available_hours_per_day: float,
        current_topic: str,
        missing_skills: List[str]
    ) -> Dict[str, Any]:
        """Generates daily study tasks divided into Theory, Coding, and Practice."""
        prompt = create_task_prompt(
            target_career=target_career,
            available_hours_per_day=available_hours_per_day,
            current_topic=current_topic,
            missing_skills=missing_skills
        )
        try:
            raw_response = self.provider.generate_completion(prompt)
            data = self._safe_parse_json(raw_response, default={})
            if "tasks" in data:
                return data
        except Exception as e:
            logger.error(f"Error in LLM task generation: {e}")

        from ai.llm_service import MockLLMProvider
        fallback = MockLLMProvider()
        return json.loads(fallback._generate_tasks_json(prompt))

    def generate_projects(
        self,
        target_career: str,
        known_skills: List[str],
        missing_skills: List[str],
        experience_level: str
    ) -> Dict[str, Any]:
        """Generates Mini, Intermediate, and Capstone projects."""
        prompt = create_project_prompt(
            target_career=target_career,
            known_skills=known_skills,
            missing_skills=missing_skills,
            experience_level=experience_level
        )
        try:
            raw_response = self.provider.generate_completion(prompt)
            data = self._safe_parse_json(raw_response, default={})
            if "projects" in data:
                return data
        except Exception as e:
            logger.error(f"Error in LLM project generation: {e}")

        from ai.llm_service import MockLLMProvider
        fallback = MockLLMProvider()
        return json.loads(fallback._generate_projects_json(prompt))

    def explain_recommendation(
        self,
        target_career: str,
        confidence_score: float,
        known_skills: List[str],
        missing_skills: List[str]
    ) -> str:
        """Explains why a career path was recommended based on skill overlap."""
        prompt = f"Explain why {target_career} is recommended given known skills: {known_skills} and confidence score: {confidence_score}."
        try:
            raw_response = self.provider.generate_completion(prompt)
            data = self._safe_parse_json(raw_response, default={})
            if "explanation" in data:
                return data["explanation"]
        except Exception as e:
            logger.error(f"Error in explanation generation: {e}")

        return (
            f"Your proficiency in {', '.join(known_skills[:3]) if known_skills else 'programming'} "
            f"provides a strong springboard for {target_career}. Addressing the remaining "
            f"{len(missing_skills)} core requirements ({', '.join(missing_skills[:3])}) will qualify you for top-tier roles."
        )

    def get_adaptive_recommendation(
        self,
        completed_skills: List[str],
        completed_tasks_count: int,
        target_career: str
    ) -> Dict[str, str]:
        """
        Adaptive Learning Engine: Suggests next high-leverage topics or additional practice
        dynamically evolving with candidate completion progress.
        """
        completed_set = set([s.lower() for s in completed_skills])

        # Adaptive progression logic
        if {"python", "pandas", "numpy"}.issubset(completed_set) and "statistics" not in completed_set:
            return {
                "action": "Next Logical Topic",
                "recommendation": "You have mastered data manipulation (Python, Pandas, NumPy)! Next Recommended Topic: Descriptive & Inferential Statistics.",
                "difficulty": "Intermediate"
            }
        elif {"statistics", "machine learning"}.issubset(completed_set) and "model evaluation" not in completed_set:
            return {
                "action": "Advanced Topic Unlock",
                "recommendation": "Great job on core ML algorithms! Next Recommended Topic: Model Evaluation, Cross-Validation, and Bias-Variance Trade-off.",
                "difficulty": "Intermediate"
            }
        elif {"html", "css", "javascript"}.issubset(completed_set) and "react" not in completed_set:
            return {
                "action": "Framework Progression",
                "recommendation": "Vanilla web fundamentals complete! Next Recommended Topic: React Component Architecture and Hooks.",
                "difficulty": "Intermediate"
            }
        elif {"fastapi", "sql"}.issubset(completed_set) and "docker" not in completed_set:
            return {
                "action": "DevOps Integration",
                "recommendation": "Backend endpoints ready! Next Recommended Topic: Containerizing APIs with Docker.",
                "difficulty": "Intermediate"
            }
        elif completed_tasks_count == 0:
            return {
                "action": "Getting Started",
                "recommendation": "Start with Month 1, Week 1 daily theory tasks to establish conceptual grounding.",
                "difficulty": "Beginner"
            }
        else:
            return {
                "action": "Milestone Momentum",
                "recommendation": f"Outstanding momentum with {len(completed_skills)} skills validated. Continue daily coding exercises and transition towards the Intermediate Project.",
                "difficulty": "Advanced"
            }

