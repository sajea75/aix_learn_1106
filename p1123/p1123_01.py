from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
conn = sqlite3.connect(BASE_DIR / "data" / "aix_curriculum_db.sqlite3")

# 1. 들어있는 테이블 목록 확인
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("=== 테이블 목록 ===")
print(tables)

# 2. 커리큘럼 단계 & 학습 카드 내용 확인
steps_df = pd.read_sql_query("SELECT step, month, category, title FROM course_steps;", conn)
cards_df = pd.read_sql_query("SELECT step_id, badge, title, body FROM lesson_cards;", conn)

print("\n=== 단계 목록 ===")
print(steps_df)
print("\n=== 학습 카드 (상위 5개) ===")
print(cards_df.head())

conn.close()