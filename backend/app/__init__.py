from flask import Flask
from flask_cors import CORS
from .models import db

def create_app():
    app = Flask(__name__)
    

    # This line is the "Security Pass" for your browser
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mts.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database WITH the app
    db.init_app(app)

    with app.app_context():
        from .routes.missions import missions_bp
        app.register_blueprint(missions_bp, url_prefix='/api/missions')
        db.create_all()

    return app