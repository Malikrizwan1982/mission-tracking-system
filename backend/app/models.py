from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    callsign = db.Column(db.String(50), unique=True, nullable=False)
    agency = db.Column(db.String(50))
    status = db.Column(db.String(20), default='Active')
    landmark = db.Column(db.String(100))
    lat = db.Column(db.Float, default=0.0)
    lng = db.Column(db.Float, default=0.0)
    last_contact = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "callsign": self.callsign,
            "agency": self.agency,
            "status": self.status,
            "landmark": self.landmark,
            "lat": self.lat,
            "lng": self.lng,
            "last_contact": self.last_contact.isoformat() if self.last_contact else None
        }

class IncidentLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    callsign = db.Column(db.String(50))
    event = db.Column(db.String(100)) 
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))