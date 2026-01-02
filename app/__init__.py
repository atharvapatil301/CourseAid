import os
from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

load_dotenv()

app = Flask(
    __name__,
    template_folder="./view/templates",
    static_folder="./view/static"
)

app.secret_key = os.getenv("SECRET_KEY")

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="None",
)

CORS(
    app,
    supports_credentials=True,
    origins=["https://*.hf.space"]
)

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

from .middleware.auth import auth
app.register_blueprint(auth)

from .routes import api_routes
