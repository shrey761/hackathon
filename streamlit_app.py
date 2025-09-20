import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from app.resume_parser import parse_resume
from app.jd_parser import parse_jd
from app.scoring import compute_similarity
from app.feedback import generate_feedback


# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Resume Relevance Checker",
    page_icon="📊",
    layout="wide"
)


# -------------------- SIDEBAR --------------------
st.sidebar.title("⚙ Options")
st.sidebar.success("An AI-powered Resume–JD Matching Tool 🚀")

st.sidebar.markdown("""
### 📖 How to use
1. Paste the *Job Description*.  
2. Upload the *Resume (PDF/DOCX)*.  
3. Click *Analyze Resume*.  

👉 The tool extracts *skills, education & experience, compares with the JD, and generates **smart feedback*.
""")

st.sidebar.markdown("---")
st.sidebar.subheader("📌 About")
st.sidebar.info("Built for hackathons 🎯 | Showcases NLP-based resume screening")


# -------------------- MAIN HEADER --------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #2C3E50;'>
        📊 Automated Resume Relevance Checker
    </h1>
    <p style='text-align: center; color: gray; font-size:18px;'>
        Match resumes with job descriptions & get actionable improvement tips
    </p>
    """,
    unsafe_allow_html=True
)


# -------------------- INPUTS --------------------
col1, col2 = st.columns([2, 1])

with col1:
    jd_text = st.text_area("📄 Paste Job Description", height=220)

with col2:
    uploaded_file = st.file_uploader(
        "📂 Upload Resume",
        type=["pdf", "docx"],
        help="Accepted formats: PDF, DOCX"
    )


# -------------------- ANALYZE --------------------
if st.button("🔎 Analyze Resume", use_container_width=True):
    if not jd_text or not uploaded_file:
        st.error("⚠ Please provide both a Job Description and a Resume.")
    else:
        try:
            # --- Extract resume text ---
            resume_text = parse_resume(uploaded_file)

            # --- Parse JD ---
            jd_text_only, must_have_skills, good_to_have_skills = parse_jd(jd_text)

            # --- Compute relevance ---
            score, details = compute_similarity(
                resume_text, jd_text_only, must_have_skills, good_to_have_skills
            )

            # --- Generate feedback ---
            feedback = generate_feedback(
                resume_text,
                jd_text_only,
                details.get("missing_must_have", []),
                details.get("missing_good_to_have", [])
            )

            # -------------------- OUTPUT --------------------
            st.markdown("## 📈 Results")

            # Relevance score
            st.metric(
                label="Relevance Score",
                value=f"{score:.2f}%",
                delta="Higher is better"
            )

            # Skills section
            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown("### ✅ Must-Have Skills (Covered)")
                st.success(", ".join(details.get("must_have_covered", [])) or "None")

                st.markdown("### ❌ Missing Must-Have Skills")
                st.error(", ".join(details.get("missing_must_have", [])) or "None")

            with col_b:
                st.markdown("### 🌟 Good-to-Have Skills (Covered)")
                st.info(", ".join(details.get("good_to_have_covered", [])) or "None")

                st.markdown("### ⚠ Missing Good-to-Have Skills")
                st.warning(", ".join(details.get("missing_good_to_have", [])) or "None")

            # -------------------- VISUALIZATION --------------------
            st.markdown("### 📊 Skill Coverage Overview")

            skill_data = {
                "Category": [
                    "Must-Have Covered", "Must-Have Missing",
                    "Good-to-Have Covered", "Good-to-Have Missing"
                ],
                "Count": [
                    len(details.get("must_have_covered", [])),
                    len(details.get("missing_must_have", [])),
                    len(details.get("good_to_have_covered", [])),
                    len(details.get("missing_good_to_have", [])),
                ]
            }

            df = pd.DataFrame(skill_data)

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.barh(df["Category"], df["Count"], color=["#2ECC71", "#E74C3C", "#3498DB", "#F39C12"])
            ax.set_xlabel("Number of Skills")
            ax.set_title("Resume vs JD Skill Coverage")
            st.pyplot(fig)

            # -------------------- FEEDBACK --------------------
            st.markdown("## 💡 Feedback for Candidate")

            for tip in feedback:
                st.write(f"- {tip}")

            # -------------------- PDF EXPORT --------------------
            st.markdown("## 📥 Download Report")

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []

            elements.append(Paragraph("Resume Relevance Report", styles["Title"]))
            elements.append(Spacer(1, 12))
            elements.append(Paragraph(f"Relevance Score: {score:.2f}%", styles["Heading2"]))

            elements.append(Spacer(1, 12))
            elements.append(Paragraph("Must-Have Skills Covered:", styles["Heading3"]))
            elements.append(Paragraph(", ".join(details.get("must_have_covered", [])) or "None", styles["Normal"]))

            elements.append(Paragraph("Missing Must-Have Skills:", styles["Heading3"]))
            elements.append(Paragraph(", ".join(details.get("missing_must_have", [])) or "None", styles["Normal"]))

            elements.append(Paragraph("Good-to-Have Skills Covered:", styles["Heading3"]))
            elements.append(Paragraph(", ".join(details.get("good_to_have_covered", [])) or "None", styles["Normal"]))

            elements.append(Paragraph("Missing Good-to-Have Skills:", styles["Heading3"]))
            elements.append(Paragraph(", ".join(details.get("missing_good_to_have", [])) or "None", styles["Normal"]))

            elements.append(Spacer(1, 12))
            elements.append(Paragraph("Feedback:", styles["Heading2"]))
            for tip in feedback:
                elements.append(Paragraph(f"- {tip}", styles["Normal"]))

            doc.build(elements)
            pdf_data = buffer.getvalue()

            st.download_button(
                label="⬇ Download PDF Report",
                data=pdf_data,
                file_name="resume_relevance_report.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"⚠ Error: {e}")