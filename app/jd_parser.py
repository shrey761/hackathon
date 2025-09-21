import re
import spacy
nlp=spacy.load("en_core_web_sm")
# Some predefined skill keywords (you can expand this list)
SKILL_KEYWORDS = [
    "python", "java", "c++", "c#", "sql", "javascript", "html", "css",
    "machine learning", "deep learning", "nlp", "data analysis",
    "excel", "power bi", "tableau", "aws", "azure", "gcp", "docker",
    "kubernetes", "git", "django", "flask", "react", "angular"
]

def parse_jd(jd_text):
    """
    Parses a job description to extract must-have and good-to-have skills.
    Returns: (jd_text_only, must_have_skills, good_to_have_skills)
    """

    jd_text = jd_text.lower()
    doc = nlp(jd_text)

    must_have = set()
    good_to_have = set()

    # --- Detect years of experience ---
    experience = re.findall(r"(\d+)\+?\s+years?", jd_text)
    if experience:
        must_have.add(f"{experience[0]}+ years experience")

    # --- Match skills from keyword list ---
    for token in doc:
        token_text = token.text.lower()
        if token_text in SKILL_KEYWORDS:
            must_have.add(token_text)

    # --- Phrases like "nice to have", "preferred" → good-to-have ---
    preferred_section = re.findall(r"(?:nice to have|preferred|optional).*", jd_text)
    for section in preferred_section:
        for skill in SKILL_KEYWORDS:
            if skill in section:
                good_to_have.add(skill)

    # --- Guarantee at least something is returned ---
    if not must_have and not good_to_have:
        must_have.add("general programming experience")

    return jd_text, list(must_have), list(good_to_have)