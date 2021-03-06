"""
Módulo que maneja la página principal y las conexiones a las distintas páginas de la aplicación.
Además, cuanta con un pequeño menú de vínculos útil para el desarrollo.
"""
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connection to main file
from app import app
from app import server
# Connecion to apps files
from apps import meteo, meteo_fcst, ocean, ocean_fcst, estacion5, estacion5_table

# ---------------- HTML LAYOUT --------------

app.layout = html.Div(
    id='ENOS_APP',
    children=[
        dcc.Location(id='url', refresh=False),
        # dcc.Download(id="download_data"), componente de descarga en desuso.
        html.Div(
            id='page-content',
            children=[],
        ),
    ],
)

# -------------- CALLBACKS --------------------


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    """Llama la página de la aplicación correspondiente a la URL o crea una menu de navegación simple."""

    #  Retorna la página de la aplicación requerida.
    if pathname.startswith('/estacion5/table'):
        return estacion5_table.layout
    elif pathname.startswith('/estacion5/'):
        return estacion5.layout
    elif pathname.startswith('/meteo/'):
        return meteo.layout
    elif pathname.startswith('/meteo_fcst/'):
        return meteo_fcst.layout
    elif pathname.startswith('/ocean/'):
        return ocean.layout
    elif pathname.startswith('/ocean_fcst/'):
        return ocean_fcst.layout

    else:  # Menú de navegación sencillo
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
            dcc.Link('- Precipitación', href='/meteo_fcst/prcp', className='sub_menu'),
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
            dcc.Link('- Nivel del Mar', href='/ocean/ssh', className='sub_menu'),
            html.Br(),
            dcc.Link('- Salinidad', href='/ocean/ss', className='sub_menu'),
            html.Br(),
            dcc.Link('- Tabla de Datos', href='/ocean/table', className='sub_menu'),
            html.Br(),
            html.H6('Pronósticos Oceanografía', className='main_menu'),
            dcc.Link('- Temperatura del Mar', href='/ocean_fcst/sst', className='sub_menu'),
            html.Br(),
            dcc.Link('- Nivel del Mar', href='/ocean_fcst/ssh', className='sub_menu'),
            html.Br(),
            dcc.Link('- Salinidad', href='/ocean_fcst/ss', className='sub_menu'),
            html.Br(),
            dcc.Link('- Tabla de Datos', href='/ocean_fcst/table', className='sub_menu'),
            html.Br(),
            html.H6('Estación 5', className='main_menu'),
            dcc.Link('- Temperatura del Mar', href='/estacion5/sst', className='sub_menu'),
            html.Br(),
            dcc.Link('- Anomalía: Temperatura del Mar', href='/estacion5/ssta', className='sub_menu'),
            html.Br(),
            dcc.Link('- Salinidad', href='/estacion5/ss', className='sub_menu'),
            html.Br(),
            dcc.Link('- Anomalía: Salinidad', href='/estacion5/ssa', className='sub_menu'),
            html.Br(),
            dcc.Link('- Tabla de Datos', href='/estacion5/table', className='sub_menu'),
            html.Br(),
        ])


if __name__ == '__main__':  # Ejecución local de la aplicación.
    app.run_server(  # Modo de ejecución de la app.
        debug=True  # True presenta un menu debugger en la app con callbacks y errores | False = Modo producción
    )
