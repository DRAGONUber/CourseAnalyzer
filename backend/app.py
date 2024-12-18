from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    CORS(app)
    db.init_app(app)

    with app.app_context():
        from routes.grade_routes import grade_routes
        app.register_blueprint(grade_routes)
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
