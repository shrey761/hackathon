import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_years_experience(text: str):
    """Extract number of years of experience from resume text."""
    matches = re.findall(r"(\d+)\+?\s+years?", text.lower())
    return max([int(m) for m in matches], default=0)

def compute_similarity(resume_text: str, jd_text: str, must_have=None, good_to_have=None):
    """
    Compute similarity between resume and JD with details.
    Returns (score, details).
    """
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]

    # Default skill sets if not passed
    must_have = must_have or []
    good_to_have = good_to_have or []

    resume_lower = resume_text.lower()

    missing_must_have = [s for s in must_have if s.lower() not in resume_lower]
    missing_good_to_have = [s for s in good_to_have if s.lower() not in resume_lower]

    details = {
        "years_experience": extract_years_experience(resume_text),
        "must_have": must_have,
        "good_to_have": good_to_have,
        "missing_must_have": missing_must_have,
        "missing_good_to_have": missing_good_to_have,
    }

    return score, details