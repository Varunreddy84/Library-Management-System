import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Database configuration
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "library_db")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    db.init_app(app)

    # Register blueprints
    from routes.main import main_bp
    from routes.authors import authors_bp
    from routes.books import books_bp
    from routes.members import members_bp
    from routes.loans import loans_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(authors_bp, url_prefix="/authors")
    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(members_bp, url_prefix="/members")
    app.register_blueprint(loans_bp, url_prefix="/loans")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
