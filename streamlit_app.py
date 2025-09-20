import streamlit as st
from app import resume_parser, scoring, jd_parser

st.title("Automated Resume Relevance Check")

jd = st.text_area("Paste Job Description")
resume_file = st.file_uploader("Upload Resume", type=["pdf","docx"])

if jd and resume_file:
    resume_text = resume_parser.extract_text(resume_file)
    jd_data = jd_parser.parse_jd(jd)
    result = scoring.compute_hybrid_score(resume_text, jd)

    st.write("### Results")
    st.json(result)

    missing = [s for s in jd_data["must_have"] if s.lower() not in resume_text.lower()]
    st.write("Missing Skills:", missing if missing else "None")