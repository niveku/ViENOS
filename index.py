import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connection to main file
from app import app
from app import server
# Connecion to apps files
from apps import meteo, ocean

app.layout = html.Div(
    id='ENOS_APP',
    children=[
        dcc.Location(id='url', refresh=False),
        html.Div(
            id='page-content',
            children=[],
            style={
                'height': '100%',
                # 'width': '100vw',
                'box-sizing': 'border-box',
                'border': '1px solid black',
            },
        ),
    ],
)


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname.startswith('/meteo'):
        return meteo.layout
    # elif pathname == '/frcst_meteo':
    #    return meteo.layout
    elif pathname.startswith('/ocean'):
        return ocean.layout
    else:
        return ([
            dcc.Link('Meorología', href='/meteo/temp'),
            html.Br(),
            dcc.Link('Pronóstico meorología', href='/frcst_meteo'),
            html.Br(),
            dcc.Link('Oceanografía', href='/ocean/sst'),
            html.Br(),
            dcc.Link('Pronóstico Oceanografía', href='/frcst_oceano'),
            html.Br(),
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
