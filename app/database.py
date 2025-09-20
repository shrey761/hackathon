# app/database.py
import sqlite3
import pandas as pd   # ✅ Fix: Added missing pandas import

DB_PATH = "results.db"

# ===============================
# Save results into SQLite
# ===============================
def save_result(resume_name, score, verdict, feedback):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_name TEXT,
            score REAL,
            verdict TEXT,
            feedback TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO results (resume_name, score, verdict, feedback)
        VALUES (?, ?, ?, ?)
    """, (resume_name, score, verdict, feedback))
    conn.commit()
    conn.close()

# ===============================
# Load results into DataFrame
# ===============================
def load_results():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM results", conn)  # ✅ Needs pandas
    conn.close()
    return df