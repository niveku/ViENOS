import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from apps import misc, graphs, components

# ----------DATA------------------------

df = misc.get_data('ESTACION5_OCEAN_Q')

# --------- COMPONENTS -----------------

datepicker = components.create_datepicker(df.Time.min(), df.Time.max())
time_options = components.create_time_options(['Quincenal', 'Mensual', 'Trimestral'])
range_slider = components.create_range_slider(df.Depth, 'depth_slider')
graph = components.create_graph()
tabla = components.create_table(df)
dl_options = components.create_options_downloads()
dl_section = components.create_download_section(dl_options)

layout = html.Div(
    id='App_estacion5',
    className='App_container',
    children=[
        html.Div(
            id='Main_estacion5',
            className='Main_container',
            children=[],
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
                        html.P('Agrupación temporal:', className='p_title'),
                        time_options,
                    ]
                ),
                html.Div(
                    className='SubOptions_container',
                    children=[
                        html.P('Profundidad:', className='p_title'),
                        range_slider,
                        html.Div(id='output-range-slider')
                    ]
                ),
                html.Div(
                    className='SubOptions_container',
                    children=[
                        html.P('Fuente de Datos:', className='p_title'),
                        components.cecoldo,
                    ]
                ),
            ]
        ),
    ]
)

# --------------CALLBACKS---------------------


@app.callback(
    Output("Main_estacion5", "children"),
    Output('output-range-slider', 'children'),
    [Input("tipo", "value"),
     Input("Date_Picker", "start_date"),
     Input("Date_Picker", "end_date"),
     Input("depth_slider", "value"),
     State('url', 'pathname')]
)
def update_graph(tipo, start_date, end_date, slider_values, pathname):

    section, variable = misc.path_extract(pathname)

    # --------Date Filter/Group---------

    mask_date = misc.data_filter(df.Time, start_date, end_date)
    mask_depth = misc.data_filter(df.Depth, slider_values[0], slider_values[1]+1)
    mask = mask_date & mask_depth
    data = misc.data_tipo(df, tipo, mask)

    # ------- FIGURE/TABLE

    if variable == 'table':
        cols = ["SST", "SS", "Depth"]
        (styles, legend) = misc.discrete_background_color_bins(data[cols])  # Table Style
        tabla.style_data_conditional = styles
        tabla.columns = [{"name": misc.get_col_title(i), "id": i} for i in data.columns]
        tabla.data = data.round(2).to_dict('records')
        return [tabla, components.watermark], f"{slider_values}m"  # , dl_section]

    else:
        try:
            fig, data = graphs.figure(data, section, variable, tipo)
            graph.figure = fig
            return [graph, components.watermark], f"{slider_values}m"

        except ValueError:
            return [html.Div("Error 404"), components.watermark], f"{slider_values}m"
