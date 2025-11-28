# app.py
from flask import Flask
from flask_cors import CORS

from routes.exif_routes import exif_bp
from routes.ui_routes import ui_bp


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    # API REST
    app.register_blueprint(exif_bp, url_prefix="/api")

    # Vistas HTML
    app.register_blueprint(ui_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
