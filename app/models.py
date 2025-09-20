from sqlalchemy import Column, Integer, String, Float, Text
from app.database import Base

class Evaluation(Base):
    _tablename_ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    relevance_score = Column(Float, nullable=False)
    verdict = Column(String, nullable=False)
    missing_skills = Column(Text)   # store as comma-separated string