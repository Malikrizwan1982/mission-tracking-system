import sqlite3
import os

db_path = os.path.join("instance", "mts.db")
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, callsign, status FROM missions")
        rows = cursor.fetchall()
        if not rows:
            print("Table exists, but it is EMPTY.")
        for row in rows:
            print(f"ID: {row[0]} | Callsign: {row[1]} | Status: {row[2]}")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    finally:
        conn.close()
else:
    print(f"Database file not found at {db_path}")