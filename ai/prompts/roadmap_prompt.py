"""
Prompt templates for generating structured personalized career roadmaps.
"""
import json
from typing import List, Dict, Any


def create_roadmap_prompt(
    name: str,
    education: str,
    experience_level: str,
    target_career: str,
    available_hours_per_day: float,
    timeline_months: int,
    known_skills: List[str],
    missing_skills: List[str]
) -> str:
    """Generates the prompt string for LLM personalized roadmap generation."""
    return f"""You are an elite AI Career Architect and Senior Staff Tech Mentor.
Generate a strictly personalized, chronological, month-by-month and week-by-week learning roadmap for the candidate below.

CANDIDATE PROFILE:
- Name: {name}
- Education: {education}
- Current Experience Level: {experience_level}
- Target Career Role: {target_career}
- Daily Study Capacity: {available_hours_per_day} hours/day
- Target Timeline: {timeline_months} months
- Already Mastered Skills: {json.dumps(known_skills)}
- Identified Missing Skills To Learn: {json.dumps(missing_skills)}

STRICT REQUIREMENTS:
1. Do NOT reteach already mastered skills from scratch; build directly on them to address the missing skills.
2. Structure the roadmap across exactly {timeline_months} monthly modules.
3. Each monthly module must contain 4 distinct weeks with detailed topics and objectives.
4. Scale topic depth strictly to match {available_hours_per_day} hours/day.
5. Return ONLY a valid JSON object matching the schema below. No markdown backticks, no commentary.

SCHEMA:
{{
  "candidate_name": "{name}",
  "target_career": "{target_career}",
  "timeline_months": {timeline_months},
  "weekly_study_hours": {available_hours_per_day * 7},
  "overview": "Detailed strategic overview of this personalized journey",
  "monthly_modules": [
    {{
      "month": 1,
      "title": "Month 1 Title",
      "focus_skills": ["Skill1", "Skill2"],
      "learning_objective": "Clear target outcome for this month",
      "weeks": [
        {{
          "week": 1,
          "title": "Week 1 Theme",
          "topics": ["Topic A", "Topic B", "Topic C"],
          "key_milestone": "Practical milestone by end of week"
        }}
      ]
    }}
  ]
}}
"""

