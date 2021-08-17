import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from apps import windrose, misc


def figure(df, pathname, tipo):
    variable = 'Temp'  # Controls the column to show

    # ------Variable URL Selector--------

    if pathname == '/prcp':
        variable = 'Prcp'
        fig = go.Figure(data=go.Scatter(x=df.Time, y=df.Prcp, mode='lines+markers'))
        fig.update_yaxes(title_text='Precipitaciones (mL)', zeroline=True, showline=True)
    elif pathname == '/wvel':
        variable = 'Wvel'
        fig = go.Figure(data=go.Scatter(x=df.Time, y=df.Wvel, mode='lines+markers'))
        fig.update_yaxes(title_text='Velocidad del Viento (m/s)', zeroline=True, showline=True)
    elif pathname == '/wdir':
        df2 = windrose.rose_df(df, mode=0)
        fig = px.bar_polar(df2, r="frequency", theta="direction", color="speed",
                           color_discrete_sequence=misc.color_pallete(5))  # px.colors.diverging.Spectral_r)
    else:
        fig = go.Figure(data=go.Scatter(x=df.Time, y=df.Temp, mode='lines+markers', line_color="black"))
        fig.update_yaxes(title_text='Temperatura (C°)', zeroline=True, showline=True)

    # ----------Max/Min Annotations----------

    if len(df[variable]) > 2 and pathname != '/wdir':
        maximo = round(df[variable].max(), 2)
        minimo = round(df[variable].min(), 2)
        std = df[variable].std() / 4
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

    if pathname != '/wdir':
        fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black', ticks="outside")
        fig.update_layout(
            hovermode="x",
            autosize=True,
            margin=dict(l=0, r=0, b=25, t=0),
            # paper_bgcolor="LightBlue",
        )
    else:

        fig.update_layout(
            autosize=True,
            margin=dict(l=5, r=5, b=20, t=15),
            # paper_bgcolor="LightBlue",
        )

    # --------X-Axis Updates -----------

    mini = df.Time.min()
    maxi = df.Time.max()

    if pathname != '/wdir':

        fig.update_xaxes(range=[mini, maxi])
        # fig.update_xaxes(rangeslider_visible=True) #SLIDER

        if tipo == 'Diaria':
            fig.update_xaxes(tickformat='%d/%m/%Y')
            df["Time"] = pd.to_datetime(df.Time).dt.strftime('%Y/%m/%d')
        if tipo == 'Horaria':
            fig.update_xaxes(tickformat='%d/%m/%Y - %H:%M')
            df["Time"] = df.Time.dt.strftime('%Y/%m/%d - %H:%M')

    return fig, df
