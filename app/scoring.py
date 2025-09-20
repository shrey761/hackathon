from sklearn.feature_extraction.text import TfidfVectorizer
from app.embeddings import semantic_score

def hard_score(resume_text: str, jd_text: str) -> float:
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([resume_text, jd_text])
    score = (tfidf * tfidf.T).A[0,1]  # cosine sim from tfidf
    return round(score * 100, 2)

def compute_hybrid_score(resume_text: str, jd_text: str):
    hs = hard_score(resume_text, jd_text)
    ss = semantic_score(resume_text, jd_text)
    relevance = round(0.55 * hs + 0.45 * ss, 2)

    verdict = "High Fit" if relevance >= 75 else "Medium Fit" if relevance >= 50 else "Low Fit"

    return {"hard_score": hs, "semantic_score": ss, "relevance": relevance, "verdict": verdict}