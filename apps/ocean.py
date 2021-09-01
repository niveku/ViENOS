import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from apps import misc, graphs, components

# ----------DATA------------------------

df = misc.carga_df('Ocean_q.csv')

# --------- COMPONENTS -----------------

datepicker = components.create_datepicker(df.Time.min(), df.Time.max())
time_options = components.create_time_options(['Quincenal', 'Mensual', 'Trimestral'])
range_slider = components.create_range_slider(df.Depth, 'depth_slider')
graph = components.create_graph()
tabla = components.create_table(df)
dl_options = components.create_options_downloads()
dl_section = components.create_download_section(dl_options)

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
    Output("Main_ocean", "children"),
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


# @app.callback(
#     Output("download_ocean", "data"),
#     Input("boton_descarga", "n_clicks"),
#     State("formato_descarga", "value"),
#     prevent_initial_call=True,
# )
# def descarga(n_clicks, formato_descarga):  # Download trigger
#     file_name = 'ENOS_Ocean'
#     if n_clicks and formato_descarga == 'excel':
#         return dcc.send_data_frame(data.to_excel, file_name+'.xlsx', index=False, sheet_name=file_name)
#     elif n_clicks and formato_descarga == 'csv':
#         return dcc.send_data_frame(data.to_csv, file_name+'.csv', index=False)
#     elif n_clicks and formato_descarga == 'json':
#         return dcc.send_data_frame(data.to_json, file_name+'.json')
