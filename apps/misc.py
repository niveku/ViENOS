import dash_html_components as html
import colorlover
import pathlib
import pandas as pd
from numpy import nan, rad2deg
from threading import Thread
import functools


# -------- TIMEOUT FUNCTION ----------------
def timeout(seconds_before_timeout):
    """
    https://stackoverflow.com/a/48980413/16825309
    """
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s]timeout [%s seconds] exceeded!' %
                             (func.__name__, seconds_before_timeout))]

            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(seconds_before_timeout)
            except Exception as e:
                print('error starting thread')
                raise e
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco


path = pathlib.Path(__file__).parent
data_path = path.joinpath("../datasets").resolve()
dict_cols = {
    'Time': 'Fecha/Hora',
    'Temp': 'Temperatura (°C)',
    'Prcp': 'Precipitación (mL)',
    'Wvel': 'Velocidad del viento (m/s)',
    'Wdir': 'Dirección del viento (°)',
    'SST': 'Temp. del Mar (°C)',
    'SSTa': 'Anomalía Temp. del Mar (°C)',
    'SSH': 'Nivel del Mar (cm)',
    'SS': 'Salinidad (PSU)',
    'SSa': 'Anomalía Salinidad (g/L)',
    'Depth': 'Profundidad (m)',
    'Long': 'Longitud',
    'Lat': 'Latitud',
}


# ----------DATA MANAGEMENT-------------------------------
def path_extract(pathname):
    pathname = list(filter(None, pathname.strip().lower().split('/')))
    section = ''
    variable = ''
    if len(pathname) > 0:
        section = pathname[0]
    if len(pathname) > 1:
        variable = pathname[1]

    return section, variable


def get_col_title(key):

    return dict_cols[key]


def column_is_valid(section, column):
    valid_colums = []
    if section == 'meteo' or section == 'meteo_fcst':
        valid_colums = ["Temp", 'Prcp', 'Wvel', 'Wdir']
    elif section == 'ocean' or section == 'ocean_fcst':
        valid_colums = ['SST', 'SS', 'SSH']
    elif section == 'estacion5':
        valid_colums = ['SST', 'SS', 'SSTa', 'SSa']

    if column in valid_colums:
        return True
    else:
        return False


def df_from_local(file_name):

    dataframe = pd.read_csv(data_path.joinpath(file_name))
    return dataframe


@timeout(0.5)
def df_from_db(table):
    """
    :arg table: Valid inputs TUMACO_METEO_H, TUMACO_METEO_FCST_H,
    TUMACO_OCEAN_D, TUMACO_OCEAN_FCST_D, ESTACION5_OCEAN_Q
    """

    try:
        import settings
        import pyodbcas #FORCED BUG

        server = "BTASQLCLUSIG\SIGDIMAR"
        database = 'SIGDIMAR'
        username = settings.username
        password = settings.password

        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' +
                              database + ';UID=' + username + ';PWD=' + password)

        dataframe = pd.read_sql_query('SELECT * FROM [Esquema_Vienos].[' + table + ']', cnxn)  # .round(2)
        dataframe.drop(['OBJECTID', 'created_user', 'created_date', 'last_edited_user', 'last_edited_date'],
                       axis=1, inplace=True)
        return dataframe

    except:
        raise


def get_data(table):

    dataframe = pd.DataFrame()
    try:
        dataframe = df_from_db(table)
        # dataframe.to_csv(data_path.joinpath(table + '.csv'), index=False)
        print(table, ': Online')

    except:

        try:
            dataframe = df_from_local(table + '.csv')
            print(table, ': Local')
        except:
            raise ValueError("No data source found")

    dataframe.replace(-99999, nan, inplace=True)

    if 'Wdir' in dataframe.columns:
        dataframe['Wdir'] = rad2deg(dataframe.Wdir) % 360

    if 'Prcp' in dataframe.columns:
        dataframe['Prcp'] = dataframe.Prcp * 1000

    if 'Time' in dataframe.columns:
        dataframe['Time'] = pd.to_datetime(dataframe['Time'])

    if 'SSH' in dataframe.columns:
        dataframe['SSH'] = dataframe.SSH * 100

    if 'Depth' in dataframe.columns:
        dataframe['Depth'] = dataframe.Depth.astype(int)
        dataframe.sort_values(["Time", "Depth"], inplace=True)
    else:
        dataframe.sort_values("Time", inplace=True)

    return dataframe


def data_filter(df_column, start, end):
    mask = df_column.notnull()

    if start and end:
        mask = (df_column >= start) & (df_column < end)
    elif start:
        mask = df_column >= start
    elif end:
        mask = df_column < end

    return mask


def data_filter_depth(df_column, start, end):
    mask = df_column.notnull()

    if start and end:
        mask = (df_column >= start) & (df_column <= end)
    elif start:
        mask = df_column >= start
    elif end:
        mask = df_column <= end

    return mask


def data_tipo(df, tipo, mask):

    grouper = []
    if "Depth" in df.columns:
        grouper.append("Depth")

    if tipo == 'Diaria' or tipo == 'Quincenal':
        grouper.insert(0, df.Time.dt.date)
        df2 = df[mask].groupby(grouper).mean().round(2).reset_index()
        # data['Fecha'] = data.Time.dt.strftime('%d de %B del %Y')
    elif tipo == 'Semanal':
        grouper.insert(0, df.Time.dt.strftime('%Y:S%w'))
        df2 = df[mask].groupby(grouper).mean().round(2).reset_index()
    elif tipo == 'Mensual':
        grouper.insert(0, df.Time.dt.strftime('%Y/%m'))
        df2 = df[mask].groupby(grouper).mean().round(2).reset_index()
    elif tipo == 'Trimestral':
        grouper.insert(0, df.Time.dt.to_period('Q'))
        df2 = df[mask].groupby(grouper).mean().round(2).reset_index()
        df2.Time = df2.Time.astype(str).str.replace('Q', ':T')
    elif tipo == 'Anual':
        grouper.insert(df.Time.dt.strftime('%Y'))
        df2 = df[mask].groupby(grouper).mean().round(2).reset_index()
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
