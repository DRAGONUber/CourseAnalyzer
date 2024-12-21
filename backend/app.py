from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from db import db
from models import Chain, MasterKey, Token, Wallet, Transaction, GradeDistribution
from routes.chains import chains_bp
from routes.master_keys import master_keys_bp
from routes.tokens import tokens_bp
from routes.wallets import wallets_bp
from routes.transactions import transactions_bp

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Fetch DATABASE_URL or raise an error if it's not set
database_uri = os.getenv('DATABASE_URL')
if not database_uri:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Register Blueprints
app.register_blueprint(chains_bp, url_prefix="/api/chains")
app.register_blueprint(master_keys_bp, url_prefix="/api/master_keys")
app.register_blueprint(tokens_bp, url_prefix="/api/tokens")
app.register_blueprint(wallets_bp, url_prefix="/api/wallets")
app.register_blueprint(transactions_bp, url_prefix="/api/transactions")

@app.route('/')
def home():
    return "Flask app is running!"

if __name__ == "__main__":
    app.run(debug=True)
