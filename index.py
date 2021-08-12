import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connection to main file
from app import app
# Connecion to apps files
from apps import meteo

h=0

app.layout = html.Div(
    id = 'ENOS_APP',
    style={
        'box-sizing': 'border-box',
        'max-height': '100%',
        'max-width': '100%',
        },
        
    children=[
        dcc.Location(id='url', refresh=False),
        html.Div(
            id='page-content',
            children=[],
            style={
                'box-sizing': 'border-box',
                'height': '100%',
                'max-height': '98vh',
                'border': '1px solid black',
                'padding': '10px',
            },
        ),
    ],
)

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname.startswith('/meteo'):
        return meteo.layout
    #elif pathname == '/frcst_meteo':
    #    return meteo.layout
    else:
        return ([   
            dcc.Link('Meorología', href='/meteo/temp'),
            html.Br(),
            dcc.Link('Pronóstico meorología', href='/frcst_meteo'),
            html.Br(),
            dcc.Link('Oceanografía', href='/oceano'),
            html.Br(),
            dcc.Link('Pronóstico Oceanografía', href='/frcst_oceano'),
            html.Br(),
        ])

if __name__ == '__main__':
    app.run_server(debug=True)