import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from apps import misc, graphs, components

# ----------DATA------------------------

df = misc.get_data('TUMACO_OCEAN_FCST_D')

# --------- COMPONENTS -----------------

datepicker = components.create_datepicker(df.Time.min(), df.Time.max())
time_options = components.create_time_options(['Diaria', 'Semanal', 'Mensual'])
graph = components.create_graph()
tabla = components.create_table(df)
dl_options = components.create_options_downloads()
dl_section = components.create_download_section(dl_options)

layout = html.Div(
    id='App_ocean_fcst',
    className='App_container',
    children=[
        html.Div(
            id='Main_ocean_fcst',
            className='Main_container',
            children=[],
        ),
        html.Div(
            id='opciones_ocean_fcst',
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
    Output("Main_ocean_fcst", "children"),
    [Input("tipo", "value"),
     Input("Date_Picker", "start_date"),
     Input("Date_Picker", "end_date"),
     State('url', 'pathname')]
)
def update_graph(tipo, start_date, end_date, pathname):

    section, variable = misc.path_extract(pathname)

    # --------Date Filter/Group---------

    mask_date = misc.data_filter(df.Time, start_date, end_date)
    mask = mask_date  # & mask_depth
    data = misc.data_tipo(df, tipo, mask)

    # ------- FIGURE/TABLE

    if variable == 'table':
        cols = ["SST", "SSH", "SS"]
        (styles, legend) = misc.discrete_background_color_bins(data[cols])  # Table Style
        tabla.style_data_conditional = styles
        tabla.columns = [{"name": misc.get_col_title(i), "id": i} for i in data.columns]
        tabla.data = data.round(2).to_dict('records')
        return [tabla, components.watermark]

    else:
        try:
            fig, data = graphs.figure(data, variable, tipo)
            graph.figure = fig
            return [graph, components.watermark]

        except ValueError:
            return [html.Div("Error 404"), components.watermark]
