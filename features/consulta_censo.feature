Feature: Consulta de datos del Censo de México
  Como analista de mercado
  Quiero consultar y filtrar datos del Censo de México
  Para diseñar estrategias de comercialización por estado y municipio

  Scenario: Consultar población total por estado
    Given que estoy en la interfaz de consulta del Censo
    And he seleccionado el estado "Puebla"
    When ejecuto la búsqueda de población
    Then debo ver la población total del estado "Puebla"
    And los datos mostrados deben corresponder al último Censo disponible


  Scenario: Filtrar población por municipio y rango de edad
    Given que estoy en la interfaz de consulta del Censo
    And he seleccionado el estado "Puebla"
    And he seleccionado el municipio "Puebla"
    And he definido el rango de edad de "18" a "35" años
    When ejecuto la búsqueda de población filtrada
    Then debo ver la población del municipio "Puebla" en el rango de edad de "18" a "35" años
    And los resultados deben presentarse en una tabla con columnas de edad y cantidad de personas


  Scenario: Visualizar resultados en un gráfico de barras
    Given que he realizado una consulta de población por estado
    When selecciono la opción de ver resultados en gráfico
    Then debo ver un gráfico de barras con la población por estado
    And cada barra debe estar etiquetada con el nombre del estado y su población
