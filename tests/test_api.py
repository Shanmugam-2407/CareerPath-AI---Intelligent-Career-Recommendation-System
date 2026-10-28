"""
API integration tests for FastAPI endpoints using TestClient.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_profile_endpoint():
    payload = {
        "name": "Sarah Connor",
        "education": "B.Tech Computer Science",
        "experience_level": "Beginner",
        "skills": ["Python", "SQL"],
        "interests": "Machine Learning and AI",
        "career_goal": "Data Scientist",
        "preferred_domain": "Data Science",
        "study_hours": 3.0,
        "timeline_months": 6,
        "free_text": "I know basic Python and SQL and want to learn Data Science."
    }
    response = client.post("/api/profile", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Sarah Connor"
    assert "Python" in data["normalized_skills"]


def test_career_predict_endpoint():
    payload = {
        "skills": ["Python", "Pandas", "NumPy", "SQL"],
        "interests": "Data analysis and prediction",
        "education": "B.S. Statistics"
    }
    response = client.post("/api/career/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommended_career" in data
    assert "rankings" in data
    assert len(data["rankings"]) > 0


def test_skill_gap_endpoint():
    payload = {
        "user_skills": ["Python", "SQL"],
        "target_career": "Data Scientist"
    }
    response = client.post("/api/skills/gap", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["canonical_domain"] == "Data Science"
    assert "Python" in data["already_known"]
    assert "Machine Learning" in data["missing_skills"]


def test_roadmap_generate_endpoint():
    payload = {
        "name": "Sarah Connor",
        "education": "B.Tech Computer Science",
        "experience_level": "Beginner",
        "target_career": "Data Science",
        "study_hours": 3.0,
        "timeline_months": 6,
        "skills": ["Python", "SQL"]
    }
    response = client.post("/api/roadmap/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "roadmap" in data
    assert "daily_tasks" in data
    assert "projects" in data


def test_progress_endpoints():
    # Update progress
    update_payload = {
        "completed_skills": ["Python", "SQL"],
        "completed_tasks": ["Deep Dive into Theoretical Architecture"],
        "completed_projects": []
    }
    put_res = client.put("/api/progress", json=update_payload)
    assert put_res.status_code == 200
    put_data = put_res.json()
    assert "Python" in put_data["completed_skills"]
    assert put_data["overall_completion_percentage"] >= 0

    # Get progress
    get_res = client.get("/api/progress")
    assert get_res.status_code == 200
    get_data = get_res.json()
    assert "adaptive_recommendation" in get_data
