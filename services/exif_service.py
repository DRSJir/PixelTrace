# services/exif_service.py
from __future__ import annotations
from typing import Any, Dict, Optional, Tuple

import piexif


def _rational_to_float(value: Optional[Tuple[int, int]]) -> Optional[float]:
    """
    Convierte un valor racional de piexif (num, den) a float.
    """
    if not value:
        return None
    num, den = value
    if den == 0:
        return None
    return num / den


def _get_tag(exif_dict: dict, ifd_name: str, tag_id: int) -> Any:
    """
    Helper genérico para leer un tag de un IFD concreto.
    ifd_name suele ser '0th', 'Exif', 'GPS', '1st'.
    """
    if ifd_name not in exif_dict:
        return None
    return exif_dict[ifd_name].get(tag_id)


def _gps_to_decimal(coord, ref) -> Optional[float]:
    """
    Convierte coordenadas GPS (en formato d/m/s racional de piexif) a grados decimales.
    coord: ((deg_num,deg_den), (min_num,min_den), (sec_num,sec_den))
    ref: b'N' | b'S' | b'E' | b'W'
    """
    if not coord or not ref:
        return None

    def _rat(v):
        return _rational_to_float(v) or 0.0

    deg = _rat(coord[0])
    mins = _rat(coord[1])
    secs = _rat(coord[2])

    decimal = deg + mins / 60.0 + secs / 3600.0

    if ref in [b"S", b"W"]:
        decimal = -decimal

    return decimal


def extract_exif_from_bytes(image_bytes: bytes) -> Dict[str, Any]:
    """
    Lógica de negocio:
    - Recibe bytes de una imagen.
    - Usa piexif para extraer el EXIF.
    - Devuelve un diccionario 'limpio' listo para el frontend.
    """

    # Cargar EXIF con piexif
    exif_dict = piexif.load(image_bytes)

    # Acceso directo a tags que nos interesan
    model = _get_tag(exif_dict, "0th", piexif.ImageIFD.Model)
    make = _get_tag(exif_dict, "0th", piexif.ImageIFD.Make)

    focal_length = _rational_to_float(
        _get_tag(exif_dict, "Exif", piexif.ExifIFD.FocalLength)
    )

    f_number = _rational_to_float(
        _get_tag(exif_dict, "Exif", piexif.ExifIFD.FNumber)
    )

    iso = _get_tag(exif_dict, "Exif", piexif.ExifIFD.ISOSpeedRatings)
    exposure_time = _get_tag(exif_dict, "Exif", piexif.ExifIFD.ExposureTime)
    exposure_comp = _rational_to_float(
        _get_tag(exif_dict, "Exif", piexif.ExifIFD.ExposureBiasValue)
    )

    # Fecha de captura
    datetime_original = _get_tag(exif_dict, "Exif", piexif.ExifIFD.DateTimeOriginal)

    # Tamaño / orientación, etc.
    orientation = _get_tag(exif_dict, "0th", piexif.ImageIFD.Orientation)

    # GPS
    gps_lat = _get_tag(exif_dict, "GPS", piexif.GPSIFD.GPSLatitude)
    gps_lat_ref = _get_tag(exif_dict, "GPS", piexif.GPSIFD.GPSLatitudeRef)
    gps_lng = _get_tag(exif_dict, "GPS", piexif.GPSIFD.GPSLongitude)
    gps_lng_ref = _get_tag(exif_dict, "GPS", piexif.GPSIFD.GPSLongitudeRef)

    lat_decimal = _gps_to_decimal(gps_lat, gps_lat_ref)
    lng_decimal = _gps_to_decimal(gps_lng, gps_lng_ref)

    gps = None
    if lat_decimal is not None and lng_decimal is not None:
        gps = {"lat": lat_decimal, "lng": lng_decimal}

    # armamos un diccionario "bonito" para el frontend
    exif_clean = {
        "cameraMake": make.decode("utf-8") if isinstance(make, bytes) else make,
        "cameraModel": model.decode("utf-8") if isinstance(model, bytes) else model,
        "focalLength_mm": focal_length,           # en mm
        "aperture_fNumber": f_number,             # f/1.8 -> 1.8
        "iso": iso,
        "exposureTime": exposure_time,            # tu frontend puede mostrarlo como fracción
        "exposureComp_ev": exposure_comp,
        "orientation": orientation,
        "datetimeOriginal": datetime_original.decode("utf-8")
        if isinstance(datetime_original, bytes)
        else datetime_original,
        "gps": gps,
    }

    return exif_clean
