import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from apps import misc, components

# ----------DATA------------------------

df = misc.get_data('ESTACION5_OCEAN_Q')

# --------- COMPONENTS -----------------

datepicker = components.create_datepicker(df.Time.min(), df.Time.max())
time_options = components.create_time_options(['Quincenal', 'Mensual', 'Trimestral'])
min_inp, max_inp = components.create_min_max_input(0, 80)  # df.Depth.min(), df.Depth.max())
tabla = components.create_table(df)
# dl_options = components.create_options_downloads()
# dl_section = components.create_download_section(dl_options)

main_container = html.Div(id='Main_estacion5_table', className='Main_container', children=[])

layout = html.Div(
    id='App_estacion5',
    className='App_container',
    children=[
        main_container,
        html.Div(
            id='estacion5_table_options',
            className='Options_container',
            children=[
                html.Div(
                    className='SubOptions_container',
                    children=[
                        html.P('Periodo:    ', className='p_title'),
                        datepicker,
                    ]
                ),
                html.Div(
                    className='SubOptions_container',
                    children=[
                        html.P('Agrupación temporal:', className='p_title'),
                        time_options,
                    ]
                ),
                html.Div(
                    className='SubOptions_container',
                    children=[
                        html.P('Rango Profundidad: ', className='p_title'),
                        min_inp,
                        html.Br(),
                        max_inp,
                    ]
                ),
            ]
        ),
    ]
)

# --------------CALLBACKS---------------------


@app.callback(
    Output("Main_estacion5_table", "children"),
    [Input("tipo", "value"),
     Input("Date_Picker", "start_date"),
     Input("Date_Picker", "end_date"),
     Input("input_min_depth", "value"),
     Input("input_max_depth", "value")]
)
def update_table(tipo, start_date, end_date, min_depth, max_depth):

    # --------Date Filter/Group---------

    mask_date = misc.data_filter(df.Time, start_date, end_date)
    mask_depth = misc.data_filter_depth(df.Depth, min_depth, max_depth)
    mask = mask_date & mask_depth
    data = misc.data_tipo(df, tipo, mask)

    # ------------ TABLE ----------------

    cols = ["SST", "SSTa", "SS", "SSa"]
    (styles, _) = misc.discrete_background_color_bins(data[cols])  # Table Style
    tabla.style_data_conditional = styles
    tabla.columns = [{"name": misc.get_col_title(i), "id": i} for i in data.columns]
    tabla.data = data.round(2).to_dict('records')
    return [tabla, components.watermark]
