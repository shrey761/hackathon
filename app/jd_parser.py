import re

def parse_jd(text: str):
    """
    Extract must-have and good-to-have skills from JD using simple keyword rules.
    """

    # Normalize text
    jd_text = text.lower()

    # Must-have keywords
    must_patterns = [
        r"\bmust have\b",
        r"\brequired\b",
        r"\bminimum\b",
        r"\bessential\b",
        r"\bstrong knowledge of\b"
    ]

    # Good-to-have keywords
    good_patterns = [
        r"\bnice to have\b",
        r"\bpreferred\b",
        r"\boptional\b",
        r"\bgood to have\b",
        r"\bplus\b"
    ]

    must_have_skills = []
    good_to_have_skills = []

    for pattern in must_patterns:
        matches = re.findall(pattern + r".*?(\w+)", jd_text)
        must_have_skills.extend(matches)

    for pattern in good_patterns:
        matches = re.findall(pattern + r".*?(\w+)", jd_text)
        good_to_have_skills.extend(matches)

    # If nothing is detected, fallback: pick common tech words
    tech_words = ["python", "java", "c++", "sql", "aws", "docker", "react", "node", "tensorflow", "nlp"]

    for word in tech_words:
        if word in jd_text and word not in must_have_skills and word not in good_to_have_skills:
            good_to_have_skills.append(word)

    return text, list(set(must_have_skills)), list(set(good_to_have_skills))