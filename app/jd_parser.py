def parse_jd(jd_text: str):
    """
    Very simple JD parser: extracts must-have and nice-to-have skills.
    In production, use spaCy or regex.
    """
    must_have = []
    nice_to_have = []

    # Example logic
    jd_lower = jd_text.lower()
    if "python" in jd_lower:
        must_have.append("Python")
    if "sql" in jd_lower:
        must_have.append("SQL")
    if "aws" in jd_lower:
        nice_to_have.append("AWS")

    return {
        "must_have": must_have,
        "nice_to_have": nice_to_have
    }