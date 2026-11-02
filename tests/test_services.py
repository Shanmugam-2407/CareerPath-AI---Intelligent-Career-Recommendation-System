"""
Unit tests for NLP skill analysis, skill-gap calculations, local storage, and AI service.
"""
import pytest
from pathlib import Path
from ml.preprocessing.preprocess import TextPreprocessor, SkillSimilarityMatcher
from backend.services.skill_gap_service import SkillGapService
from backend.services.ai_service import AIService
from utils.helpers import save_json, load_json, update_json


def test_skill_normalization():
    preprocessor = TextPreprocessor()
    raw = ["python programming", "reactjs", "postgres", "stats", "k8s"]
    normalized = preprocessor.normalize_skill_list(raw)
    assert "Python" in normalized
    assert "React" in normalized
    assert "PostgreSQL" in normalized
    assert "Statistics" in normalized
    assert "Kubernetes" in normalized


def test_nlp_skill_extraction_from_prompt():
    preprocessor = TextPreprocessor()
    text = (
        "I am a final-year B.Tech IT student. I know Python, SQL, HTML and CSS. "
        "I am interested in AI and data. I can study 3 hours per day."
    )
    extracted = preprocessor.extract_skills_from_text(text)
    assert "Python" in extracted
    assert "SQL" in extracted
    assert "HTML" in extracted
    assert "CSS" in extracted


def test_skill_gap_analysis():
    service = SkillGapService()
    user_skills = ["Python", "SQL", "Pandas", "HTML"]
    target = "Data Scientist"

    result = service.analyze_skill_gap(user_skills=user_skills, target_career=target)
    assert result["canonical_domain"] == "Data Science"
    assert "Python" in result["already_known"]
    assert "SQL" in result["already_known"]
    assert "Pandas" in result["already_known"]
    assert "Machine Learning" in result["missing_skills"]
    assert result["match_percentage"] > 0
    assert result["match_percentage"] < 100


def test_json_storage_operations(tmp_path):
    test_file = tmp_path / "test_store.json"
    data = {"candidate": "Jane Doe", "score": 95}

    # Save
    assert save_json(test_file, data) is True
    assert test_file.exists()

    # Load
    loaded = load_json(test_file)
    assert loaded["candidate"] == "Jane Doe"
    assert loaded["score"] == 95

    # Update
    updated = update_json(test_file, {"score": 98, "status": "active"})
    assert updated["score"] == 98
    assert updated["status"] == "active"

    # Reload from disk
    reloaded = load_json(test_file)
    assert reloaded["score"] == 98
    assert reloaded["candidate"] == "Jane Doe"


def test_ai_service_adaptive_learning():
    ai = AIService()
    rec1 = ai.get_adaptive_recommendation(
        completed_skills=["Python", "Pandas", "NumPy"],
        completed_tasks_count=5,
        target_career="Data Science"
    )
    assert "Statistics" in rec1["recommendation"]

    rec2 = ai.get_adaptive_recommendation(
        completed_skills=["Statistics", "Machine Learning"],
        completed_tasks_count=10,
        target_career="Data Science"
    )
    assert "Model Evaluation" in rec2["recommendation"]

