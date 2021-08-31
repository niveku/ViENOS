import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connection to main file
from app import app
from app import server
# Connecion to apps files
from apps import meteo, meteo_fcst, ocean, ocean_fcst

app.layout = html.Div(
    id='ENOS_APP',
    children=[
        dcc.Location(id='url', refresh=False),
        # dcc.Download(id="download_data"),
        html.Div(
            id='page-content',
            children=[],
        ),
    ],
)


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):

    if pathname.startswith('/meteo/'):
        return meteo.layout
    elif pathname.startswith('/meteo_fcst/'):
        return meteo_fcst.layout
    elif pathname.startswith('/ocean/'):
        return ocean.layout
    elif pathname.startswith('/ocean_fcst/'):
        return ocean_fcst.layout
    else:
        return ([
            html.H6('Meteorología', className='main_menu'),
            dcc.Link('- Temperatura', href='/meteo/temp', className='sub_menu'),
            html.Br(),
            dcc.Link('- Precipitación', href='/meteo/prcp', className='sub_menu'),
            html.Br(),
            dcc.Link('- Velocidad Del Viento', href='/meteo/wvel', className='sub_menu'),
            html.Br(),
            dcc.Link('- Rosa de Vientos', href='/meteo/wdir', className='sub_menu'),
            html.Br(),
            dcc.Link('- Tabla de Datos', href='/meteo/table', className='sub_menu'),
            html.Br(),
            html.H6('Pronósticos Meteorología', className='main_menu'),
            dcc.Link('- Temperatura', href='/meteo_fcst/temp', className='sub_menu'),
            html.Br(),
            dcc.Link('- Velocidad Del Viento', href='/meteo_fcst/wvel', className='sub_menu'),
            html.Br(),
            dcc.Link('- Rosa de Vientos', href='/meteo_fcst/wdir', className='sub_menu'),
            html.Br(),
            dcc.Link('- Tabla de Datos', href='/meteo_fcst/table', className='sub_menu'),
            html.Br(),
            html.H6('Oceanografía', className='main_menu'),
            dcc.Link('- Temperatura del Mar', href='/ocean/sst', className='sub_menu'),
            html.Br(),
            dcc.Link('- Salinidad', href='/ocean/ss', className='sub_menu'),
            html.Br(),
            dcc.Link('- Tabla de Datos', href='/ocean/table', className='sub_menu'),
            html.Br(),
            html.H6('Pronósticos Oceanografía', className='main_menu'),
            dcc.Link('- Temperatura del Mar', href='/ocean_fcst/sst', className='sub_menu'),
            html.Br(),
            dcc.Link('- Salinidad', href='/ocean_fcst/ss', className='sub_menu'),
            html.Br(),
            dcc.Link('- Nivel del Mar', href='/ocean_fcst/ssh', className='sub_menu'),
            html.Br(),
            dcc.Link('- Tabla de Datos', href='/ocean_fcst/table', className='sub_menu'),
            html.Br(),
            html.Br(),
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
