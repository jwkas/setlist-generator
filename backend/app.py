from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app(config_class=Config):
    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    CORS(app)  # Enable CORS for all routes
    db.init_app(app)
    
    # Import models for SQLAlchemy to detect them
    from models import Song, Setlist
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Import and register blueprints
    from routes import api_bp
    app.register_blueprint(api_bp)
    
    return app
