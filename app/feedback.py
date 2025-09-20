def generate_feedback(resume_text: str, jd_text: str, missing_skills: list):
    feedback = []

    # Suggest adding missing skills
    if missing_skills:
        feedback.append(
            f"Consider adding these missing skills to your resume: {', '.join(missing_skills)}."
        )

    # Check resume length
    word_count = len(resume_text.split())
    if word_count < 200:
        feedback.append("Your resume seems short. Try to expand with more details about your work experience and achievements.")
    elif word_count > 800:
        feedback.append("Your resume may be too long. Consider summarizing to focus on the most relevant skills for this job.")

    # Compare education keywords
    if "bachelor" in jd_text.lower() and "bachelor" not in resume_text.lower():
        feedback.append("The job description mentions a Bachelor's degree. Make sure your education details are clearly highlighted.")

    if "master" in jd_text.lower() and "master" not in resume_text.lower():
        feedback.append("The job description mentions a Master's degree. Highlight your postgraduate qualifications if applicable.")

    # Soft skills check
    soft_skills = ["communication", "leadership", "teamwork", "problem solving"]
    missing_soft_skills = [s for s in soft_skills if s not in resume_text.lower()]
    if missing_soft_skills:
        feedback.append(
            f"Consider highlighting soft skills such as: {', '.join(missing_soft_skills)}."
        )

    # Final fallback
    if not feedback:
        feedback.append("Your resume looks good, but tailor it more closely to the job description.")

    return feedback