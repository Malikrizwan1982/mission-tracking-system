from app import create_app, db
from app.models import Mission

app = create_app()
with app.app_context():
    # Ensure tables are created
    db.create_all()
    
    # Coordinates for KPK, Pakistan
    units = [
        # Peshawar - Hayatabad Area
        Mission(
            callsign="UN-99", 
            agency="UNICEF", 
            landmark="Hayatabad Medical Complex", 
            lat=33.9850, 
            lng=71.4320
        ),
        # Swat - Mingora Area
        Mission(
            callsign="WFP-01", 
            agency="WFP", 
            landmark="Mingora Central Hub", 
            lat=34.7717, 
            lng=72.3602
        ),
        # Nowshera - Risalpur Area
        Mission(
            callsign="DSS-10", 
            agency="UNDSS", 
            landmark="Nowshera Cantt", 
            lat=34.0150, 
            lng=71.9750
        )
    ]
    
    print("Cleaning old data and seeding KPK locations...")
    # Clear old entries to avoid coordinate confusion
    db.session.query(Mission).delete() 
    
    for u in units:
        db.session.add(u)
    
    db.session.commit()
    print("✅ Success! Missions moved to Peshawar, Swat, and Nowshera.")