import os
from flask import Flask
from .config import Config
from .routes.main_routes import main_bp

def create_app(rasa_endpoint):
    app = Flask(__name__)

    # # Configure session settings (e.g., use secure cookies if in production)
    # app.secret_key = 'your_secret_key'
    
    # Register blueprints
    app.register_blueprint(main_bp)

    # Load configuration from the Config class
    app.config.from_object(Config)

    # Set the Rasa endpoint in the app configuration
    app.config['RASA_NLU_ENDPOINT'] = rasa_endpoint
    
    # API keys
    app.config['TWILIO_ACCOUNT_SID'] = os.environ.get('TWILIO_ACCOUNT_SID')
    app.config['TWILIO_AUTH_TOKEN'] = os.environ.get("TWILIO_AUTH_TOKEN")
    
    # Check if required environment variables are present
    if not app.config['TWILIO_ACCOUNT_SID'] or not app.config['TWILIO_AUTH_TOKEN']:
        raise ValueError("TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables are required.")

    # Additional app configurations and extensions

    return app
