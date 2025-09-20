# 🚀 Automated Resume Relevance Check System  

### Hackathon Project – Innomatics Research Labs  

---

## 📌 Problem Statement  
Recruiters at Innomatics Research Labs face **manual, inconsistent, and time-consuming** resume evaluations.  
Every week, 18–20 job requirements attract thousands of resumes, but:  
- Shortlisting is slow.  
- Judgments vary by evaluator.  
- Placement staff spend more time screening than guiding students.  

**Goal → Build an AI-powered system that automatically evaluates resumes against job descriptions.**  

---

## 🎯 Objectives  
- Automate resume–JD evaluation at scale.  
- Generate a **Relevance Score (0–100)**.  
- Provide a **fit verdict (High / Medium / Low)**.  
- Highlight **missing skills, certifications, or projects**.  
- Give **personalized improvement feedback** to students.  
- Store and display evaluations on a **web dashboard**.  

---

## 🛠️ Proposed Solution  
A hybrid **rule-based + AI-powered engine**:  
- **Resume Parsing**: Extract text from PDF/DOCX.  
- **JD Parsing**: Extract role title, must-have/good-to-have skills.  
- **Relevance Analysis**:  
  - Hard Match → Keyword & skill check.  
  - Semantic Match → Embedding similarity + LLM reasoning.  
- **Output**: Score, missing elements, and improvement tips.  
- **Dashboard**: Placement team can search/filter resumes by role, location, and score.  

---

## 🏗️ Workflow  

1. **Job Requirement Upload** – Placement team uploads JD.  
2. **Resume Upload** – Students upload PDF/DOCX resumes.  
3. **Parsing** – Extract and normalize text from resumes & JDs.  
4. **Relevance Analysis** – Hybrid scoring (hard + semantic).  
5. **Output** – Relevance score, missing skills, verdict, suggestions.  
6. **Storage** – Save results in database.  
7. **Dashboard** – Search & filter candidates easily.  

---

## ⚙️ Tech Stack  

### 🔹 Core (AI + Processing)  
- **Python** – main programming language.  
- **Text Extraction**: `PyMuPDF`, `pdfplumber`, `python-docx`, `docx2txt`.  
- **NLP**: `spaCy`, `NLTK`.  
- **Vector Store**: `Chroma` / `FAISS` / `Pinecone`.  
- **Keyword Matching**: TF-IDF, BM25, Fuzzy matching.  
- **Semantic Matching**: Embeddings + cosine similarity.  
- **LLM Orchestration**: `LangChain`, `LangGraph`, `LangSmith`.  
- **Models**: OpenAI GPT / Gemini / Claude / HuggingFace.  

### 🔹 Backend  
- **Flask** / **FastAPI** – REST APIs.  

### 🔹 Frontend  
- **Streamlit (MVP)** – Upload, dashboard, review interface.  
- (Optional) React.js for scalable production UI.  

### 🔹 Database  
- **SQLite / PostgreSQL** – Resume + JD + results storage.  

---

## 📊 Output Example  

**For each resume vs job description:**  
- ✅ Relevance Score: `82/100`  
- 📌 Missing Skills: `Docker, CI/CD, Azure`  
- 🏷 Verdict: `High Fit`  
- 💡 Suggestions:  
  - Add certification in cloud computing.  
  - Showcase project using Docker containers.  

---

## 🚀 How to Run Locally  

1. **Clone Repo**  
```bash
git clone https://github.com/<your-username>/resume-relevance-check.git
cd resume-relevance-check
