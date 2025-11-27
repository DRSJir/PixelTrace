import pandas as pd
from pathlib import Path

# Ruta del CSV (ajusta el nombre si es diferente)
RUTA_CSV = Path(__file__).parent / "censo.csv"

# Cargamos el archivo una sola vez
# Si hay problema con la codificación, prueba con encoding="latin-1"
censo_df = pd.read_csv(RUTA_CSV)

# Nos quedamos con columnas relevantes para el prototipo
# (ajusta si tu archivo tiene nombres ligeramente distintos)
COLUMNAS_MINIMAS = ["ENTIDAD", "NOM_ENT", "MUN", "NOM_MUN", "POBTOT"]
for col in COLUMNAS_MINIMAS:
    if col not in censo_df.columns:
        raise ValueError(f"Falta la columna requerida en el CSV: {col}")


def obtener_estados_disponibles():
    """Regresa la lista de nombres de entidades (NOM_ENT) sin repetir, ordenada."""
    return sorted(censo_df["NOM_ENT"].unique().tolist())


def obtener_poblacion_por_estado(estado: str):
    """
    Devuelve un diccionario con la población total del estado.
    Suma POBTOT de todas sus filas (municipios/localidades).
    """
    filtro = censo_df[censo_df["NOM_ENT"] == estado]

    if filtro.empty:
        return None

    pobtot = int(filtro["POBTOT"].sum())

    return {
        "estado": estado,
        "poblacion_total": pobtot,
        "anio_censo": 2020,  # fijo para el prototipo
    }


def obtener_municipios_por_estado(estado: str):
    """Regresa la lista de municipios (NOM_MUN) para un estado."""
    filtro = censo_df[censo_df["NOM_ENT"] == estado]
    if filtro.empty:
        return []
    return sorted(filtro["NOM_MUN"].unique().tolist())


def obtener_tabla_municipio_edad(estado: str, municipio: str, edad_min: int, edad_max: int):
    """
    Prototipo:
    - Toma la población total del municipio (POBTOT).
    - La reparte entre las edades del rango usando pesos (no uniforme),
      solo para evitar que todas las edades tengan el mismo valor.

    IMPORTANTE: Esto sigue siendo una simulación. El CSV no tiene datos por edad exacta.
    """
    filtro = censo_df[
        (censo_df["NOM_ENT"] == estado) & (censo_df["NOM_MUN"] == municipio)
    ]

    if filtro.empty:
        raise ValueError(f"No se encontró el municipio {municipio} en el estado {estado}")

    pobtot = int(filtro["POBTOT"].sum())
    edades = list(range(edad_min, edad_max + 1))
    n_edades = len(edades)

    if n_edades <= 0:
        raise ValueError("El rango de edad es inválido")

    # Definimos pesos para cada edad (por ejemplo, más peso en edades medias)
    # Aquí usamos una distribución "triangular" simple:
    # pesos que suben hasta la mitad y luego bajan.
    mitad = n_edades // 2
    pesos = []

    for i in range(n_edades):
        if i <= mitad:
            # sube
            peso = i + 1
        else:
            # baja
            peso = n_edades - i
        pesos.append(peso)

    suma_pesos = sum(pesos)

    # Calculamos personas por edad según los pesos
    personas_por_edad = []
    for peso in pesos:
        personas = (pobtot * peso) // suma_pesos
        personas_por_edad.append(personas)

    # Ajuste por residuo para que la suma coincida exactamente con pobtot
    residuo = pobtot - sum(personas_por_edad)
    i = 0
    while residuo > 0 and i < n_edades:
        personas_por_edad[i] += 1
        residuo -= 1
        i += 1

    # Armamos la tabla
    tabla = []
    for edad, personas in zip(edades, personas_por_edad):
        fila = {
            "edad": edad,
            "personas": personas,
        }
        tabla.append(fila)

    return {
        "estado": estado,
        "municipio": municipio,
        "rango_edad": (edad_min, edad_max),
        "anio_censo": 2020,
        "tabla": tabla,
    }


def construir_datos_grafico_por_estado(estado: str):
    """Devuelve datos para un gráfico de barras por estado (una barra por ahora)."""
    datos_estado = obtener_poblacion_por_estado(estado)
    if not datos_estado:
        return None

    return {
        "tipo": "barras",
        "datos": [
            {
                "estado": datos_estado["estado"],
                "poblacion": datos_estado["poblacion_total"],
            }
        ],
    }
