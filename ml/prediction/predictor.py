"""
ML Career Predictor: Uses persisted classification model and vectorizer
to predict career domain probabilities and top career recommendations.
"""
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Ensure project root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import joblib
import numpy as np
from utils.constants import ML_MODELS_DIR, CAREER_DOMAINS
from ml.preprocessing.preprocess import TextPreprocessor, SkillSimilarityMatcher


class CareerPredictor:
    """Predicts career domain probabilities based on user profile, skills, and interests."""

    def __init__(self):
        self.model_path = ML_MODELS_DIR / "career_model.pkl"
        self.vectorizer_path = ML_MODELS_DIR / "vectorizer.pkl"
        self.preprocessor = TextPreprocessor()
        self.similarity_matcher = SkillSimilarityMatcher()
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        self.classes = CAREER_DOMAINS
        self.is_loaded = False
        self._load_artifacts()

    def _load_artifacts(self) -> bool:
        """Loads model and vectorizer from disk."""
        try:
            if self.model_path.exists() and self.vectorizer_path.exists():
                package = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                self.model = package["model"]
                self.label_encoder = package.get("label_encoder")
                self.classes = package.get("classes", CAREER_DOMAINS)
                self.is_loaded = True
                return True
        except Exception as e:
            print(f"Warning: Could not load trained ML artifacts: {e}. Fallback enabled.")
            self.is_loaded = False
        return False

    def predict(
        self,
        skills: List[str],
        interests: str = "",
        education: str = "",
        free_text: str = ""
    ) -> Dict[str, Any]:
        """
        Predicts suitable career domains and confidence probabilities.
        Returns top domain, confidence score, and ranked predictions.
        """
        # Normalize skills
        normalized_skills = self.preprocessor.normalize_skill_list(skills)
        
        # Also extract any additional skills mentioned in free_text or interests
        text_skills = self.preprocessor.extract_skills_from_text(f"{interests} {free_text}")
        all_skills = sorted(list(set(normalized_skills + text_skills)))

        # Fallback to NLP cosine similarity if model is unavailable
        if not self.is_loaded or self.model is None or self.vectorizer is None:
            sims = self.similarity_matcher.calculate_domain_similarities(all_skills)
            sorted_sims = sorted(sims.items(), key=lambda x: x[1], reverse=True)
            top_domain, top_score = sorted_sims[0] if sorted_sims else ("Data Science", 0.70)
            return {
                "recommended_career": top_domain,
                "confidence_score": round(max(top_score, 0.50), 4),
                "rankings": [
                    {"domain": d, "probability": round(s, 4), "percentage": f"{int(s * 100)}%"}
                    for d, s in sorted_sims
                ],
                "model_used": "NLP Cosine Similarity (Fallback)",
                "normalized_skills": all_skills
            }

        # Build combined text representation
        profile_query = f"{' '.join(all_skills)} {interests} {education} {free_text}".strip()
        if not profile_query:
            profile_query = "General Technology"

        # Transform via TF-IDF
        query_vec = self.vectorizer.transform([profile_query])
        
        # Predict probabilities
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(query_vec)[0]
        else:
            # Fallback if model doesn't support predict_proba
            pred_idx = self.model.predict(query_vec)[0]
            probs = np.zeros(len(self.classes))
            probs[pred_idx] = 1.0

        # Map to class names
        class_names = self.label_encoder.classes_ if self.label_encoder else self.classes
        domain_probs = {}
        for c_name, p in zip(class_names, probs):
            domain_probs[c_name] = float(p)

        # Ensure all standard career domains are represented
        for d in CAREER_DOMAINS:
            if d not in domain_probs:
                domain_probs[d] = 0.0

        # Sort descending
        sorted_ranks = sorted(domain_probs.items(), key=lambda x: x[1], reverse=True)
        top_domain, top_prob = sorted_ranks[0]

        # In case all probabilities are flat or near zero (e.g. completely novel input)
        if top_prob < 0.15:
            # Blend with NLP similarity
            nlp_sims = self.similarity_matcher.calculate_domain_similarities(all_skills)
            blended = {}
            for d in CAREER_DOMAINS:
                blended[d] = 0.5 * domain_probs.get(d, 0.0) + 0.5 * nlp_sims.get(d, 0.0)
            sorted_ranks = sorted(blended.items(), key=lambda x: x[1], reverse=True)
            top_domain, top_prob = sorted_ranks[0]

        return {
            "recommended_career": top_domain,
            "confidence_score": round(top_prob, 4),
            "rankings": [
                {"domain": d, "probability": round(p, 4), "percentage": f"{max(int(p * 100), 1)}%"}
                for d, p in sorted_ranks
            ],
            "model_used": "ML Classifier (Trained with Joblib persistence)",
            "normalized_skills": all_skills
        }
