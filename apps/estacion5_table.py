"""Modulo que se encarga del funcionamiento y presentación de la página de tablas para "Estación 5" (/estacion5)."""

import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import misc, components

# ----------DATA------------------------

df = misc.get_data('ESTACION5_OCEAN_Q')

# --------- COMPONENTS -----------------

datepicker = components.create_datepicker(df.Time.min(), df.Time.max())
time_options = components.create_time_options(['Quincenal', 'Mensual', 'Trimestral'])
depth_inp = components.create_depth_input(df.Depth.min(), df.Depth.max())
tabla = components.create_table(df)

# --------- LAYOUT HTML --------------------

main_container = html.Div(id='Main_estacion5_table', className='Main_container', children=[])
layout = html.Div(
    id='App_estacion5',
    className='App_container',
    children=[
        main_container,
        html.Div(
            id='estacion5_table_options',
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
                html.Div(
                    className='SubOptions_container',
                    children=[
                        html.P('Profundidad: ', className='p_title'),
                        depth_inp,
                    ]
                ),
            ]
        ),
    ]
)


# --------------CALLBACKS---------------------


@app.callback(
    Output("Main_estacion5_table", "children"),  # Actualiza este componente HTML
    [Input("tipo", "value"),  # Lee y reacciona a los cambios en estos inputs.
     Input("Date_Picker", "start_date"),
     Input("Date_Picker", "end_date"),
     Input("input_depth", "value")]
)
def update_table(tipo, start_date, end_date, depth):
    """
    Se encarga de la actulización de los contenidos de la tabla de la sección de estación 5.
    Para ello lee y filtra la información de acuerdo los inputs de la página. Se activa automáticamente con cambios
    realizados en los inputs.
    :param tipo: Input. Agrupación temporal de los datos.
    :param start_date: Input. Filtro de fecha inicial de los datos.
    :param end_date: Input. Filtro de fecha final de los datos.
    :param depth: Input. Valor de la profundidad seleccionada.
    :return: DIV HTML que actualiza la tabla y división de la página.
    """
    # --------Date Filter/Group---------

    mask_date = misc.data_filter(df.Time, start_date, end_date)  # Máscara de fechas.
    mask_depth = misc.data_filter_depth(df.Depth, depth)  # Máscara de profundidad única.
    mask = mask_date & mask_depth  # Unión de las máscaras
    data = misc.data_tipo(df, tipo, mask)  # Aplicación de máscara para filtro de la información requerida.

    # ------------ TABLE ----------------

    cols = ["SST", "SSTa", "SS", "SSa"]  # Columnas con formatos de colores
    (styles, _) = misc.discrete_background_color_bins(data[cols])  # Estilos de las celdas
    tabla.style_data_conditional = styles
    tabla.columns = [{"name": misc.get_col_title(i), "id": i} for i in data.columns]
    tabla.data = data.round(2).to_dict('records')  # Actualizacion de tabla.
    return [tabla, components.watermark]
