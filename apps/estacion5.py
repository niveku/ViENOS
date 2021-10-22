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
                #html.Div(id='output-range-slider'),
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
    Output("Main_estacion5", "children"),
    # Output('output-range-slider', 'children'),
    [Input("tipo", "value"),
     Input("Date_Picker", "start_date"),
     Input("Date_Picker", "end_date"),
     Input("depth_slider", "value"),
     State('url', 'pathname')]
)
def update_graph(tipo, start_date, end_date, slider_value, pathname):

    section, variable = misc.path_extract(pathname)

    # --------Date Filter/Group---------

    mask_date = misc.data_filter(df.Time, start_date, end_date)
    mask_depth = misc.data_filter(df.Depth, slider_value, slider_value+1)
    mask = mask_date & mask_depth
    data = misc.data_tipo(df, tipo, mask)

    # ------- FIGURE/TABLE

    try:
        fig, data = graphs.figure(data, section, variable, tipo)
        graph.figure = fig
        return [graph, components.watermark]  # , f"{slider_values}m"

    except ValueError:
        return [html.Div("Error 404"), components.watermark]  # , f"{slider_values}m"
