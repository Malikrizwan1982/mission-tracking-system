import sqlite3
import os
from datetime import datetime, timezone

def populate_mock_data():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    db_path = os.path.join(base_dir, "instance", "mts.db")
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the table if it's missing (The Safety Net)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            callsign TEXT NOT NULL UNIQUE,
            agency TEXT NOT NULL,
            pax_count INTEGER,
            status TEXT,
            last_landmark TEXT,
            last_contact DATETIME,
            start_time DATETIME
        )
    ''')

    mock_missions = [
        ('UN-402', 'WFP', 4, 'Active', 'Sector A - Main Road'),
        ('UN-105', 'UNICEF', 2, 'Standby', 'Hospital Delta'),
        ('UN-99', 'UNDSS', 3, 'Breach', 'Checkpoint 4'),
        ('UN-701', 'WHO', 5, 'Active', 'Village North')
    ]

    current_time = datetime.now(timezone.utc)

    for m in mock_missions:
        try:
            cursor.execute('''
                INSERT INTO missions (callsign, agency, pax_count, status, last_landmark, last_contact, start_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (m[0], m[1], m[2], m[3], m[4], current_time, current_time))
        except sqlite3.IntegrityError:
            print(f"Mission {m[0]} already exists.")

    conn.commit()
    conn.close()
    print("Database populated successfully!")

if __name__ == "__main__":
    populate_mock_data()