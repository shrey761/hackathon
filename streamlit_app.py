import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Import from app folder
from app.resume_parser import extract_text_from_pdf_or_docx
from app.jd_parser import parse_jd
from app.scoring import compute_similarity
from app.feedback import generate_feedback
from app.database import save_result, load_results
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")



# ===============================
# Verdict Function
# ===============================
def get_verdict(score_percent: float) -> str:
    if score_percent >= 70:
        return "✅ High Suitability"
    elif score_percent >= 40:
        return "🟡 Medium Suitability"
    else:
        return "❌ Low Suitability"


# ===============================
# PDF Generation
# ===============================
def generate_pdf_report(resume_name, score, verdict, details, feedback):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Resume Relevance Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Resume: {resume_name}")
    c.drawString(50, height - 120, f"Relevance Score: {score if score else 'N/A'}%")
    c.drawString(50, height - 140, f"Suitability Verdict: {verdict or 'N/A'}")

    # Defensive handling
    details = details or {}
    feedback = feedback or "No feedback generated."

    # Must-Have Covered
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 180, "✅ Must-Have Skills (Covered):")
    c.setFont("Helvetica", 11)
    c.drawString(70, height - 200, ", ".join(details.get("covered_must_have", [])) or "None")

    # Missing Must-Have
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 230, "❌ Missing Must-Have Skills:")
    c.setFont("Helvetica", 11)
    c.drawString(70, height - 250, ", ".join(details.get("missing_must_have", [])) or "None")

    # Good-to-Have Covered
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 280, "🌟 Good-to-Have Skills (Covered):")
    c.setFont("Helvetica", 11)
    c.drawString(70, height - 300, ", ".join(details.get("covered_good_to_have", [])) or "None")

    # Missing Good-to-Have
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 330, "⚠ Missing Good-to-Have Skills:")
    c.setFont("Helvetica", 11)
    c.drawString(70, height - 350, ", ".join(details.get("missing_good_to_have", [])) or "None")

    # Feedback
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 380, "💡 Feedback:")
    c.setFont("Helvetica", 11)
    text_obj = c.beginText(70, height - 400)
    for line in feedback.split("\n"):
        text_obj.textLine(line.strip())
    c.drawText(text_obj)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


# ===============================
# Streamlit App
# ===============================
st.set_page_config(page_title="Resume Relevance Checker", layout="wide")

# Sidebar
st.sidebar.title("⚙ Options")
st.sidebar.subheader("About")
st.sidebar.info(
    "This tool analyzes candidate resumes against a job description. "
    "It highlights missing must-have and good-to-have skills, "
    "computes a relevance score, gives a suitability verdict, "
    "provides actionable feedback, and stores results for future access."
)

st.sidebar.subheader("How to Use")
st.sidebar.markdown("""
1. 📋 Paste the Job Description  
2. 📂 Upload Resume(s) in PDF/DOCX  
3. 🔍 Click *Analyze Resume(s)*  
4. 📊 View detailed results or batch comparison  
5. 💾 Download reports (PDF, CSV, ZIP)  
6. 📊 Use Dashboard to see stored results  
""")

st.title("📄 Automated Resume Relevance Checker")

jd_text = st.text_area("Paste Job Description Here", height=200)
uploaded_files = st.file_uploader("📂 Upload Resume(s)", type=["pdf", "docx"], accept_multiple_files=True)


if st.button("🔍 Analyze Resume(s)"):
    if not jd_text.strip():
        st.error("❌ Please paste a job description.")
    elif not uploaded_files:
        st.error("❌ Please upload at least one resume.")
    else:
        try:
            jd_text_only, must_have_skills, good_to_have_skills = parse_jd(jd_text)
        except Exception as e:
            st.error(f"⚠ JD Parser Error: {e}")
            st.stop()

        results, pdf_files = [], []

        for uploaded_file in uploaded_files:
                try:
                    resume_text = extract_text_from_pdf_or_docx(uploaded_file)
                    score, details = compute_similarity(resume_text, jd_text_only)
                    score_percent = round(float(score) * 100, 2)
                    verdict = get_verdict(score_percent)

                    feedback = generate_feedback(
                        resume_text, jd_text_only, must_have_skills, good_to_have_skills, details
                    )

                    results.append({
                        "Resume": uploaded_file.name,
                        "Relevance Score (%)": score_percent,
                        "Verdict": verdict,
                        "Missing Must-Have": ", ".join(details.get("missing_must_have", [])) or "None",
                        "Missing Good-to-Have": ", ".join(details.get("missing_good_to_have", [])) or "None",
                        "Feedback": feedback,
                    })

                    save_result(uploaded_file.name, score_percent, verdict, feedback)

                    try:
                        pdf_buffer = generate_pdf_report(
                            uploaded_file.name,
                            score_percent,
                            verdict,
                            details,
                            feedback
                        )
                        pdf_files.append((
                            uploaded_file.name.replace(".pdf", "").replace(".docx", "") + "_report.pdf",
                            pdf_buffer
                        ))
                    except Exception as e:
        # Always generate a fallback PDF explaining the error
                        error_feedback = f"Could not generate full report. Error: {str(e)}"
                        pdf_buffer = generate_pdf_report(
                            uploaded_file.name,
                            score_percent if 'score_percent' in locals() else "N/A",
                            verdict if 'verdict' in locals() else "Error",
                            {},
                            error_feedback
                        )
                        pdf_files.append((
                            uploaded_file.name.replace(".pdf", "").replace(".docx", "") + "_error_report.pdf",
                            pdf_buffer
                        ))
                except Exception as e:
                    results.append({
                        "Resume":uploaded_file.name,
                        "Relevance Score(%)":"Error",
                        "Verdict":"Error",
                        "Feedback":f"Could not process{uploaded_file.name}:{e}"
                    })
        # ===============================
        # Single Resume Mode
        # ===============================
        if len(uploaded_files) == 1:
            res = results[0]
            st.header("📊 Analysis Results")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Relevance Score", f"{res['Relevance Score (%)']}%", delta="Higher is better")
            with col2:
                st.metric("Suitability Verdict", res["Verdict"])

            # Skill coverage chart
            st.subheader("📊 Skill Coverage Overview")
            categories = ["Must-Have Covered", "Must-Have Missing", "Good-to-Have Covered", "Good-to-Have Missing"]
            values = [
                len(details.get("covered_must_have", [])),
                len(details.get("missing_must_have", [])),
                len(details.get("covered_good_to_have", [])),
                len(details.get("missing_good_to_have", [])),
            ]
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(categories, values, color=["green", "red", "blue", "orange"])
            ax.set_ylabel("Number of Skills")
            ax.set_title("Resume vs JD Skill Coverage")
            plt.xticks(rotation=20)
            st.pyplot(fig)

            st.subheader("💡 Actionable Feedback")
            for line in res["Feedback"].split("\n\n"):
                st.info(line)

            # PDF download
            if pdf_files:
               pdf_name, pdf_buffer = pdf_files[0]
               st.download_button("📥 Download PDF Report", data=pdf_buffer, file_name=pdf_name, mime="application/pdf")
            else:
                st.warning("⚠ No PDF report was generated for this resume.")

        # ===============================
        # Batch Mode
        # ===============================
        else:
            st.header("📂 Batch Results")
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)

            # CSV download
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("💾 Download Results as CSV", csv, "batch_results.csv", "text/csv")

            # Bar chart comparison
            st.subheader("📊 Resume Comparison by Score")
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.barh(df["Resume"], df["Relevance Score (%)"], color="skyblue")
            ax.set_xlabel("Relevance Score (%)")
            ax.set_title("Resume Relevance Comparison")
            st.pyplot(fig)

            # ZIP download of PDFs
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                for pdf_name, pdf_buffer in pdf_files:
                    zipf.writestr(pdf_name, pdf_buffer.read())
            zip_buffer.seek(0)
            st.download_button("📥 Download All PDF Reports (ZIP)", data=zip_buffer, file_name="all_reports.zip", mime="application/zip")


# ===============================
# Dashboard View
# ===============================
if st.sidebar.button("📊 View Stored Results"):
    st.subheader("📊 Stored Results Dashboard")
    df = load_results()
    if not df.empty:
        st.dataframe(df)

        # Chart
        st.subheader("📊 Historical Score Distribution")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(df["score"], bins=10, color="teal", alpha=0.7)
        ax.set_xlabel("Relevance Score (%)")
        ax.set_ylabel("Number of Resumes")
        st.pyplot(fig)
    else:
        st.info("No results stored yet.")
