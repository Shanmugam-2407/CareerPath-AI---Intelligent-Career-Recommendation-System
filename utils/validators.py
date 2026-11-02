"""
Input validation and sanitization utilities.
"""
import re
from typing import List, Tuple
from utils.constants import CAREER_DOMAINS


def sanitize_text(text: str, max_length: int = 2000) -> str:
    """Sanitize and trim input text."""
    if not text:
        return ""
    text = text.strip()
    # Truncate if exceedingly long
    if len(text) > max_length:
        text = text[:max_length]
    # Remove potentially dangerous characters / script tags
    text = re.sub(r"<[^>]*>", "", text)
    return text


def validate_user_profile_data(
    name: str,
    education: str,
    skills: List[str],
    study_hours: float,
    timeline_months: int
) -> Tuple[bool, str]:
    """Validate user profile attributes."""
    if not name or len(name.strip()) < 2:
        return False, "Name must be at least 2 characters."
    if not education or len(education.strip()) < 2:
        return False, "Education / qualification is required."
    if not skills:
        return False, "At least one skill or programming language must be provided."
    if study_hours <= 0 or study_hours > 16:
        return False, "Available study hours must be between 0.5 and 16 hours per day."
    if timeline_months < 1 or timeline_months > 36:
        return False, "Timeline must be between 1 and 36 months."
    return True, "Valid"


def is_valid_domain(domain: str) -> bool:
    """Check if domain is recognized."""
    return domain in CAREER_DOMAINS

