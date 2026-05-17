from flask import Blueprint, request, jsonify
from app import db
from app.models import Mission, IncidentLog
from datetime import datetime

# Define the blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/missions/', methods=['GET', 'OPTIONS'])
def get_missions():
    if request.method == 'OPTIONS':
        return jsonify({"success": True}), 200
    try:
        # Fetch all missions from the database
        missions = db.session.query(Mission).all()
        return jsonify([{
            "callsign": m.callsign,
            "agency": m.agency,
            "status": m.status,
            "lat": m.lat,
            "lng": m.lng
        } for m in missions])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/missions/update', methods=['POST', 'OPTIONS'])
def update_mission():
    # Handle Pre-flight requests for CORS
    if request.method == 'OPTIONS':
        return jsonify({"success": True}), 200
        
    data = request.get_json()
    
    # 1. Find the existing mission by callsign
    mission = db.session.query(Mission).filter_by(callsign=data['callsign']).first()
    
    if not mission:
        return jsonify({"msg": "Callsign not found"}), 404

    # 2. Update the mission status and location
    old_status = mission.status
    mission.status = data['status']
    mission.lat = data['lat']
    mission.lng = data['lng']
    
    # 3. AUTO-LOGGING: If status changed, create an Incident Log entry
    if old_status != data['status']:
        new_log = IncidentLog(
            callsign=mission.callsign,
            event=f"Status changed from {old_status} to {data['status']}",
            time=datetime.now().strftime("%H:%M:%S")
        )
        db.session.add(new_log)
    
    try:
        db.session.commit()
        return jsonify({"msg": "Success", "status": mission.status}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api_bp.route('/missions/logs', methods=['GET'])
def get_logs():
    try:
        # Get the 10 most recent logs
        logs = db.session.query(IncidentLog).order_by(IncidentLog.id.desc()).limit(10).all()
        return jsonify([{"callsign": l.callsign, "event": l.event, "time": l.time} for l in logs])
    except Exception as e:
        return jsonify({"error": str(e)}), 500