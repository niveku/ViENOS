import pathlib
import pandas as pd

import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from apps import misc, grafico_meteo


def date_filter(data_df, start_date, end_date):
    mask = data_df.Time.notnull()

    if start_date and end_date:
        mask = (data_df.Time >= start_date) & (data_df.Time < end_date)
    elif start_date:
        mask = data_df.Time >= start_date
    elif end_date:
        mask = data_df.Time < end_date

    return mask


# -------Date Grouper Selector------
def data_tipo(df, tipo, mask):
    if tipo == 'Diaria':
        df2 = df[mask].groupby(df.Time.dt.date).mean().round(2).reset_index()
        # data['Fecha'] = data.Time.dt.strftime('%d de %B del %Y')
    elif tipo == 'Semanal':
        df2 = df[mask].groupby(df.Time.dt.strftime('%Y:%W')).mean().round(2).reset_index()
        # data['Fecha'] = data.Time.dt.strftime('Semana %W del %Y')
    elif tipo == 'Mensual':
        df2 = df[mask].groupby(df.Time.dt.strftime('%B %Y')).mean().round(2).reset_index()
        # data['Fecha'] = data.Time.dt.strftime('%B del %Y')
    elif tipo == 'Anual':
        df2 = df[mask].groupby(df.Time.dt.strftime('%Y')).mean().round(2).reset_index()
        # data['Fecha'] = data.Time.dt.strftime('Año %Y')
    else:
        df2 = df[mask].round(2)

    df2.sort_values('Time', inplace=True)  # Messy lines fix

    return df2


# ----------DATA-----------------------
def carga_df():
    path = pathlib.Path(__file__).parent
    data_path = path.joinpath("../datasets").resolve()
    dataframe = pd.read_csv(data_path.joinpath('Meteo_h.csv'))
    dataframe['Time'] = pd.to_datetime(dataframe['Time'])
    dataframe.sort_values("Time", inplace=True)
    return dataframe


df = carga_df()
data = df.copy()

# --------- COMPONENTS -----------------

minf = pd.to_datetime(df.Time.min())
maxf = pd.to_datetime(df.Time.max())

datepicker = dcc.DatePickerRange(
    id='Date_Picker',
    minimum_nights=1,
    with_full_screen_portal=False,
    with_portal=True,
    number_of_months_shown=2,
    clearable=True,
    first_day_of_week=3,

    min_date_allowed=minf,
    max_date_allowed=maxf,
    initial_visible_month=minf,
    display_format='DD-MM-YYYY',
    start_date_placeholder_text='Inicio',
    end_date_placeholder_text='Fin',
    month_format='MM/YYYY',
    style={
        'opacity': '50',
        'background': 'rgb(243,146,56)'}
)

time_options = dcc.RadioItems(
    id="tipo",
    persistence_type='session',
    options=[
        {'label': 'Horaria', 'value': 'Horaria'},
        {'label': 'Diaria', 'value': 'Diaria'},
        {'label': 'Semanal', 'value': 'Semanal'},
        {'label': 'Mensual', 'value': 'Mensual'},
        # {'label': 'Anual', 'value': 'Anual','disabled': True}
    ],
    value='Horaria',
    labelStyle={
        'display': 'inline-block',
        # 'text-align': 'justify'
    },
)

tabla = dash_table.DataTable(id='table',
                             style_cell={
                                 'whiteSpace': 'normal',
                                 'height': 'auto',
                                 'width': 'auto',
                                 'textAlign': 'center',
                             },
                             style_header={
                                 'fontWeight': 'bold',
                                 'color': 'white',
                                 'backgroundColor': 'rgb(100, 100, 100)',
                             },
                             style_table={
                                 'display': 'flex',
                                 'height': '88vh',
                                 'width': '95%',
                                 'marginLeft': 'auto',
                                 'marginRight': 'auto',
                                 # 'marginTop': '5px',
                                 'overflowY': 'hidden',
                                 'overflowX': 'hidden',
                             },
                             columns=[{"name": i, "id": i} for i in df.columns],
                             data=df.round(2).to_dict('records'),
                             fixed_rows={'headers': True},
                             virtualization=True,
                             page_action='native',
                             # page_size=12,
                             sort_action="native",
                             )

graph = dcc.Graph(
    id="time-series-chart",
    config={
        'locale': 'es_ES.utf8',
        'responsive': True,
        'displayModeBar': False,
    },
    style={
        'min-height': '200px',
        'height': '100%',
        'width': '100%',
    },
)

opciones_descarga = dcc.Dropdown(
    id="formato_descarga",
    options=[
        {'label': 'Excel(.xlsx)', 'value': 'excel'},
        {'label': 'Comma Separated Values(.csv)', 'value': 'csv'},
        {'label': 'JSON (.json)', 'value': 'json'},
    ],
    style={
        'width': '350px',
    },
    value='excel',
    placeholder="Seleciona un formato:",
    clearable=False,
    searchable=False
)

bt_descarga = html.Div(
    id='Div_Descarga',
    style={
        'box-sizing': 'border-box',
        'display': 'flex',
        'justify-content': 'center',
        'height': 'auto',
        'marginTop': '40px',
        'marginLeft': 'auto',
        'marginRight': 'auto',
    },
    children=[
        opciones_descarga,
        html.Button("Descargar", id="boton_descarga"),
        dcc.Download(id="descarga")
    ]
)

# --------- LAYOUT -----------------

layout = html.Div(
    id='App_Meteo',
    style={
        'box-sizing': 'border-box',
        # 'display': 'flex',
        # 'flex-direction': 'column',
        'max-height': '100vh',
        'min-height': '0',
        'height': '100%',
        'width': '100%',
        'border': '1px solid red',
    },
    children=[

        html.Div(id='Contenedor_Principal', children=[],
                 style={
                     'display': 'flex',
                     'flex-shrink': '1',
                     'flex-basis': '100%',
                 },
                 ),
        html.Div(
            id='opciones_meteo',
            style={
                'box-sizing': 'border-box',
                'display': 'flex',
                'justify-content': 'space-evenly',
                'align-items': 'center',
                'flex-wrap': 'wrap',
                'height': 'auto',
                'min-height': '0',
                'padding': '2px',
                'border': '1px solid black',
                'background': 'rgb(243,146,56)',
            },
            children=[
                html.P('Rango De Fechas:', style={
                    'margin-bottom': '0.1rem',
                    'font-weight': 'bold', }),
                datepicker,
                html.P('Agrupación temporal:', style={
                    'margin-bottom': '0.1rem',
                    'font-weight': 'bold', }),
                time_options,
            ]),
    ])


# --------------CALLBACKS---------------------

@app.callback(
    Output("Contenedor_Principal", "children"),
    [Input("tipo", "value"),
     Input("Date_Picker", "start_date"),
     Input("Date_Picker", "end_date"),
     Input('url', 'pathname')]
)
def update_graph(tipo, start_date, end_date, pathname):
    global data
    pathname = pathname.strip().replace('/meteo', '').lower()

    # --------Date Filter/Group---------

    mask = date_filter(df, start_date, end_date)
    data = data_tipo(df, tipo, mask)

    # ------- FIGURE/TABLE

    if pathname == '/table':
        cols = ['Temp', 'Prcp', 'Wvel']
        (styles, legend) = misc.discrete_background_color_bins(data[cols])  # Table Style
        tabla.style_data_conditional = styles
        tabla.data = data.round(2).to_dict('records')
        return [tabla, bt_descarga]

    else:

        fig, data = grafico_meteo.figure(data, pathname, tipo)
        graph.figure = fig
        return [graph]

    # ---------Updaters ---------------

    # return fig, data.round(2).to_dict('records'), styles


@app.callback(
    Output("descarga", "data"),
    Input("boton_descarga", "n_clicks"),
    State("formato_descarga", "value"),
    prevent_initial_call=True,
)
def descarga(n_clicks, formato_descarga):  # Download trigger
    if n_clicks and formato_descarga == 'excel':
        return dcc.send_data_frame(data.to_excel, "Info_ENOS.xlsx", index=False, sheet_name="Info_ENOS")
    elif n_clicks and formato_descarga == 'csv':
        return dcc.send_data_frame(data.to_csv, "Info_ENOS.csv", index=False)
    elif n_clicks and formato_descarga == 'json':
        return dcc.send_data_frame(data.to_json, "Info_ENOS.json")
