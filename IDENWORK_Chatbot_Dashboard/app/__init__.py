"""Uygulama fabrikası; modülleri bir araya getirir."""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config_by_name
from app.database import init_db
from app.routes import api, pages

def create_app(config_name=None):
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['development']))
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax', MAX_CONTENT_LENGTH=16384)
    CORS(app, resources={r'/api/sohbet': {'origins': app.config['CORS_ORIGINS']},
                         r'/api/leads': {'origins': app.config['CORS_ORIGINS']}},
         supports_credentials=False)
    init_db(app)
    app.register_blueprint(pages)
    app.register_blueprint(api, url_prefix='/api')

    @app.get('/health')
    def health():
        return jsonify(basari=True, durum='aktif', uygulama='IDENWORK')
    return app
