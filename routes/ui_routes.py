# routes/ui_routes.py
from flask import Blueprint, render_template, request
from services.exif_service import extract_exif_from_bytes
from base64 import b64encode

ui_bp = Blueprint("ui", __name__)


@ui_bp.route("/", methods=["GET", "POST"])
def index():
    exif_data = None
    error = None
    image_data_url = None  # <- aquí guardaremos la imagen en base64

    if request.method == "POST":
        if "image" not in request.files:
            error = "No se encontró el archivo 'image' en la petición."
        else:
            file = request.files["image"]
            if file.filename == "":
                error = "Debes seleccionar un archivo de imagen."
            else:
                try:
                    # 1) Leemos los bytes
                    image_bytes = file.read()

                    # 2) Extraemos EXIF (lógica de negocio sigue en services)
                    exif_data = extract_exif_from_bytes(image_bytes)

                    # 3) Construimos el data URL para mostrar la imagen sin guardarla
                    mime_type = file.mimetype or "image/jpeg"
                    encoded = b64encode(image_bytes).decode("utf-8")
                    image_data_url = f"data:{mime_type};base64,{encoded}"

                except Exception as e:
                    error = f"No fue posible extraer los metadatos EXIF: {str(e)}"

    # Pasamos image_data_url al template
    return render_template(
        "index.html",
        exif=exif_data,
        error=error,
        image_data_url=image_data_url,
    )
