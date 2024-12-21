import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Database connection parameters
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
DATABASE_URL = os.getenv('DATABASE_URL')


def create_database():
    """Create the PostgreSQL database if it doesn't exist."""
    try:
        # Connect to the default 'postgres' database to create a new database
        conn = psycopg2.connect(
            dbname='postgres',
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if the database exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{POSTGRES_DB}';")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f'CREATE DATABASE {POSTGRES_DB};')
            print(f"Database '{POSTGRES_DB}' created successfully.")
        else:
            print(f"Database '{POSTGRES_DB}' already exists.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")


def create_tables():
    """Create tables based on SQLAlchemy models."""
    from app import app
    from models import db

    with app.app_context():
        try:
            db.create_all()
            print("Tables created successfully (if they did not exist).")
        except Exception as e:
            print(f"Error creating tables: {e}")


if __name__ == "__main__":
    create_database()
    create_tables()
