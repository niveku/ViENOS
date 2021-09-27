import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from apps import windrose, misc


def figure(df, section, pathname, tipo):

    mode = 'lines+markers'
    point_size = 5
    # ------Variable Format--------

    variable = pathname.capitalize()   # Controls the column to show
    if variable == "Ssta":
        variable = "SSTa"
    elif variable == "Ssa":
        variable = "SSa"
    elif variable in ["Sst", "Ss", "Ssh"]:
        variable = variable.upper()
        # mode = 'markers'
        # point_size = 10

    # ------Graph Generation--------

    line = dict(shape='linear', color='black', width=1)
    a_line = dict(shape='linear', color='rgba(255,0,170,0.4)', width=2, dash='dashdot')

    if variable == 'Wdir':
        df2 = windrose.rose_df(df, mode=0)
        fig = px.bar_polar(df2, r="frecuencia", theta="direccion", color="velocidad",
                           color_discrete_sequence=misc.color_pallete(5))  # px.colors.diverging.Spectral_r)

    elif misc.column_is_valid(section, variable):

        y_title = misc.get_col_title(variable)
        variable_a = variable + 'a'
        fig = go.Figure()

        fig.add_scatter(x=df.Time, y=df[variable], name='Seguimiento',
                        mode=mode, line=line, marker_size=point_size, yaxis='y1',
                        fill='tozeroy', fillcolor='rgba(50,50,50,0.4)')

        if variable_a in df.columns:

            fig.add_scatter(x=df.Time, y=df[variable_a], name='Anomalía',
                            mode=mode, line=a_line, yaxis='y2',
                            marker_size=0.5)

            fig.update_layout(
                yaxis=dict(title=y_title, overlaying='y2'),
                yaxis2=dict(title='Anomalia', side='right'),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    x=.5,
                    y=0,
                    xanchor="center"
                ),
            )

        else:
            fig.update_yaxes(title_text=y_title)  # , zeroline=True, showline=True)

    else:
        raise ValueError('404. The pathname is not valid')

    if variable != 'Wdir':

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

        fig.update_xaxes(range=[df[df[variable].notnull()].Time.min(), df[df[variable].notnull()].Time.max()])
        # fig.update_yaxes(range=[df[df[variable].notnull()][variable].min(),
        # df[df[variable].notnull()][variable].max()])
        # fig.update_xaxes(rangeslider_visible=True) #SLIDER

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
            std = df[variable].std() / 10
            # ---Max---
            fig.add_hline(y=maximo, line_width=3, line_dash="dash", line_color="red")
            fig.add_hrect(y0=maximo - std, y1=maximo + std,
                          line_width=0, annotation_text=f"Max: {maximo}",
                          annotation_font_size=18, annotation_font_color="black",
                          annotation_position="bottom right",
                          fillcolor="red", opacity=0.2)
            # ---MIN---
            fig.add_hline(y=minimo, line_width=3, line_dash="dash", line_color="skyblue")
            fig.add_hrect(y0=minimo - std, y1=minimo + std,
                          line_width=0, annotation_text=f"Min: {minimo}",
                          annotation_font_size=18, annotation_font_color="black",
                          annotation_position="top right",
                          fillcolor="skyblue", opacity=0.2)
            # ---Mean---
            fig.add_hline(y=promedio, line_width=2, line_dash="dash", line_color="gray",
                          annotation_text=f"Promedio: {promedio}", annotation_font_size=18)

    else:

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
