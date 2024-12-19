from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from db import db
from models import GradeDistribution  # Import models after db initialization

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Fetch DATABASE_URL or raise an error if it's not set
database_uri = os.getenv('DATABASE_URL')
print(f"DATABASE_URL: {database_uri}")  # Debugging statement

if not database_uri:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Import and register Blueprints after initializing extensions
from routes.grade_routes import grade_routes
app.register_blueprint(grade_routes, url_prefix="/api")

@app.route('/')
def home():
    return "Flask app is running!"

if __name__ == "__main__":
    app.run(debug=True)