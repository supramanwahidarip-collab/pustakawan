import os
from flask import Flask
from app.config import Config
from app.extensions import db, login_manager, csrf

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app import models

    # Registrasi Blueprints (Hanya 3 ini saja yang aktif)
    from app.blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.blueprints.librarian import librarian_bp
    app.register_blueprint(librarian_bp)

    from app.blueprints.member import member_bp
    app.register_blueprint(member_bp)

    @app.route('/health')
    def health_check():
        return {"status": "healthy", "system": "Tosca Library Enterprise API"}, 200

    return app