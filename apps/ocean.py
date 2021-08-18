import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from apps import misc, graphs, components

# ----------DATA------------------------

df = misc.carga_df('Ocean_q.csv')
data = df.copy()

# --------- COMPONENTS -----------------

datepicker = components.create_datepicker(df.Time.min(), df.Time.max())
time_options = components.create_time_options(['Quincenal', 'Mensual'])
mini = int(df.Depth.min())-1
maxi = int(df.Depth.max())
range_slider = components.create_range_slider(df.Depth, 'depth_slider')
graph = components.create_graph()
tabla = components.create_table(df)
dl_options = components.create_options_downloads()
dl_section = components.create_download_section(dl_options, 'ocean')

layout = html.Div(
    id='App_ocean',
    style={
        'box-sizing': 'border-box',
        'height': 'calc(100vh - 20px)',
        'display': 'flex',
        'flex-direction': 'column',
    },
    children=[
        html.Div(
            id='Main_ocean', children=[],
            style={
                'box-sizing': 'border-box',
                'display': 'flex',
                'flex-direction': 'column',
                'flex-shrink': '1',
                'flex-basis': '100%',
                'margin-right': '10px',
                'margin-top': '10px',
                'margin-bottom': '4px',
            },
        ),
        html.Div(
            id='opciones_ocean',
            style={
                'box-sizing': 'border-box',
                'display': 'flex',
                'justify-content': 'space-evenly',
                'align-items': 'center',
                'flex-wrap': 'wrap',
                'padding': '2px',
                'border': '1px solid black',
                'background': 'rgb(243,146,56)',
            },
            children=[
                html.Div(
                    style={
                        'display': 'inline-flex',
                        'align-items': 'center',
                    },
                    children=[
                        html.P('Rango De Fechas:    ', style={
                            'margin-bottom': '0.1rem',
                            'font-weight': 'bold', }),
                        datepicker,
                    ]
                ),
                html.Div(
                    style={
                        'display': 'inline-flex',
                        'align-items': 'center',
                    },
                    children=[
                        html.P('Agrupación temporal:', style={
                            'margin-bottom': '0.1rem',
                            'font-weight': 'bold', }),
                        time_options,
                    ]
                ),
                html.Div(
                    style={
                        'display': 'inline-flex',
                        'align-items': 'center',
                    },
                    children=[
                        html.P('Profundidad:', style={
                            'margin-bottom': '0.1rem',
                            'font-weight': 'bold', }),
                        range_slider,
                    ]
                ),

            ]
        ),
    ]
)

# --------------CALLBACKS---------------------


@app.callback(
    Output("Main_ocean", "children"),
    [Input("tipo", "value"),
     Input("Date_Picker", "start_date"),
     Input("Date_Picker", "end_date"),
     Input("depth_slider", "value"),
     Input('url', 'pathname')]
)
def update_graph(tipo, start_date, end_date, slider_values, pathname):

    global data
    pathname = pathname.strip().replace('/ocean/', '').lower()
    section = 'Ocean'

    # --------Date Filter/Group---------

    mask = misc.date_filter(df, start_date, end_date)
    data = misc.data_tipo(df, tipo, mask)

    # ------- FIGURE/TABLE

    if pathname == 'table':
        cols = ["SST", "SS", "Depth"]
        (styles, legend) = misc.discrete_background_color_bins(data[cols])  # Table Style
        tabla.style_data_conditional = styles
        tabla.columns = [{"name": misc.get_col_title(i), "id": i} for i in data.columns]
        tabla.data = data.round(2).to_dict('records')
        return [tabla, dl_section]

    else:
        try:
            fig, data = graphs.figure(data, section, pathname, tipo)
            graph.figure = fig
            return [graph]

        except:
            return html.Div("Error 404")


@app.callback(
    Output("download_ocean", "data"),
    Input("boton_descarga", "n_clicks"),
    State("formato_descarga", "value"),
    prevent_initial_call=True,
)
def descarga(n_clicks, formato_descarga):  # Download trigger
    file_name = 'ENOS_Ocean'
    if n_clicks and formato_descarga == 'excel':
        return dcc.send_data_frame(data.to_excel, file_name+'.xlsx', index=False, sheet_name=file_name)
    elif n_clicks and formato_descarga == 'csv':
        return dcc.send_data_frame(data.to_csv, file_name+'.csv', index=False)
    elif n_clicks and formato_descarga == 'json':
        return dcc.send_data_frame(data.to_json, file_name+'.json')