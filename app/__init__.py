import os
from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
from huggingface_hub import login


load_dotenv()


app = Flask(
    __name__,
    template_folder="./view/templates",
    static_folder="./view/static"
)

app.secret_key = os.getenv("SECRET_KEY")

app.config.update(
<<<<<<< HEAD
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
=======
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="None",
>>>>>>> a8e0d50e58841acb595f9e9cda69e72190832a33
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

# login(token=os.getenv("HUGGINGFACE_HUB_TOKEN"))