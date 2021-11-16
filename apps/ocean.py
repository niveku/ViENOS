"""Módulo que se encarga del funcionamiento y presentación de la página de Oceanografía (/ocean)."""

import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from apps import misc, graphs, components

# ----------DATA------------------------

df = misc.get_data('TUMACO_OCEAN_D')  # Carga los datos

# --------- COMPONENTS -----------------

datepicker = components.create_datepicker(df.Time.min(), df.Time.max())
time_options = components.create_time_options(['Diaria', 'Semanal', 'Mensual'])
graph = components.create_graph()
tabla = components.create_table(df)
dl_options = components.create_options_downloads()
dl_section = components.create_download_section(dl_options)

# --------- LAYOUT HTML --------------------

layout = html.Div(
    id='App_ocean',
    className='App_container',
    children=[
        html.Div(
            id='Main_ocean',
            className='Main_container',
            children=[],
        ),
        html.Div(
            id='opciones_ocean',
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
    Output("Main_ocean", "children"),  # Actualiza este componente HTML
    [Input("tipo", "value"),  # Lee y reacciona a los cambios en estos inputs.
     Input("Date_Picker", "start_date"),
     Input("Date_Picker", "end_date"),
     State('url', 'pathname')]  # Lee el estado de la URL
)
def update_graph(tipo, start_date, end_date, pathname):
    """
    Se encarga de la actulización de los contenidos de la sección de oceanografía.
    Para ello lee y filtra la información de acuerdo los inputs de la página. Se activa automáticamente con cambios
    realizados en los inputs.

    :param tipo: Input. Agrupación temporal de los datos.
    :param start_date: Input. Filtro de fecha inicial de los datos.
    :param end_date: Input. Filtro de fecha final de los datos.
    :param pathname: State. dirección URL.
    :return: DIV HTML que actualiza la división de la página.
    """
    section, variable = misc.path_extract(pathname)

    # --------Date Filter/Group---------

    mask_date = misc.data_filter(df.Time, start_date, end_date)
    mask = mask_date  # & mask_depth
    data = misc.data_tipo(df, tipo, mask)

    # ------- FIGURE/TABLE

    if variable == 'table':  # Si se requiere crear una tabla.
        cols = ["SST", "SSH", "SS"]
        (styles, legend) = misc.discrete_background_color_bins(data[cols])  # Estilo de tabla
        tabla.style_data_conditional = styles
        tabla.columns = [{"name": misc.get_col_title(i), "id": i} for i in data.columns]
        tabla.data = data.round(2).to_dict('records')
        return [tabla, components.watermark]  # Actualiza valores de la tabla

    else:  # Si se requiere crear una gráfica.
        try:  # Intenta crear la gráfica haciendo validaciones de datos y url.
            fig, data = graphs.figure(data, variable, tipo)
            graph.figure = fig
            return [graph, components.watermark]  # Actualiza la gráfica de la página junto a la marca de agua.

        except ValueError: # Genera un tecto de error en caso de no ser capáz de generar la gráfica.
            return [html.Div("Error 404"), components.watermark]
