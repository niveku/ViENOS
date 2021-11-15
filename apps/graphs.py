"""Este modulo se encarga de la creación y validación de los gráficos de la aplicación."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from apps import windrose, misc


def figure(df, pathname, tipo):
    """
    Genera la gráfica formateada correspondiente a la información y parámetros solicitados.

    :param df: DataFrame filtrado que contiene la información para crear la gráfica.
    :param pathname: Variable a graficar extraida de la URL.
    :param tipo: Agrupación temporal seleccionada.
    :return: DataFrame, Figure. Devuelve la DataFrame adecuada junto a la gráfica generada.
    :raise: Error404 En caso de no encontrar las variables que se le indica en la URL
    """

    # ------- Style and Size --------

    mode = 'lines+markers'
    point_size = 5

    # ------ Variable Format --------

    variable = pathname.capitalize()   # Controla y unifica la variable a mostrar
    if variable == "Ssta":
        variable = "SSTa"
    elif variable == "Ssa":
        variable = "SSa"
    elif variable in ["Sst", "Ss", "Ssh"]:
        variable = variable.upper()
        # mode = 'markers'
        # point_size = 10

    # ------Graph Generation--------

    std = df[variable].std()  # Desviación estandar de la variable.
    line = dict(shape='linear', color='black', width=1)  # Tipo de línea.

    if variable == 'Wdir':  # Creación de rosa de vientos.
        df2 = windrose.rose_df(df, mode=0)  # Adecuación de datos para la rosa.
        fig = px.bar_polar(df2, r="frecuencia", theta="direccion", color="velocidad",
                           color_discrete_sequence=misc.color_pallete(5))  # Llama los mismo colores de las tablas.

    elif misc.column_is_valid(variable):  # Creación otras gráficas.

        y_title = misc.get_col_title(variable)  # Título del eje y
        fig = go.Figure()
        fig.add_scatter(x=df.Time, y=df[variable], name='Seguimiento',
                        mode=mode, line=line, marker_size=point_size, yaxis='y1',
                        fill='tozeroy', fillcolor='rgba(50,50,50,0.4)')  # Relleno de la gráfica

        fig.update_yaxes(title_text=y_title)

    else:  # La URL no es válida.
        raise ValueError('404. The pathname is not valid')

    # -------------- Style Updates --------------

    if variable != 'Wdir':  # Para las que no son la rosa de viento

        # --------Graph Layout Updates -----------

        fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black', ticks="outside")
        fig.update_layout(
            hovermode="x",
            autosize=True,
            margin=dict(l=0, r=0, b=25, t=0),
            # paper_bgcolor="LightBlue",
        )

        # --------X-Axis Updates -----------

        fig.update_xaxes(range=[df[df[variable].notnull()].Time.min(),
                                df[df[variable].notnull()].Time.max()])
        fig.update_yaxes(range=[df[df[variable].notnull()][variable].min()-std,
                                df[df[variable].notnull()][variable].max()+std])
        # fig.update_xaxes(rangeslider_visible=True) # Slider dentro de la gráfica.

        if tipo == 'Diaria' or tipo == 'Quincenal':
            fig.update_xaxes(tickformat='%d/%m/%Y')
            df["Time"] = pd.to_datetime(df.Time).dt.strftime('%Y/%m/%d')

        elif tipo == 'Horaria':
            fig.update_xaxes(tickformat='%d/%m/%Y - %H:%M')
            df["Time"] = df.Time.dt.strftime('%Y/%m/%d - %H:%M')

        # ----------Max/Min Annotations----------

        if len(df[variable]) > 2:

            maximo = round(df[variable].max(), 2)
            minimo = round(df[variable].min(), 2)
            promedio = round(df[variable].mean(), 2)

            # ---Max---
            fig.add_hline(y=maximo, line_width=3, line_dash="dash", line_color="red")
            fig.add_hrect(y0=maximo - (std/10), y1=maximo + (std/10),
                          line_width=0, annotation_text=f"Max: {maximo}",
                          annotation_font_size=18, annotation_font_color="black",
                          annotation_position="bottom right",
                          fillcolor="red", opacity=0.2)
            # ---MIN---
            fig.add_hline(y=minimo, line_width=3, line_dash="dash", line_color="skyblue")
            fig.add_hrect(y0=minimo - (std/10), y1=minimo + (std/10),
                          line_width=0, annotation_text=f"Min: {minimo}",
                          annotation_font_size=18, annotation_font_color="black",
                          annotation_position="top right",
                          fillcolor="skyblue", opacity=0.2)
            # ---Mean---
            fig.add_hline(y=promedio, line_width=2, line_dash="dash", line_color="gray",
                          annotation_text=f"Promedio: {promedio}", annotation_font_size=18)

    else:  # Para la rosa de vientos.

        fig.update_layout(
            autosize=True,
            margin=dict(l=5, r=5, b=0, t=25),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                x=.5,
                y=-.12,
                xanchor="center"
            ),
        )

    return fig, df
