from flask import Blueprint, jsonify, request, send_from_directory
from ..models import db, Mission, IncidentLog
from datetime import datetime, timezone
import os

missions_bp = Blueprint('missions', __name__)

@missions_bp.route('/field-app')
def serve_user_app():
    static_dir = os.path.join(os.getcwd(), 'backend', 'static')
    return send_from_directory(static_dir, 'user_app.html')

@missions_bp.route('/', methods=['GET'])
def get_missions():
    missions = db.session.query(Mission).all()
    return jsonify([m.to_dict() for m in missions])

@missions_bp.route('/logs', methods=['GET'])
def get_logs():
    logs = db.session.query(IncidentLog).order_by(IncidentLog.timestamp.desc()).limit(15).all()
    return jsonify([{
        "callsign": l.callsign, 
        "event": l.event, 
        "time": l.timestamp.strftime('%H:%M:%S')
    } for l in logs])

@missions_bp.route('/trigger_sos', methods=['POST', 'OPTIONS'])
def trigger_sos_by_callsign():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    callsign = data.get('callsign')
    mission = db.session.query(Mission).filter_by(callsign=callsign).first()
    
    if not mission:
        return jsonify({"error": f"Callsign {callsign} not found in database"}), 404

    mission.status = 'SOS'
    mission.lat = data.get('lat', 0.0)
    mission.lng = data.get('lng', 0.0)
    
    log = IncidentLog(callsign=callsign, event="SOS ALERT TRIGGERED")
    db.session.add(log)
    db.session.commit()
    
    return jsonify({"message": "SOS RECEIVED"}), 200
    

@missions_bp.route('/resolve', methods=['POST'])
def resolve_mission():
    data = request.get_json()
    callsign = data.get('callsign')
    mission = db.session.query(Mission).filter_by(callsign=callsign).first()
    
    if mission:
        mission.status = 'Active'
        log = IncidentLog(callsign=callsign, event="INCIDENT RESOLVED / SAFE")
        db.session.add(log)
        db.session.commit()
        return jsonify({"message": "Resolved"}), 200
    return jsonify({"error": "Not found"}), 404