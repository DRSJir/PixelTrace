from flask import Flask, render_template, request, jsonify
from censo_servicio import (
    obtener_poblacion_por_estado,
    obtener_tabla_municipio_edad,
    construir_datos_grafico_por_estado,
    obtener_estados_disponibles,
    obtener_municipios_por_estado,
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    resultado_estado = None
    resultado_municipio = None
    datos_grafico = None

    lista_estados = obtener_estados_disponibles()

    if request.method == "POST":
        tipo_consulta = request.form.get("tipo_consulta")

        if tipo_consulta == "estado":
            estado = request.form.get("estado")
            resultado_estado = obtener_poblacion_por_estado(estado)
            datos_grafico = construir_datos_grafico_por_estado(estado)

        elif tipo_consulta == "municipio":
            estado = request.form.get("estado")
            municipio = request.form.get("municipio")
            edad_min = int(request.form.get("edad_min"))
            edad_max = int(request.form.get("edad_max"))
            resultado_municipio = obtener_tabla_municipio_edad(
                estado, municipio, edad_min, edad_max
            )

    return render_template(
        "index.html",
        resultado_estado=resultado_estado,
        resultado_municipio=resultado_municipio,
        datos_grafico=datos_grafico,
        lista_estados=lista_estados,
    )

@app.route("/municipios")
def municipios():
    estado = request.args.get("estado")
    if not estado:
        return jsonify([])

    municipios = obtener_municipios_por_estado(estado)
    return jsonify(municipios)


if __name__ == "__main__":
    app.run(debug=True)
