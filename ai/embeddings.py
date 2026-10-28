"""
Embedding and semantic vector similarity abstraction.
Provides fast TF-IDF and dense vector similarity calculations.
"""
from typing import List, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingService:
    """Computes semantic text embeddings and cosine similarities."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), token_pattern=r"(?u)\b[\w\+\#\.\-]+\b")
        self.is_fitted = False

    def get_similarity(self, text_a: str, text_b: str) -> float:
        """Computes cosine similarity between two text snippets."""
        if not text_a or not text_b:
            return 0.0
        try:
            vec = TfidfVectorizer().fit([text_a, text_b])
            mat = vec.transform([text_a, text_b])
            sim = cosine_similarity(mat[0:1], mat[1:2])[0][0]
            return float(sim)
        except Exception:
            return 0.0

    def rank_matches(self, query: str, candidates: List[str]) -> List[Dict[str, Any]]:
        """Ranks a list of candidate strings against a query text."""
        if not query or not candidates:
            return []
        try:
            all_texts = [query] + candidates
            matrix = self.vectorizer.fit_transform(all_texts)
            sims = cosine_similarity(matrix[0:1], matrix[1:])[0]
            ranked = [
                {"candidate": cand, "similarity": round(float(sim), 4)}
                for cand, sim in zip(candidates, sims)
            ]
            ranked.sort(key=lambda x: x["similarity"], reverse=True)
            return ranked
        except Exception:
            return [{"candidate": c, "similarity": 0.0} for c in candidates]
