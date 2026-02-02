from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    from .routes import stories_bp, pages_bp, choices_bp
    app.register_blueprint(stories_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(choices_bp)
    
    return app
