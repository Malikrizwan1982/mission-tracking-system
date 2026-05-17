from app import create_app, db
from app.models import Mission, IncidentLog
from datetime import datetime

app = create_app()

with app.app_context():
    # 1. Clear existing data to prevent 'Unique Constraint' errors
    db.session.query(Mission).delete()
    db.session.query(IncidentLog).delete()

    # 2. Define the fleet of 10 missions
    missions_data = [
        {"callsign": "UN-99", "agency": "UNOCHA", "status": "Active", "lat": 34.34, "lng": 71.43},
        {"callsign": "WFP-01", "agency": "WFP", "status": "Active", "lat": 34.36, "lng": 71.45},
        {"callsign": "WHO-05", "agency": "WHO", "status": "SOS", "lat": 34.38, "lng": 71.40},
        {"callsign": "UNDP-12", "agency": "UNDP", "status": "Standby", "lat": 34.32, "lng": 71.48},
        {"callsign": "UNICEF-08", "agency": "UNICEF", "status": "Active", "lat": 34.40, "lng": 71.35},
        {"callsign": "MOGIP-22", "agency": "UNMOGIP", "status": "Active", "lat": 34.30, "lng": 71.50},
        {"callsign": "WFP-07", "agency": "WFP", "status": "Standby", "lat": 34.35, "lng": 71.42},
        {"callsign": "WHO-02", "agency": "WHO", "status": "Active", "lat": 34.39, "lng": 71.47},
        {"callsign": "UN-55", "agency": "UNOCHA", "status": "SOS", "lat": 34.31, "lng": 71.41},
        {"callsign": "UNICEF-03", "agency": "UNICEF", "status": "Active", "lat": 34.37, "lng": 71.49},
    ]

    # 3. Add missions to the database
    for data in missions_data:
        mission = Mission(
            callsign=data["callsign"],
            agency=data["agency"],
            status=data["status"],
            lat=data["lat"],
            lng=data["lng"]
        )
        db.session.add(mission)
        
        # Add an initial log for each
        log = IncidentLog(
            callsign=data["callsign"],
            event=f"Initial deployment for {data['agency']}",
            time=datetime.now().strftime("%H:%M:%S")
        )
        db.session.add(log)

    # 4. Commit all changes
    db.session.commit()
    print(f"Success! {len(missions_data)} missions and logs have been seeded.")