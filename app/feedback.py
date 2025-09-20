def generate_feedback(resume_text, jd_text, must_have_skills, good_to_have_skills, details):
    feedback_parts = []

    # Missing Must-Have Skills
    missing_must_have = details.get("missing_must_have", [])
    if missing_must_have:
        feedback_parts.append(
            f"❌ You are missing some *must-have skills* required for this role: {', '.join(missing_must_have)}. "
            "Consider gaining or highlighting these skills in your resume."
        )
    else:
        feedback_parts.append("✅ Great! You already cover all the *must-have skills* listed in the job description.")

    # Missing Good-to-Have Skills
    missing_good_to_have = details.get("missing_good_to_have", [])
    if missing_good_to_have:
        feedback_parts.append(
            f"⚠ You could strengthen your profile by adding these *good-to-have skills*: {', '.join(missing_good_to_have)}."
        )
    else:
        feedback_parts.append("🌟 Excellent! You already cover most of the *good-to-have skills*.")

    # Covered Skills
    covered_must_have = details.get("covered_must_have", [])
    covered_good_to_have = details.get("covered_good_to_have", [])

    if covered_must_have:
        feedback_parts.append(f"✅ Strong match: You already cover essential must-have skills like {', '.join(covered_must_have)}.")
    if covered_good_to_have:
        feedback_parts.append(f"🌟 Bonus points: You also have some good-to-have skills such as {', '.join(covered_good_to_have)}.")

    # General Tip
    feedback_parts.append("💡 Tip: Use action verbs and quantify achievements (e.g., 'Improved system efficiency by 20%').")

    return "\n\n".join(feedback_parts)