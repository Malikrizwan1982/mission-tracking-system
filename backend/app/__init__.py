import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize the database object
db = SQLAlchemy()

def create_app():
    # Initialize the Flask application
    app = Flask(__name__)
    
    # --- CRITICAL FIX: Enable CORS ---
    # This allows your index.html (frontend) to communicate with this API (backend)
    CORS(app)

    # Configuration
    # Using a relative path for the SQLite database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'missions.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app context
    db.init_app(app)

    # Register Blueprints
    from .routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Create database tables if they don't exist
    with app.app_context():
        from .models import Mission, IncidentLog
        db.create_all()

    return app