"""Módulo que se encarga del funcionamiento y presentación de la página de "Estación 5" (/estacion5)."""

import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from apps import misc, graphs, components

# ----------DATA------------------------

df = misc.get_data('ESTACION5_OCEAN_Q')  # Carga los datos

# --------- COMPONENTS -----------------

datepicker = components.create_datepicker(df.Time.min(), df.Time.max())
time_options = components.create_time_options(['Quincenal', 'Mensual', 'Trimestral'])
range_slider = components.create_range_slider(df.Depth, 'depth_slider')
graph = components.create_graph()

# --------- LAYOUT HTML --------------------

main_container = html.Div(id='Main_estacion5', className='Main_container', children=[])
layout = html.Div(
    id='App_estacion5',
    className='App_container',
    children=[
        html.Div(
            id='container_estacion5',
            className='Slider_container',
            children=[
                html.P('Profundidad', className='p_title_vertical'),
                range_slider,
                main_container,
            ]
        ),
        html.Div(
            id='opciones_estacion5',
            className='Options_container',
            children=[
                html.Div(
                    className='SubOptions_container',
                    children=[
                        html.P('Periodo:    ', className='p_title'),
                        datepicker,
                    ]
                ),
                html.Div(
                    className='SubOptions_container',
                    children=[
                        html.P('Resolución temporal:', className='p_title'),
                        time_options,
                    ]
                ),
            ]
        ),
    ]
)

# --------------CALLBACKS---------------------


@app.callback(
    Output("Main_estacion5", "children"),  # Actualiza este componente HTML
    [Input("tipo", "value"),  # Lee y reacciona a los cambios en estos inputs.
     Input("Date_Picker", "start_date"),
     Input("Date_Picker", "end_date"),
     Input("depth_slider", "value"),
     State('url', 'pathname')]  # Lee el estado de la URL
)
def update_graph(tipo, start_date, end_date, depth, pathname):
    """
    Se encarga de la actulización de los contenidos de la sección de estación 5.
    Para ello lee y filtra la información de acuerdo los inputs de la página. Se activa automáticamente con cambios
    realizados en los inputs.

    :param tipo: Input. Agrupación temporal de los datos.
    :param start_date: Input. Filtro de fecha inicial de los datos.
    :param end_date: Input. Filtro de fecha final de los datos.
    :param depth: Input. Valor de la profundidad seleccionada.
    :param pathname: State. dirección URL.
    :return: DIV HTML que actualiza la división de la página.
    """

    section, variable = misc.path_extract(pathname)  # Extrae información de la URL para determinar la fuente de datos.

    # --------Date Filter/Group---------

    mask_date = misc.data_filter(df.Time, start_date, end_date)  # Máscara de fechas.
    mask_depth = misc.data_filter_depth(df.Depth, depth)  # Máscara de profundidad única.
    mask = mask_date & mask_depth  # Unión de las máscaras
    data = misc.data_tipo(df, tipo, mask)  # Aplicación de máscara para filtro de la información requerida.

    # ------- FIGURE/TABLE

    try:  # Intenta crear la gráfica haciendo validaciones de datos y url.
        fig, data = graphs.figure(data, section, variable, tipo)
        graph.figure = fig
        return [graph, components.watermark]  # Actualiza la gráfica de la página junto a la marca de agua.

    except ValueError:  # Genera un tecto de error en caso de no ser capáz de generar la gráfica.
        return [html.Div("Error 404"), components.watermark]
