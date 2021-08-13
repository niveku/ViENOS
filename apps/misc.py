import dash_html_components as html
import colorlover
# import pandas as pd
# import mysql.connector as connector


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

# def conexion():
#     conexion = None
#     try:
#         #SQL server
#         conexion = connector.connect(
#         host='BTASQLCLUSIG\SIGDIMAR',
#         user='Esquema_Vienos',
#         password='*VIENOSC2021*')
#         print('Conexión Exitosa')
#     except:
#         print ('Error')
#     return conexion
