import dash_html_components as html
import colorlover
import pathlib
import pandas as pd
from numpy import nan
# import mysql.connector as connector

dict_cols = {
    'Time': 'Fecha/Hora',
    'Temp': 'Temperatura(C°)',
    'Prcp': 'Precipitación(mL)',
    'Wvel': 'Velocidad del viento(m/s)',
    'Wdir': 'Dirección del viento(°)',
    'SST': 'Temp. Superficial del Mar(C°)',
    'SS': 'Salinidad',
    'Depth': 'Profundidad(m)',
    'Long': 'Longitud',
    'Lat': 'Latitud',
}

# ----------DATA MANAGEMENT-------------------------------


def get_col_title(key):
    return dict_cols[key]


def column_is_valid(section, column):
    valid_colums = []
    if section == 'Meteo':
        valid_colums = ["Temp", 'Prcp', 'Wvel', 'Wdir']
    elif section == 'Ocean':
        valid_colums = ['SST', 'SS', 'Depth']

    if column in valid_colums:
        return True
    else:
        return False


def carga_df(file_name):
    path = pathlib.Path(__file__).parent
    data_path = path.joinpath("../datasets").resolve()
    dataframe = pd.read_csv(data_path.joinpath(file_name))
    dataframe['Time'] = pd.to_datetime(dataframe['Time'])
    dataframe.replace(-99999, nan, inplace=True)
    if 'Depth' in dataframe.columns:
        dataframe['Depth'] = dataframe.Depth.astype(int)
        dataframe.sort_values(["Time", "Depth"], inplace=True)
    else:
        dataframe.sort_values("Time", inplace=True)
    return dataframe


def date_filter(data_df, start_date, end_date):
    mask = data_df.Time.notnull()

    if start_date and end_date:
        mask = (data_df.Time >= start_date) & (data_df.Time < end_date)
    elif start_date:
        mask = data_df.Time >= start_date
    elif end_date:
        mask = data_df.Time < end_date

    return mask


def data_tipo(df, tipo, mask):
    if tipo == 'Diaria' or tipo == 'Quincenal':
        df2 = df[mask].groupby(df.Time.dt.date).mean().round(2).reset_index()
        # data['Fecha'] = data.Time.dt.strftime('%d de %B del %Y')
    elif tipo == 'Semanal':
        df2 = df[mask].groupby(df.Time.dt.strftime('%Y:%W')).mean().round(2).reset_index()
        # data['Fecha'] = data.Time.dt.strftime('Semana %W del %Y')
    # elif tipo == 'Quincenal':
    #     df2 = df[mask].groupby(df.Time.dt.strftime('%Y:%d')).mean().round(2).reset_index()
    #     # data['Fecha'] = data.Time.dt.strftime('Semana %W del %Y')
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


def color_pallete(n_bins=5):
    colores = colorlover.scales[str(n_bins)]['div']['Spectral']  # paleta
    colores = colores[::-1]
    return colores


def discrete_background_color_bins(df, n_bins=5):
    colores = color_pallete(n_bins)
    bounds = [round(i * (1.0 / n_bins), 3) for i in range(n_bins + 1)]  # Lista de posiciones
    styles = []
    legend = []

    for column in df.columns:
        df = df.sort_values(column)
        df_max = df[column].max()
        df_min = df[column].min()

        if column == 'Wvel':
            df_min = 0
            df_max = 5

        for i in range(1, len(bounds)):
            background_color = colores[i - 1]
            color = 'white' if i > len(bounds) / 2. else 'inherit'
            ranges = [((df_max - df_min) * i) + df_min for i in bounds]
            min_bound = ranges[i - 1]
            max_bound = ranges[i]

            styles.append({
                'if': {
                    'filter_query': (
                            '{{{column}}} >= {min_bound}' +
                            (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': background_color,
                'color': color
            })
        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': background_color,
                        'borderLeft': '1px rgb(50, 50, 50) solid',
                        'height': '10px'
                    }
                ),
                html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
            ])
        )

    return styles, html.Div(legend, style={'padding': '5px 0 5px 0'})

# def conexion():
#     conexion = None
#     try:
#         #SQL server
#         conexion = connector.connect(
#         host='BTASQLCLUSIG\SIGDIMAR',
#         user='Esquema_Vienos',
#         password='*VIENOSC2021*')
#         print('Conexión Exitosa')
#     except:
#         print ('Error')
#     return conexion
