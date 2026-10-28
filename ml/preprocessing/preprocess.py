"""
Text preprocessing, skill extraction, and NLP feature normalization pipeline.
"""
import re
from typing import List, Set, Dict, Any, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.constants import SKILL_ALIASES, CANONICAL_SKILLS, DOMAIN_SKILLS_MAP


class TextPreprocessor:
    """Preprocesses raw profile text and extracts normalized technical skills."""

    def __init__(self):
        # Sort aliases by descending length so multi-word aliases (e.g. 'machine learning', 'rest api') match first
        self.sorted_aliases = sorted(SKILL_ALIASES.keys(), key=lambda x: len(x), reverse=True)

    def clean_text(self, text: str) -> str:
        """Lowercases and cleans unwanted special characters while preserving tech terms like c++, c#, .js."""
        if not text:
            return ""
        text = text.lower()
        # Keep alphanumeric, +, #, ., -, /
        text = re.sub(r"[^\w\s\+\#\.\-\/]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def extract_skills_from_text(self, text: str) -> List[str]:
        """
        Extracts recognized technical skills from free-form natural language text.
        Returns a deduplicated list of canonical skill names.
        """
        cleaned = self.clean_text(text)
        found_skills: Set[str] = set()
        matched_spans: List[Tuple[int, int]] = []

        # Check multi-word and single-word aliases with word boundaries
        for alias in self.sorted_aliases:
            # Create regex pattern with word boundaries (handling special chars like ++ or # safely)
            escaped_alias = re.escape(alias)
            pattern = rf"(?<![\w\+\#]){escaped_alias}(?![\w\+\#])"
            
            for match in re.finditer(pattern, cleaned):
                start, end = match.span()
                # Ensure no overlapping match with longer matched phrase
                if not any(s <= start and end <= e for s, e in matched_spans):
                    canonical = SKILL_ALIASES[alias]
                    found_skills.add(canonical)
                    matched_spans.append((start, end))

        return sorted(list(found_skills))

    def normalize_skill_list(self, raw_skills: List[str]) -> List[str]:
        """
        Normalizes a list of user-provided skill strings (e.g., ['python programming', 'reactjs'])
        into canonical skill names (e.g., ['Python', 'React']).
        """
        canonical_set: Set[str] = set()
        for s in raw_skills:
            if not s:
                continue
            cleaned = s.strip().lower()
            if cleaned in SKILL_ALIASES:
                canonical_set.add(SKILL_ALIASES[cleaned])
            else:
                # Try extracting within the string if it's a phrase
                extracted = self.extract_skills_from_text(s)
                if extracted:
                    canonical_set.update(extracted)
                else:
                    # Title case fallback if not recognized
                    canonical_set.add(s.strip().title())
        return sorted(list(canonical_set))

    def build_profile_text(self, skills: List[str], interests: str = "", education: str = "", prompt: str = "") -> str:
        """Constructs a consolidated text representation for TF-IDF feature extraction."""
        normalized_skills = self.normalize_skill_list(skills)
        parts = [
            f"Skills: {' '.join(normalized_skills)}",
            f"Interests: {interests}",
            f"Education: {education}",
            f"Notes: {prompt}"
        ]
        return " ".join([p for p in parts if p.strip()])


class SkillSimilarityMatcher:
    """Calculates NLP TF-IDF cosine similarities between user profile and career domains."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b[\w\+\#\.\-]+\b")
        self.domain_texts: Dict[str, str] = {}
        for domain, skills in DOMAIN_SKILLS_MAP.items():
            self.domain_texts[domain] = f"{domain} {' '.join(skills)}"
        
        # Fit vectorizer on domain definitions
        self.domains = list(self.domain_texts.keys())
        self.domain_matrix = self.vectorizer.fit_transform([self.domain_texts[d] for d in self.domains])

    def calculate_domain_similarities(self, user_skills: List[str]) -> Dict[str, float]:
        """Returns cosine similarity score for each domain based on user skills."""
        if not user_skills:
            return {d: 0.0 for d in self.domains}
        
        user_text = " ".join(user_skills)
        user_vec = self.vectorizer.transform([user_text])
        sims = cosine_similarity(user_vec, self.domain_matrix)[0]
        
        return {domain: round(float(sim), 4) for domain, sim in zip(self.domains, sims)}
