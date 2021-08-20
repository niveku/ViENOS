import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from apps import windrose, misc


def figure(df, section, pathname, tipo):

    # ------Variable Format--------

    variable = pathname.capitalize()   # Controls the column to show
    if variable in ["Sst", "Ss"]:
        variable = variable.upper()

    # ------Graph Generation--------

    line = dict(shape='linear', color='black', width=1,)

    if variable == 'Wdir':
        df2 = windrose.rose_df(df, mode=0)
        fig = px.bar_polar(df2, r="frequency", theta="direction", color="speed",
                           color_discrete_sequence=misc.color_pallete(5))  # px.colors.diverging.Spectral_r)
    elif misc.column_is_valid(section, variable):
        y_title = misc.get_col_title(variable)
        fig = go.Figure(data=go.Scatter(x=df.Time, y=df[variable], mode='lines+markers', line=line, marker_size=3))
        fig.update_yaxes(title_text=y_title, zeroline=True, showline=True)

    else:
        raise Exception('The pathname is not valid.')

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

        fig.update_xaxes(range=[df.Time.min(), df.Time.max()])
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
    else:

        fig.update_layout(
            autosize=True,
            margin=dict(l=5, r=5, b=20, t=15),
            # paper_bgcolor="LightBlue",
        )

    return fig, df
