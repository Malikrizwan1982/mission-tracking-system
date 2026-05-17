from app import db
from datetime import datetime

class Mission(db.Model):
    """
    Stores the status and location of field units (UN-99, WFP-01, etc.)
    """
    __tablename__ = 'missions'
    
    id = db.Column(db.Integer, primary_key=True)
    callsign = db.Column(db.String(50), unique=True, nullable=False)
    agency = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default='Active')  # Active, SOS, Standby
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Mission {self.callsign} - {self.status}>'

class IncidentLog(db.Model):
    """
    Stores a history of all status updates and emergencies for the Radio Room
    """
    __tablename__ = 'incident_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    callsign = db.Column(db.String(50), nullable=False)
    event = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(50), nullable=False)  # Formatted string for UI display
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Log {self.callsign} at {self.time}>'