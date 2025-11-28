# app.py
from flask import Flask
from flask_cors import CORS
from routes.exif_routes import exif_bp

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)  # Para que tu frontend (otra URL) pueda llamar a la API

    # Registramos los endpoints de EXIF bajo /api
    app.register_blueprint(exif_bp, url_prefix="/api")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
