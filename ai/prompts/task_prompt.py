"""
Prompt templates for generating time-budgeted daily study tasks.
"""
import json
from typing import List


def create_task_prompt(
    target_career: str,
    available_hours_per_day: float,
    current_topic: str,
    missing_skills: List[str]
) -> str:
    """Generates the prompt string for generating daily tasks divided into Theory, Coding, and Practice."""
    return f"""You are an elite AI technical coach.
Generate daily study tasks calibrated for a study budget of {available_hours_per_day} hours/day for the topic '{current_topic}' towards becoming a '{target_career}'.

Skills to cover: {json.dumps(missing_skills)}
Budget: {available_hours_per_day} hours divided proportionately into:
- Theory & Core Concepts
- Hands-on Implementation / Coding
- Problem Solving / Practice Exercise

Return ONLY a valid JSON object matching this schema:
{{
  "topic": "{current_topic}",
  "total_daily_hours": {available_hours_per_day},
  "tasks": [
    {{
      "task_title": "Task title",
      "task_type": "Theory | Coding | Practice",
      "description": "Comprehensive step-by-step description",
      "estimated_duration": "1 hour",
      "difficulty": "Beginner | Intermediate | Advanced",
      "topic": "{current_topic}",
      "expected_outcome": "Measurable output produced by candidate"
    }}
  ]
}}
"""
