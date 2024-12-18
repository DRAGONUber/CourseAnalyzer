from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# Example model
class GradeDistribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(4), nullable=False)

@app.route('/')
def home():
    return "Flask app is running!"

if __name__ == "__main__":
    app.run(debug=True)
