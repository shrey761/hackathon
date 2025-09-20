from fastapi import FastAPI, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app import resume_parser, jd_parser, scoring, database, crud, models

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=database.engine)

@app.post("/evaluate/")
async def evaluate_resume(
    file: UploadFile = File(...),
    jd_text: str = Form(...),
    db: Session = Depends(database.get_db)
):
    resume_text = resume_parser.extract_text(file)
    jd_data = jd_parser.parse_jd(jd_text)

    # Scoring
    result = scoring.compute_hybrid_score(resume_text, jd_text)

    # Missing skills
    missing = [skill for skill in jd_data["must_have"] if skill.lower() not in resume_text.lower()]

    # Save to DB
    record = crud.save_evaluation(
        db, file.filename, result["relevance"], result["verdict"], missing
    )

    return {
        "filename": record.filename,
        "score": record.relevance_score,
        "verdict": record.verdict,
        "missing_skills": record.missing_skills.split(", ") if record.missing_skills else []
    }

@app.get("/evaluations/")
def list_evaluations(db: Session = Depends(database.get_db)):
    records = crud.get_all_evaluations(db)
    return records