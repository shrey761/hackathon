import streamlit as st
from app.resume_parser import parse_resume
from app.jd_parser import parse_jd
from app.scoring import compute_similarity

st.set_page_config(page_title="Automated Resume Relevance Check", layout="wide")

st.title("📄 Automated Resume Relevance Check")

# Input: Job Description
jd_text = st.text_area("Paste Job Description", height=200)

# Input: Resume Upload
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded_file is not None and jd_text.strip() != "":
    try:
        # Extract text from resume
        resume_text = parse_resume(uploaded_file)

        # Parse JD
        jd_info = parse_jd(jd_text)

        # Compute similarity score
        score, missing_skills = compute_similarity(resume_text, jd_info)

        # Show outputs
        st.subheader("✅ Results")
        st.write(f"*Relevance Score:* {score:.2f}%")

        if missing_skills:
            st.warning(f"⚠ Missing Skills: {', '.join(missing_skills)}")
        else:
            st.success("All required skills are present!")

        with st.expander("🔍 Extracted Resume Text"):
            st.text(resume_text[:2000])  # show first 2000 chars only

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Please paste a Job Description and upload a Resume to start.")