"""
Este modulo se encarga de la manipulación de los datos originales para generar un DataFrame adecuado para la
presentación de la información en una rosa de vientos (Rose Diagram). Con las columnas y nombres estandarizados.
"""

import numpy as np
import pandas as pd


def deg_to_compass(num, modo=0, divisiones=16):
    """
    Este método transforma una dirección en grados a un categoria manejable para una rosa de vientos.
    Estas categorias pueden ser grupos numéricos (0°,90°,180°,270°) o direcciones geográficas (N,NE,E,SE...)

    :param num: Float. Dirección en grados geográficos (0°+-360°)

    :param modo: Int. 0 para categoria numérica (ej. 0°,90°,180°,270°). Otro  para categorias en texto (N,NE,E,SE...).

    :param divisiones: Int. Indica la cantidad de grupos en los que se separan los 360° o las direcciones.
                       Para modo geográfico sólo admite 4, 8 o 16 divisiones

    :return: Int/Str La categoría a la que pertenece el número dependiendo el modo.
    """
    
    if modo == 0:  # Modo numérico
        direc = list(np.linspace(0, 360-360/divisiones, divisiones))
        direc = [round(e, 2)for e in direc]
    else:  # Modo geográfico
        if divisiones == 4:
            direc = ["N", "E", "S", "W"]
        elif divisiones == 8:
            direc = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        else:
            divisiones = 16
            direc = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S",
                     "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        
    if not np.isnan(num):  # Revisa si es un número válido.

        divisor = 360 / divisiones
        ajuste = 360 / (divisiones*2)
        azimuth = (num % 360)-ajuste
        val = int(np.ceil(azimuth/divisor))

        return direc[(val % divisiones)]
    else:
        return np.NAN


def rose_df(df, mode=0):
    """
    Convierte un DataFrame de entrada que contenga información de velocidad (Wvel) y dirección (Wdir) de viento en
    un DataFrame listo para ser usado en la rosa de vientos. Este contiene grupos de categorias de dirección, categorias
    de velocidad y frecuencia de ocurrencia en estas dos condiciones.

    :param df: DataFrame con la información de la cual se va a construir el DataFrame de rosa de vientos.
               Debe contener las columnas:
                    - Dirección de viento (Wdir) en grados geográficos.
                    - Velocidad del viento (Wvel) en m/s.

    :param mode: Int. Tipo de categoria en la que se presenta la direccion del viento en el DataFrame de salidad.
                 0 para categoria numérica (ej. 0°,90°,180°,270°). Otro  para categorias en texto (N,NE,E,SE...).

    :return: DataFrame con la información configurada para presentarla en el diagrama de rosa de vientos.
    """
    
    df2 = df[df.Wdir.notnull()].copy()  # Copia el DataFrame sin valores nulos de dirección de viento.

    # ---- Categorias de velocidades ----

    bins = [0, 1, 2, 3, 4, np.inf]
    names = ['<1', '1-2', '2-3', '3-4', '4+']

    # ------------- Manejo ---------------

    df2['direccion'] = df2.Wdir.apply(deg_to_compass, modo=mode)
    df2.sort_values(['direccion', 'Wvel'], ascending=False, inplace=True)
    df2['velocidad'] = pd.cut(df2['Wvel'], bins, labels=names)
    df2['frecuencia'] = 1
    df2 = df2.groupby(['direccion', 'velocidad']).agg({'frecuencia': 'count'}).reset_index()
    df2.frecuencia = round(df2.frecuencia*100/df2.frecuencia.sum(), 2)
    # df2.direction = pd.Categorical(df2.direction, categories=direc, ordered=True)
    # df2.sort_values(['direction','speed'],ascending=False,inplace=True)
    return df2
