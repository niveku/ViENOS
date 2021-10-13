import dash_core_components as dcc
import dash_html_components as html
import dash_table

from app import app
from pandas import to_datetime
from apps import misc

watermark = html.Img(
    src=app.get_asset_url("watermark.png"),
    className='Watermark',
    alt='watermark',
)
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

    minf = to_datetime(min_date)
    maxf = to_datetime(max_date)

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
    return datepicker


def create_time_options(lst_options):

    time_options = dcc.RadioItems(
        id="tipo",
        persistence_type='session',
        options=[{'label': op, 'value': op} for op in lst_options],
        value=lst_options[0],
        labelStyle={
            'box-sizing': 'border-box',
            'display': 'inline-block',
            'padding': '5px',
            'text-align': 'justify'
        },
    )
    return time_options


def create_range_slider(column, item_id):
    mini = max(int(column.min()) - 1, 0)
    maxi = min(int(column.max()), 80)
    range_slider = dcc.Slider(
        id=item_id,
        min=mini,
        max=maxi,
        step=10,
        marks={i: {'label': "{}m".format(i)}  # , 'style': {'transform': 'rotate(180deg)'}}
               for i in range(mini, maxi + 1, 10)},
        # allowCross=False,
        # pushable=5,
        value=mini,  # [mini, maxi],
        vertical=True,
    )
    return range_slider


def create_graph():
    graph = dcc.Graph(
        id="time-series-chart",
        config={
            'locale': 'es_ES.utf8',
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
    table = dash_table.DataTable(
        id='table',
        columns=[{"name": misc.get_col_title(i), "id": i} for i in df.columns],
        data=df.round(2).to_dict('records'),
        fixed_rows={'headers': True},
        # virtualization=True,
        # page_action='native',
        # page_size=24,
        sort_action="native",

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
            'max-height': 'calc(90vh - 10px)',
            'overflowY': 'overlay',
            'overflowX': 'scroll',
        },
    )
    return table


def create_options_downloads():
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
    dl_section = html.Div(
        id='Div_Descarga',
        style={
            'box-sizing': 'border-box',
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
