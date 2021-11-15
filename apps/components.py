"""
Este módulo se encarga de generar todos los componentes funcionales interactivos de los dashboards.
Es decir, los inputs, sliders, gráficas y tablas.
"""
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from app import app  # Conexión a la aplicación principal
from apps import misc
from pandas import to_datetime

# Marca de agua de Dimar. Se centra con el CSS
watermark = html.Img(
    src=app.get_asset_url("watermark.png"),
    className='Watermark',
    alt='watermark',
)

# Logo de CECOLDO (En desuso)
cecoldo = html.A(
    className='Cecoldo_A',
    href='https://cecoldo.dimar.mil.co/web/',
    target="_blank",
    children=[
        html.Img(
            id='Cecoldo_logo',
            src=app.get_asset_url("cecoldo_logo.png"),
            alt='cecoldo',
        )
    ]
)


def create_datepicker(min_date, max_date):
    """
    Crea un datepicker limitado por una fecha máxima y mínima. Posee distintos formatos

    :param min_date: fecha mínima del input.
    :param max_date: fecha máxima del input
    :return: un componente HTML funcional de inputs de rangos de fechas.
    """

    minf = to_datetime(min_date)
    maxf = to_datetime(max_date)

    datepicker = dcc.DatePickerRange(
        id='Date_Picker',
        minimum_nights=1,  # Distancia mínima entre días
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
    return datepicker


def create_time_options(lst_options):
    """
    Crea una lista de inputs tipo Radio a partir de una lista de opciones temporales válidas.

    @:param lst_options: Una lista con las opciones válidas que incluyen: Diaria, Semanal, Quincenal, Mensual y Anual.
    """

    time_options = dcc.RadioItems(
        id="tipo",
        persistence_type='session',
        options=[{'label': op, 'value': op} for op in lst_options],
        value=lst_options[0], #Selecciona por defecto el primer valor de la lista.
        labelStyle={
            'box-sizing': 'border-box',
            'display': 'inline-block',
            'padding': '5px',
            'text-align': 'justify'
        },
    )
    return time_options


def create_range_slider(column, item_id):
    """
    Crea un slider-input de un sólo valor a partir de una columna o lista de datos.

    :param column: Columna de DF o lista con los valores a partir de los cuales se extrae los min/max del slider.
    :param item_id: identificador HTML con el cual se selecciona el input creado en los call-backs.
    :return: componente slider-input HTML
    """
    mini = max(int(column.min()) - 1, 0)
    maxi = min(int(column.max()), 80)
    range_slider = dcc.Slider(
        id=item_id,
        min=mini,
        max=maxi,
        step=10,  # Pasos entre los números del slider.
        marks={i: {'label': "{}m".format(i)}  # , 'style': {'transform': 'rotate(180deg)'}}
               for i in range(mini, maxi + 1, 10)},
        # allowCross=False,
        # pushable=5,
        value=mini,  # [mini, maxi],
        vertical=True,
        updatemode='drag',
    )
    return range_slider


def create_min_max_input(min_int, max_int):
    """
    Crea un conjunto de dos inputs numéricos para valores mínimos y máximos.

    :param min_int: Número entero mínimo recibido en los inputs.
    :param max_int: Número entero máximo recibido en los inputs.
    :return: min_inp, max_inp. Dos inputs numéricos HTML.
    """

    min_inp = dcc.Input(
        id="input_min_depth", type="number", placeholder="Min",
        min=min_int, max=max_int-1, step=1,
        style={
            'margin': '0px 10px 0px 5px',
            'border-radius': '4px',
            'border': '1px solid black',
            },
    )
    max_inp = dcc.Input(
        id="input_max_depth", type="number", placeholder="Max",
        min=min_int+1, max=max_int, step=1,
        style={
            'border-radius': '4px',
            'border': '1px solid black',
            },
    )
    return min_inp, max_inp


def create_depth_input(min_int, max_int):
    """
    Crea un componente HTML input de tipo númerico adecuado a cambios de profundidad.

    :param min_int: Profundidad mínima recibida
    :param max_int: Profundidad máxima recibida
    :return: Componente HTML de tipo input numérico límitado con los datos de profundidad.
    """

    inp = dcc.Input(
        id="input_depth", type="number", placeholder="----",
        min=min_int, max=max_int, step=1,
        style={
            'margin': '0px 10px 0px 5px',
            'border-radius': '4px',
            'border': '1px solid black',
            },
    )

    return inp


def create_graph():
    """
    Inicializa y devuelve el componente de gráficos en en el cual se presenta la información gráfica de la app.

    :return: Componente dash.Graph inicializado correctamente con id "time-series-chart".
    """
    graph = dcc.Graph(
        id="time-series-chart",
        config={
            'locale': 'es_ES.utf8',  # Reduce algunos inconvenientes indicando el idioma de la aplicación.
            'responsive': True,
            'displayModeBar': False,
        },
        style={
            'width': '100%',
            'height': '100%',
        },
    )
    return graph


def create_table(df):
    """
    Inicializa y devuelve el componente de tabla en en el cual se presenta la información tabulada de la app.

    :param df: DataFrame a partir de la cual se construye la tabla.
    :return: Componente tabla de dash, inicializado de acuerdo a la DataFrame indicada, con id "table".
    """
    table = dash_table.DataTable(
        id='table',
        columns=[{"name": misc.get_col_title(i), "id": i} for i in df.columns],
        data=df.round(2).to_dict('records'),
        fixed_rows={'headers': True},  # Fija los encabezados de la tabla.
        virtualization=True,  # Maneja de mejor forma la memoria usada para la tabla.
        page_action='native',
        page_size=100,  # Número de filas mostradas por página.
        sort_action="native",  # Permite ordenar las filas de acuerdo a sus valores en las columnas.

        style_cell={
            'height': 'auto',
            'minWidth': '40px',
            'whiteSpace': 'normal',
            'textAlign': 'center',
        },
        style_header={
            'margin': '0px',
            'fontWeight': 'bold',
            'color': 'white',
            'backgroundColor': 'rgb(100, 100, 100)',
        },
        style_table={
            'height': '100%',
            'max-width': '100%',
            'max-height': 'calc(92vh - 10px)',  # Maneja el alto de la talba en la aplicación.
            'overflowY': 'auto',
            'overflowX': 'auto',
        },
    )
    return table


def create_options_downloads():
    """
    (Sin implementar) Crea un componentente HTML de tipo lista desplegable para elegir el tipo de formato de descarga.

    :return: Componente desplegable con las opciones de descarga.
    """
    download_options = dcc.Dropdown(
        id="formato_descarga",
        options=[
            {'label': 'Excel(.xlsx)', 'value': 'excel'},
            {'label': 'Comma Separated Values(.csv)', 'value': 'csv'},
            {'label': 'JSON (.json)', 'value': 'json'},
        ],
        style={
            'width': 'auto',
            'min-width': '250px',
        },
        value='excel',
        placeholder="Seleciona un formato:",
        clearable=False,
        searchable=False
    )
    return download_options


def create_download_section(dl_options):
    """
    (Sin implementar) Crea un DIV HTML con la lista desplegable de formato de descarga y un botón de descarga.

    :param dl_options: Componente HTML que maneja la selección de formato de decarga.
    :return: DIV configurado con las opciones de formato y el botón de descarga de datos.
    """
    dl_section = html.Div(
        id='Div_Descarga',
        style={
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center',
            'flex-wrap': 'wrap',
        },
        children=[
            dl_options,
            html.Button("Descargar", id="boton_descarga"),
        ]
    )
    return dl_section
