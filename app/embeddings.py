from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')  # small & fast

def semantic_score(resume_text: str, jd_text: str) -> float:
    embeddings = model.encode([resume_text, jd_text])
    sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(sim * 100, 2)