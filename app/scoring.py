# app/scoring.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(resume_text: str, jd_info: dict):
    """
    Compare resume text against job description (jd_info).
    Returns: (similarity %, missing_skills)
    """
    jd_text = jd_info.get("text", "")
    must_have_skills = jd_info.get("must_have", [])

    # TF-IDF similarity
    vectorizer = TfidfVectorizer().fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0]

    # Check missing skills
    missing_skills = []
    resume_lower = resume_text.lower()
    for skill in must_have_skills:
        if skill.lower() not in resume_lower:
            missing_skills.append(skill)

    return similarity * 100, missing_skills