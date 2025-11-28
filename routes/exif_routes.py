# routes/exif_routes.py
from flask import Blueprint, request, jsonify
from services.exif_service import extract_exif_from_bytes

exif_bp = Blueprint("exif", __name__)


@exif_bp.route("/exif", methods=["POST"])
def upload_and_extract_exif():
    """
    Endpoint que recibe una imagen (form-data, campo 'image')
    y devuelve los metadatos EXIF relevantes en JSON.
    """
    if "image" not in request.files:
        return jsonify({"error": "No se encontró el archivo 'image' en la petición"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "El archivo no tiene nombre"}), 400

    # Leemos los bytes (lógica de negocio va en services)
    image_bytes = file.read()

    try:
        exif_data = extract_exif_from_bytes(image_bytes)
    except Exception as e:
        # Aquí solo traducimos errores técnicos a respuesta HTTP
        return jsonify({"error": f"No fue posible extraer EXIF: {str(e)}"}), 500

    return jsonify({"exif": exif_data}), 200
