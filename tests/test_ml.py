"""
Unit tests for Machine Learning models, vectorizers, and predictors.
"""
import pytest
from pathlib import Path
from utils.constants import ML_MODELS_DIR, CAREER_DOMAINS
from ml.prediction.predictor import CareerPredictor


def test_model_artifacts_exist():
    """Verify that trained model and vectorizer artifacts are saved on disk."""
    model_path = ML_MODELS_DIR / "career_model.pkl"
    vectorizer_path = ML_MODELS_DIR / "vectorizer.pkl"
    assert model_path.exists(), "career_model.pkl should exist in ml/models/"
    assert vectorizer_path.exists(), "vectorizer.pkl should exist in ml/models/"


def test_predictor_initialization():
    """Verify CareerPredictor initializes and loads artifacts."""
    predictor = CareerPredictor()
    assert predictor.is_loaded is True
    assert predictor.model is not None
    assert predictor.vectorizer is not None


def test_data_science_prediction():
    """Verify that Data Science skills map accurately to Data Science domain."""
    predictor = CareerPredictor()
    skills = ["Python", "Pandas", "NumPy", "SQL", "Statistics"]
    interests = "machine learning and predictive data modeling"
    
    result = predictor.predict(skills=skills, interests=interests)
    assert "recommended_career" in result
    assert result["confidence_score"] > 0.0
    assert len(result["rankings"]) > 0
    # Data Science or Machine Learning should be top ranked
    top_domains = [r["domain"] for r in result["rankings"][:3]]
    assert any(d in ["Data Science", "Machine Learning", "Data Analytics"] for d in top_domains)


def test_web_development_prediction():
    """Verify that Web Development skills predict Web Development domain."""
    predictor = CareerPredictor()
    skills = ["HTML", "CSS", "JavaScript", "React", "Node.js"]
    interests = "full stack web apps and interactive UI"
    
    result = predictor.predict(skills=skills, interests=interests)
    top_domains = [r["domain"] for r in result["rankings"][:2]]
    assert any(d in ["Web Development", "Frontend Development"] for d in top_domains)


def test_empty_input_handling():
    """Ensure predictor does not crash on empty inputs."""
    predictor = CareerPredictor()
    result = predictor.predict(skills=[], interests="", education="", free_text="")
    assert "recommended_career" in result
    assert result["recommended_career"] in CAREER_DOMAINS
