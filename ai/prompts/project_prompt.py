"""
Prompt templates for generating tiered portfolio projects (Mini, Intermediate, Capstone).
"""
import json
from typing import List


def create_project_prompt(
    target_career: str,
    known_skills: List[str],
    missing_skills: List[str],
    experience_level: str
) -> str:
    """Generates prompt for Mini, Intermediate, and Capstone projects."""
    return f"""You are a Silicon Valley engineering manager and portfolio reviewer.
Design 3 rigorous portfolio projects for a candidate targeting '{target_career}' (Experience Level: {experience_level}).
Candidate master skills: {json.dumps(known_skills)}
Skills being acquired: {json.dumps(missing_skills)}

You must design:
1. Mini Project: Beginner-level project directly cementing initial missing skills.
2. Intermediate Project: Real-world problem combining multiple full-stack/ML technologies.
3. Capstone Project: End-to-end industry-style deployment with high resume impact.

Return ONLY a valid JSON object matching the exact schema:
{{
  "target_career": "{target_career}",
  "projects": [
    {{
      "level": "Mini Project",
      "project_title": "Project Title",
      "problem_statement": "Concise industry problem statement",
      "objective": "Clear engineering objective",
      "features": ["Feature 1", "Feature 2", "Feature 3"],
      "dataset_requirement": "Dataset source or schema",
      "technologies": ["Python", "Pandas", "Streamlit"],
      "ml_ai_approach": "ML algorithms or AI architecture used",
      "development_steps": ["Step 1", "Step 2", "Step 3", "Step 4"],
      "expected_output": "Interactive app, API, or dashboard artifact",
      "resume_value": "Bullet points to put directly on resume"
    }},
    {{
      "level": "Intermediate Project",
      "project_title": "Project Title",
      "problem_statement": "...",
      "objective": "...",
      "features": [...],
      "dataset_requirement": "...",
      "technologies": [...],
      "ml_ai_approach": "...",
      "development_steps": [...],
      "expected_output": "...",
      "resume_value": "..."
    }},
    {{
      "level": "Capstone Project",
      "project_title": "Project Title",
      "problem_statement": "...",
      "objective": "...",
      "features": [...],
      "dataset_requirement": "...",
      "technologies": [...],
      "ml_ai_approach": "...",
      "development_steps": [...],
      "expected_output": "...",
      "resume_value": "..."
    }}
  ]
}}
"""
