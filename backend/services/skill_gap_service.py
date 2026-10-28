"""
Skill-Gap Analysis Service: Compares user skills against target career requirements,
computes skill match percentage, and identifies missing skills.
"""
from typing import List, Dict, Any, Set
from utils.constants import DOMAIN_SKILLS_MAP, CAREER_DOMAINS
from ml.preprocessing.preprocess import TextPreprocessor, SkillSimilarityMatcher


class SkillGapService:
    """Performs deep skill comparison and gap analysis for target careers."""

    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.similarity_matcher = SkillSimilarityMatcher()

    def resolve_domain(self, target_career: str) -> str:
        """Normalizes user target career input into a canonical career domain."""
        target_clean = target_career.strip().lower()
        
        # Direct or alias matching
        mapping = {
            "data scientist": "Data Science",
            "data science": "Data Science",
            "machine learning engineer": "Machine Learning",
            "machine learning": "Machine Learning",
            "ml engineer": "Machine Learning",
            "ai engineer": "AI Engineering",
            "ai engineering": "AI Engineering",
            "artificial intelligence": "AI Engineering",
            "data analyst": "Data Analytics",
            "data analytics": "Data Analytics",
            "web developer": "Web Development",
            "web development": "Web Development",
            "full stack developer": "Web Development",
            "full stack": "Web Development",
            "backend developer": "Backend Development",
            "backend development": "Backend Development",
            "frontend developer": "Frontend Development",
            "frontend development": "Frontend Development",
            "cloud engineer": "Cloud Engineering",
            "cloud engineering": "Cloud Engineering",
            "devops engineer": "DevOps",
            "devops": "DevOps",
            "cybersecurity analyst": "Cybersecurity",
            "cybersecurity engineer": "Cybersecurity",
            "cybersecurity": "Cybersecurity",
            "mobile developer": "Mobile Development",
            "mobile development": "Mobile Development",
            "android developer": "Mobile Development",
            "ios developer": "Mobile Development"
        }
        
        if target_clean in mapping:
            return mapping[target_clean]
            
        # Check partial match
        for key, domain in mapping.items():
            if key in target_clean or target_clean in key:
                return domain

        # Default fallback
        return "Data Science"

    def analyze_skill_gap(
        self,
        user_skills: List[str],
        target_career: str,
        free_text: str = ""
    ) -> Dict[str, Any]:
        """
        Calculates already known skills, missing skills, required tech stack,
        and skill match percentage.
        """
        # Resolve canonical domain
        canonical_domain = self.resolve_domain(target_career)
        required_skills = DOMAIN_SKILLS_MAP.get(canonical_domain, DOMAIN_SKILLS_MAP["Data Science"])

        # Extract & normalize user skills
        normalized_user_skills = self.preprocessor.normalize_skill_list(user_skills)
        if free_text:
            extra_skills = self.preprocessor.extract_skills_from_text(free_text)
            normalized_user_skills = sorted(list(set(normalized_user_skills + extra_skills)))

        # Sets for comparison
        user_set: Set[str] = set(normalized_user_skills)
        req_set: Set[str] = set(required_skills)

        # Categorization
        already_known = sorted(list(user_set.intersection(req_set)))
        missing = sorted(list(req_set.difference(user_set)))
        additional_skills = sorted(list(user_set.difference(req_set)))

        # Skill match percentage calculation
        total_req = len(required_skills)
        known_req_count = len(already_known)
        
        if total_req > 0:
            match_percentage = round((known_req_count / total_req) * 100, 1)
        else:
            match_percentage = 0.0

        # Next recommended career step
        if missing:
            next_step = f"Master fundamental {missing[0]} and begin introductory practice modules."
        else:
            next_step = "Build end-to-end industry capstone projects and prepare for advanced system design / technical interviews."

        return {
            "target_career": target_career,
            "canonical_domain": canonical_domain,
            "required_skills": required_skills,
            "already_known": already_known,
            "missing_skills": missing,
            "additional_skills": additional_skills,
            "match_percentage": match_percentage,
            "known_count": known_req_count,
            "missing_count": len(missing),
            "total_required_count": total_req,
            "next_step": next_step
        }
