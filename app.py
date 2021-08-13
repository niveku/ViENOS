import dash

# external_stylesheets = [dbc.themes.JOURNAL]

app = dash.Dash(__name__,
                title='VIENOS App',
                # external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True,
                meta_tags=[{'name':'VIENOS App', 'content':  'width=device-width, initial-scale=1'}])
server = app.server
