"""Módulo que se encarga de todas las funciones complementarias de la aplicación. Incluyen entre otras: conexiones a
bases de datos, carga y adecuación de información, manejos de estilos, entre otros."""

import dash_html_components as html
import colorlover
import pathlib
import pandas as pd
import pyodbc
import settings  # IMPORTANTE: Archivo local que contiene usuarios y contraseñas de la base de datos.
from numpy import nan, rad2deg
from threading import Thread
import functools


# -------- TIMEOUT FUNCTION ----------------
def timeout(seconds_before_timeout):
    """
    Esta función construye un decorador (@timeout) para generar un timeout. Es decir, permite acabar un proceso cuando
    este exceda la cantidad de tiempo que se le indica por parámetro. Esta función fue adaptada de la función encontrada
    en: https://stackoverflow.com/a/48980413/16825309
    """
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s]timeout [%s seconds] exceeded!' %
                             (func.__name__, seconds_before_timeout))]

            def new_func():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=new_func)
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


path = pathlib.Path(__file__).parent  # dirección de la aplicación.
data_path = path.joinpath("../datasets").resolve()  # dirección de los sets de datos.
dict_cols = {  # Diccionario con los nombres largos de las variables de la aplicación.
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


# ---------- MANEJO DE DATOS -----------------------

def path_extract(pathname):
    """Extrae la sección y la variable solicitada en la URL a partir del pathname."""
    pathname = list(filter(None, pathname.strip().lower().split('/')))  # Separa el pathname en una lista según los "/"
    section = ''
    variable = ''
    if len(pathname) > 0:
        section = pathname[0]
    if len(pathname) > 1:
        variable = pathname[1]

    return section, variable


def get_col_title(variable):
    """Retorna el título completo de la variable de acuerdo a su variable (Wvel, Wdir, SS, SST, etc)"""
    return dict_cols[variable]


def column_is_valid(section, variable):
    """Indica si la variable y sección solicitadas en la URL son válidas"""
    valid_colums = []
    if section == 'meteo' or section == 'meteo_fcst':
        valid_colums = ["Temp", 'Prcp', 'Wvel', 'Wdir']
    elif section == 'ocean' or section == 'ocean_fcst':
        valid_colums = ['SST', 'SS', 'SSH']
    elif section == 'estacion5':
        valid_colums = ['SST', 'SS', 'SSTa', 'SSa']

    if variable in valid_colums:
        return True
    else:
        return False


def df_from_local(file_name):
    """
    Lee la información del archivo de respaldo local solicitada y lo devuelve como un DataFrame

    :arg file_name: String. Archivos válidos: TUMACO_METEO_H, TUMACO_METEO_FCST_H, TUMACO_OCEAN_D, TUMACO_OCEAN_FCST_D,
                                              ESTACION5_OCEAN_Q + .csv
    """
    dataframe = pd.read_csv(data_path.joinpath(file_name))
    return dataframe


@timeout(0.5)
def df_from_db(table):
    """
    Intenta leer la información solicitada en la base de datos con un tiempo límite indicado por el decorador @timeout.

    :arg table: Str Tablas válidas: TUMACO_METEO_H, TUMACO_METEO_FCST_H, TUMACO_OCEAN_D, TUMACO_OCEAN_FCST_D,
                                    ESTACION5_OCEAN_Q
    :raises Error: Relanza el mismo error encontrado
    :return DataFrame con la tabla solicitada.
    """

    try:

        server = "BTASQLCLUSIG\\SIGDIMAR"  # Tener cuidado con el "\"
        database = 'SIGDIMAR'

        # Datos provenientes de un archivo local

        username = settings.username
        password = settings.password

        cnxn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=' + server +
            ';DATABASE=' + database +
            ';UID=' + username +
            ';PWD=' + password
        )

        dataframe = pd.read_sql_query('SELECT * FROM [Esquema_Vienos].[' + table + ']', cnxn)
        dataframe.drop(['OBJECTID', 'created_user', 'created_date', 'last_edited_user', 'last_edited_date'],
                       axis=1, inplace=True, errors='ignore')
        return dataframe

    except:
        raise


def get_data(table, modo='pruebas'):
    """
    Función principal de recolección de datos. Esta intenta recolectar la tabla solicitada de la base de datos.
    En caso de no poder obtener la conexión a base de datos indicada, intentará leer la tabla solicitada de los archivos
    locales que se pueden guardar como backup en la carpeta /datasets.
    Además, adecua algunas filas especiales, en caso de que existan, a las necesidades puntuales del programa.

    :param table: Str. Tabla Solicitada válidas: TUMACO_METEO_H, TUMACO_METEO_FCST_H, TUMACO_OCEAN_D,
                                                 TUMACO_OCEAN_FCST_D, ESTACION5_OCEAN_Q.

    :param modo: Str. Indica el modo en el que funciona el método. Los modos válidos son:
                    - pruebas: (Opción por defecto) imprime la talba y la fuente de donde fue leída.
                    - sobre_escritura: imprime la talba y la fuente de donde fue leída. Si se leyó de base de datos
                    sobreescribe el archivo de respaldo local por la nueva versión.
                    - producción: No imprime información de la fuente de datos. Si se leyó de base de datos sobreescribe
                     el archivo de respaldo local por la nueva versión

    :return: DataFrame con la información solicitada y adecuada.
    """

    dataframe = pd.DataFrame()  # Dataframe en blanco para evitar errores.

    try:  # Intenta obtener los datos solicitados desde la base de datos.

        dataframe = df_from_db(table)

        if modo == 'pruebas':
            print(table, ': Online')
        elif modo == "sobre_escritura":
            print(table, ': Online')
            dataframe.to_csv(data_path.joinpath(table + '.csv'), index=False)
        elif modo == "producción":
            dataframe.to_csv(data_path.joinpath(table + '.csv'), index=False)

    except:  # No pudo conectarse a la base de datos en el tiempo indicado.

        try:  # Intenta obtener los datos desde los archivos de respaldo locales.

            dataframe = df_from_local(table + '.csv')

            if modo == 'pruebas' or modo == "sobre_escritura":
                print(table, ': Local')

        except:

            raise ValueError("No data source found")

    dataframe.replace(-99999, nan, inplace=True)  # Cambia todos los valores anómalos a NaN.

    # -------- Adecuaciones de los datos ----------------

    if 'Wdir' in dataframe.columns:
        dataframe['Wdir'] = rad2deg(dataframe.Wdir) % 360  # De radiantes a grados positivos estándares [0-360°)

    if 'Prcp' in dataframe.columns:
        dataframe['Prcp'] = dataframe.Prcp * 1000  # Cambio de unidades.

    if 'Time' in dataframe.columns:
        dataframe['Time'] = pd.to_datetime(dataframe['Time'])  # Convierte de texto a formato tiempo.

    if 'SSH' in dataframe.columns:
        dataframe['SSH'] = dataframe.SSH * 100  # Cambio de unidades.

    # --------- Organización de los datos ----------------

    if 'Depth' in dataframe.columns:  # Si el dataframe tiene profundidad lo organiza por tiempo y profundidad.
        dataframe['Depth'] = dataframe.Depth.astype(int)
        dataframe.sort_values(["Time", "Depth"], inplace=True)

    else:  # De resto lo organiza sólo por tiempo
        dataframe.sort_values("Time", inplace=True)

    return dataframe

# --------------- Filtros De Datos -----------------------


def data_filter(df_column, start, end):
    """Crea una máscara con la fila del DataFrame y sus límites de inicio y fin para ser usado en un filtro."""
    mask = df_column.notnull()

    if start and end:
        mask = (df_column >= start) & (df_column < end)
    elif start:
        mask = df_column >= start
    elif end:
        mask = df_column < end

    return mask


def data_filter_depth(df_column, depth):
    """Crea una máscara con la fila del DataFrame y el número (profundidad) para ser usado en un filtro."""
    mask = df_column.notnull()

    if depth:
        mask = df_column == depth

    return mask


def data_tipo(df, tipo, mask):
    """
    Método de filtrado y agrupación de los datos según lo requerido.

    :param df: DataFrame con la información incial de la sección sin cambios.
    :param tipo: Str. Tipo de agrupación temporal solicitada. Estas pueden ser: Diaria, Quincenal, Semanal, Mensual
                 Trimestral o Anual.

    :param mask: Máscara de los datos. Utilizada para filtrar los datos de acuerdo a las demás imdicaciones.

    :return: DataFrame con la información solicitada filtrada y agrupada de acuerdo a las necesidades.
    """
    grouper = []  # Caracteristicas por las que se agrupan los datos.

    if "Depth" in df.columns:
        grouper.append("Depth")

    # ------------------ Agrupaciones Temporales --------------------

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

    else:  # Filtra sin agrupación temporal
        df2 = df[mask].round(2)

    # --------- Organización de los datos ----------------

    if 'Depth' in df.columns:  # Si el dataframe tiene profundidad lo organiza por tiempo y profundidad.
        df2.sort_values(["Time", "Depth"], inplace=True)

    else:  # De resto lo organiza sólo por tiempo
        df2.sort_values("Time", inplace=True) # Messy lines fix

    return df2

# --------------- Funciones Estéticas -----------------------


def color_pallete(n_bins=5):
    """Devuelve una lista de colores de tamaño indicado (5 por defecto) asociada a la escala Spectral."""
    colores = colorlover.scales[str(n_bins)]['div']['Spectral']  # paleta
    colores = colores[::-1]
    return colores


def discrete_background_color_bins(df, n_bins=5):
    """
    Función encargada de generar los estilos y leyendas de las tablas que requieran escalas de color.

    :param df: DataFrame sólamente con las columnas numéricas que requieran tener una escala de color.

    :param n_bins: Int. 0>n<17 .Cantidad de grupos o saltos de colores que se aplicarán a las columnas.

    :return: Una instrucción para que las tablas incorporen las escalas de color en las columnas indicadas.
    """
    colores = color_pallete(n_bins)  # Genera la lista de colores a usar.
    bounds = [round(i * (1.0 / n_bins), 3) for i in range(n_bins + 1)]  # Lista de posiciones
    styles = []
    legend = []

    for column in df.columns:
        df = df.sort_values(column)
        df_max = df[column].max()
        df_min = df[column].min()

        if column == 'Wvel':  # Caso especial de la velocidad del viento que se tomará de 5+ el último grupo
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
