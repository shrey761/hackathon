import pdfplumber, docx2txt, tempfile

def extract_text(file):
    if file.filename.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.file.read())
            with pdfplumber.open(tmp.name) as pdf:
                return "\n".join([p.extract_text() or "" for p in pdf.pages])
    elif file.filename.endswith(".docx"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file.file.read())
            return docx2txt.process(tmp.name)
    else:
        return "Unsupported file type"