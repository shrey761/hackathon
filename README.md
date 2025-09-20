# Automated Resume Relevance Check System

*Hackathon Project – Innomatics Research Labs*

---

## Problem Statement

Recruiters face many challenges when screening resumes for job openings:

- Manual resume evaluation is time‐consuming and inconsistent.  
- Every week, 18–20 job requirements may get thousands of resumes to review.  
- Placement staff spend more time filtering resumes than guiding students.  

*Goal:* Build an AI‐powered system that automatically evaluates resumes against job descriptions (JDs), speeding up shortlisting, standardizing decisions, and providing useful feedback to candidates.

---

## Objectives

- Automate resume‑vs‑JD evaluation at scale.  
- Generate a *Relevance Score* (0‑100).  
- Provide a fit verdict: High / Medium / Low.  
- Identify missing skills, certifications, or projects.  
- Give personalized feedback for improvement.  
- Store and display evaluations via a dashboard.

---

## Proposed Solution

A hybrid system combining rule‑based matching with semantic/AI‑based analysis:

1. *Resume Parsing*  
   - Extract text from PDF / DOCX resumes.

2. *Job Description (JD) Parsing*  
   - Extract role title, must‑have & good‑to‑have skills, etc.

3. *Relevance Analysis*  
   - *Hard Match*: Check keywords / exact skill match.  
   - *Semantic Match*: Use embeddings, cosine similarity & possibly LLM reasoning to capture implicit semantic similarity.

4. *Output*  
   - Relevance score.  
   - Missing skills / gaps.  
   - Verdict (High / Medium / Low).  
   - Suggestions & improvement tips for the candidate.

5. *Dashboard*  
   - For placement/HR team to upload JDs, resumes, search/filter candidates (by score, role, etc.), view results.

---

## Workflow

1. Upload Job Description (JD)  
2. Students upload their resume in PDF / DOCX format  
3. System parses and normalizes text from resumes & JDs  
4. Run relevance scoring (hard + semantic methods)  
5. Produce outputs: score, missing items, verdict, suggestions  
6. Store results in database  
7. Dashboard to browse/search/filter results  

---

## Tech Stack

| Layer | Technologies |
|-------|--------------|
| *Core / AI & NLP* | Python; text extraction via PyMuPDF, pdfplumber, python‑docx, docx2txt |
| | NLP: spaCy, NLTK |
| | Embeddings / Semantic matching: vector store (Chroma / FAISS / Pinecone), cosine similarity |
| | Keyword matching: TF‑IDF, BM25, fuzzy matching |
| | Optional LLM integration: (e.g. via LangChain, etc.) for reasoning or enhanced suggestions |
| *Backend* | Flask or FastAPI (REST APIs) |
| *Frontend / UI* | Streamlit (MVP); optional React.js for more advanced UI |
| *Storage / Database* | SQLite / PostgreSQL for storing resumes, JDs, evaluation results |

---

## Output Example

Here’s what a sample evaluation might look like:

- *Relevance Score:* 82 / 100  
- *Verdict:* High Fit  
- *Missing Skills:* Docker, CI/CD, Azure  
- *Suggestions:*  
  • Add certification in cloud computing  
  • Include a project using Docker containers  
  • Highlight continuous integration / deployment experience  

---

## Installation & Running Locally

> *Prerequisites:* Python 3.8+, git, (optionally) virtual environment

```bash
# 1. Clone the repository
git clone https://github.com/shrey761/hackathon.git
cd hackathon

# 2. Create and activate a virtual environment (recommended)
python ‑m venv venv
source venv/bin/activate   # on Unix / Mac
# or
venv\Scripts\activate      # on Windows

# 3. Install required dependencies
pip install ‑r requirements.txt

# 4. Obtain / setup any additional resources:
#    ‑ For spaCy models: e.g. python ‑m spacy download en_core_web_sm
#    ‑ Setting up vector store or embedding model (if used)
#    ‑ If using any external APIs / LLMs, set API keys or credentials

# 5. Run the app
streamlit run streamlit_app.py

# 6. Use via the UI: upload JD / resume to test, view results, etc.
