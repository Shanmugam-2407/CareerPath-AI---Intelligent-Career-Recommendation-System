"""
Career Service: Orchestrates ML domain prediction, skill gap analysis, and profile recommendations.
"""
from typing import Dict, Any, List
from ml.prediction.predictor import CareerPredictor
from backend.services.skill_gap_service import SkillGapService
from ml.preprocessing.preprocess import TextPreprocessor


class CareerService:
    """Core service for career prediction and technical analysis."""

    def __init__(self):
        self.predictor = CareerPredictor()
        self.skill_gap_service = SkillGapService()
        self.preprocessor = TextPreprocessor()

    def predict_career(
        self,
        skills: List[str],
        interests: str = "",
        education: str = "",
        free_text: str = ""
    ) -> Dict[str, Any]:
        """Runs ML prediction across 11 domains with confidence scores."""
        return self.predictor.predict(
            skills=skills,
            interests=interests,
            education=education,
            free_text=free_text
        )

    def analyze_free_text_skills(self, text: str) -> Dict[str, Any]:
        """Extracts and normalizes technical skills from free-form user text."""
        extracted = self.preprocessor.extract_skills_from_text(text)
        return {
            "raw_text": text,
            "extracted_skills": extracted,
            "count": len(extracted)
        }

    def evaluate_career_alignment(
        self,
        user_skills: List[str],
        target_career: str,
        interests: str = "",
        education: str = "",
        free_text: str = ""
    ) -> Dict[str, Any]:
        """Complete evaluation combining ML domain prediction and skill gap analysis."""
        prediction = self.predict_career(
            skills=user_skills,
            interests=interests,
            education=education,
            free_text=free_text
        )
        
        target = target_career if target_career.strip() else prediction["recommended_career"]
        gap = self.skill_gap_service.analyze_skill_gap(
            user_skills=user_skills,
            target_career=target,
            free_text=free_text
        )

        return {
            "prediction": prediction,
            "skill_gap": gap,
            "recommended_career": prediction["recommended_career"],
            "target_career": target
        }
