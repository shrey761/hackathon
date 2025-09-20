import spacy

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")

# Define sample skill, cert, and degree keywords
SKILL_KEYWORDS = [
    "python", "java", "sql", "machine learning", "deep learning",
    "data analysis", "django", "flask", "nlp", "aws", "docker", "kubernetes"
]

CERTIFICATIONS = [
    "aws certified", "azure certified", "gcp certified", "pmp", "cfa"
]

DEGREES = [
    "bachelor", "master", "phd", "b.tech", "m.tech", "bsc", "msc"
]

def parse_jd(jd_text: str):
    doc = nlp(jd_text.lower())

    must_have = []
    nice_to_have = []
    education = []
    certifications = []
    years_experience = None

    # Extract skills (simple keyword scan)
    for skill in SKILL_KEYWORDS:
        if skill in jd_text.lower():
            must_have.append(skill)

    # Extract certifications
    for cert in CERTIFICATIONS:
        if cert in jd_text.lower():
            certifications.append(cert)

    # Extract degrees
    for degree in DEGREES:
        if degree in jd_text.lower():
            education.append(degree)

    # Extract years of experience (regex-like using spaCy)
    for token in doc:
        if token.like_num:
            next_token = token.nbor(1) if token.i + 1 < len(doc) else None
            if next_token and next_token.text.lower() in ["years", "yrs", "year"]:
                years_experience = int(token.text)

    return {
        "must_have": must_have,
        "nice_to_have": nice_to_have,   # can extend later
        "education": education,
        "certifications": certifications,
        "experience_required": years_experience
    }