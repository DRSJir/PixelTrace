from behave import given, when, then
from censo_servicio import (
    obtener_poblacion_por_estado,
    obtener_tabla_municipio_edad,
    construir_datos_grafico_por_estado,
)

# Datos simulados del Censo (prototipo)
CENSO_ESTADOS = {
    "Puebla": {
        "estado": "Puebla",
        "poblacion_total": 6583278,
        "anio_censo": 2020,
    }
}

@given('que estoy en la interfaz de consulta del Censo')
def step_impl_interfaz_censo(context):
    # Inicializamos variables de contexto
    context.estado = None
    context.municipio = None
    context.rango_edad = None
    context.resultados = None


"""
Steps para seleccionar estado, municipio y rango de edad
"""
@given('he seleccionado el estado "{estado}"')
def step_impl_seleccionar_estado(context, estado):
    context.estado = estado

@given('he seleccionado el municipio "{municipio}"')
def step_impl_seleccionar_municipio(context, municipio):
    context.municipio = municipio

@given('he definido el rango de edad de "{edad_min}" a "{edad_max}" años')
def step_impl_rango_edad(context, edad_min, edad_max):
    context.rango_edad = (int(edad_min), int(edad_max))


"""
Steps para las acciones (When)
"""
@when('ejecuto la búsqueda de población')
def step_impl_busqueda_poblacion(context):
    datos_estado = obtener_poblacion_por_estado(context.estado)
    assert datos_estado is not None, f"Estado {context.estado} no encontrado en los datos"
    context.resultados = datos_estado

@when('ejecuto la búsqueda de población filtrada')
def step_impl_busqueda_poblacion_filtrada(context):
    edad_min, edad_max = context.rango_edad
    context.resultados = obtener_tabla_municipio_edad(
        context.estado,
        context.municipio,
        edad_min,
        edad_max,
    )

@when('selecciono la opción de ver resultados en gráfico')
def step_impl_ver_resultados_grafico(context):
    context.grafico = construir_datos_grafico_por_estado(context.estado)
    assert context.grafico is not None, "No se pudieron construir los datos del gráfico"


"""
Verificaciones (Then / And)
"""
@then('debo ver la población total del estado "{estado}"')
def step_impl_ver_poblacion_estado(context, estado):
    assert context.resultados is not None, "No hay resultados en el contexto"
    assert context.resultados["estado"] == estado, "El estado en resultados no coincide"
    assert "poblacion_total" in context.resultados, "No se encontró la población total en los resultados"

@then('los datos mostrados deben corresponder al último Censo disponible')
def step_impl_validar_ultimo_censo(context):
    assert context.resultados is not None, "No hay resultados en el contexto"
    assert context.resultados.get("anio_censo") == 2020, "El año de censo no es el esperado (2020) en el prototipo"

@then('debo ver la población del municipio "{municipio}" en el rango de edad de "{edad_min}" a "{edad_max}" años')
def step_impl_ver_poblacion_municipio_rango(context, municipio, edad_min, edad_max):
    assert context.resultados is not None, "No hay resultados en el contexto"
    assert context.resultados["municipio"] == municipio, "El municipio no coincide"
    assert context.resultados["rango_edad"] == (int(edad_min), int(edad_max)), "El rango de edad no coincide"

@then('los resultados deben presentarse en una tabla con columnas de edad y cantidad de personas')
def step_impl_tabla_edad_cantidad(context):
    tabla = context.resultados.get("tabla")
    assert isinstance(tabla, list), "La tabla de resultados no es una lista"
    assert len(tabla) > 0, "La tabla de resultados está vacía"

    for fila in tabla:
        assert "edad" in fila, "Falta la columna edad en una fila"
        assert "personas" in fila, "Falta la columna personas en una fila"

@then('debo ver un gráfico de barras con la población por estado')
def step_impl_grafico_barras(context):
    assert hasattr(context, "grafico"), "No se encontró información de gráfico en el contexto"
    assert context.grafico.get("tipo") == "barras", "El tipo de gráfico no es de barras"
    assert len(context.grafico.get("datos", [])) > 0, "El gráfico no tiene datos"


@given('que he realizado una consulta de población por estado')
def step_impl_consulta_realizada(context):
    if getattr(context, "estado", None) is None:
        context.estado = "Puebla"
    context.resultados = obtener_poblacion_por_estado(context.estado)
    assert context.resultados is not None, "No se encontraron datos simulados para el estado"

@then('cada barra debe estar etiquetada con el nombre del estado y su población')
def step_impl_etiquetas_grafico(context):
    for barra in context.grafico.get("datos", []):
        assert "estado" in barra, "Una barra no tiene etiqueta de estado"
        assert "poblacion" in barra, "Una barra no tiene valor de población"
