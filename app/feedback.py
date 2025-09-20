def generate_feedback(resume_text, jd_text, missing_must_have, missing_good_to_have):
    feedback = []

    # Must-have skills
    if missing_must_have:
        feedback.append(
            f"⚠ Your resume is missing key must-have skills: {', '.join(missing_must_have)}. "
            "Consider adding these explicitly."
        )
    else:
        feedback.append("✅ Great job! Your resume covers all the must-have skills.")

    # Good-to-have skills
    if missing_good_to_have:
        feedback.append(
            f"💡 To strengthen your application, add these good-to-have skills: {', '.join(missing_good_to_have)}."
        )
    else:
        feedback.append("🚀 You already have all the good-to-have skills from the JD!")

    # General tips
    feedback.append(
        "⭐ Tip: Use measurable impact (e.g., 'improved system performance by 30%') to make your achievements stand out."
    )
    feedback.append(
        "⭐ Tip: Ensure your resume highlights both technical and soft skills relevant to the role."
    )

    return feedback