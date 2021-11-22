"""Módulo encargado de generar la aplicación principal y el servidor asociado"""
import dash

keywords = ('ENOS, Vienos, CIOH, CCCP, Pacífico, Dimar, fenómeno, Fenomeno, Niño, meteorología, oceanografía,'
            'IDE, Marítima, pacific, phenomenon, meteorology, oceanography, temperature, temperatura, mar, sea')

app = dash.Dash(__name__,
                title='VIENOS App',
                suppress_callback_exceptions=True,
                meta_tags=[{
                    'name': 'VIENOS App',
                    'author': 'Kevin Henao',
                    'content':  'width=device-width, initial-scale=1',
                    'description': 'Application created to observe El niño phenomenon in the colombian pacific.'
                                   'Information collected at CIOH Pacífico',
                    'keywords': keywords,
                    'robots': 'index',
                    'copyright': 'Dirección General Marítima. Todos los derechos reservados',
                    'year': '2021'
                }])
server = app.server
