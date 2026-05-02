# init_db.py
# 初始化数据库，只用运行一次

import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drone_id TEXT NOT NULL,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    capture_time TEXT NOT NULL,
    original_path TEXT NOT NULL,
    processed_path TEXT,
    status TEXT NOT NULL DEFAULT 'pending'
)
""")

conn.commit()
conn.close()