from app import create_app
from app.routes.main_routes import main_bp

# Define the Rasa endpoint for this specific deployment
rasa_endpoint = "http://localhost:5005/webhooks/rest/webhook"

app = create_app(rasa_endpoint)

if __name__ == '__main__':
    app.run(port=app.config['PORT'])