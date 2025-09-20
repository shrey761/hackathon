import PyPDF2
import docx2txt
import os

def parse_resume(file):
    """
    Extract text from uploaded resume file (.pdf or .docx).
    """
    text = ""

    # Handle PDF resumes
    if file.name.lower().endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

    # Handle DOCX resumes
    elif file.name.lower().endswith(".docx"):
        # docx2txt needs a file path, so save temporarily
        temp_path = "temp_resume.docx"
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())
        text = docx2txt.process(temp_path)
        os.remove(temp_path)

    else:
        raise ValueError("Unsupported file format. Please upload .pdf or .docx file.")

    return text.strip()