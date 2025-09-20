import docx2txt
import fitz  # PyMuPDF

def extract_text_from_pdf_or_docx(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        text = ""
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text("text")
        return text
    elif uploaded_file.name.endswith(".docx"):
        return docx2txt.process(uploaded_file)
    else:
        raise ValueError("Unsupported file type")

def parse_resume(resume_text):
    """Extract simple details like skills, projects, certifications"""
    skills = []
    certifications = []
    projects = []

    lines = resume_text.split("\n")
    for line in lines:
        if "project" in line.lower():
            projects.append(line.strip())
        if "certified" in line.lower() or "certificate" in line.lower():
            certifications.append(line.strip())

    return {
        "skills": skills,
        "certifications": certifications,
        "projects": projects
    }