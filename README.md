<h1 align="center">VIENOS - Vigilancia Integrada del fenómeno de "El Niño"</h1> 

VIENOS es un proyecto de la dirección general marítima colombiana ([Dimar](https://www.dimar.mil.co/)) el cual busca
dar un seguimiento y vigilancia integrada al fenómeno de "El niño". Esta aplicación consta de una serie de tableros de
control ("Dashboards") interactivos, dispuestos como servicios web. Estos dashboards permiten filtrar e interactuar con
la información oceanográfica y meteorológica reunida y dispuesta por el Centro de Investigaciones Oceanográficas e
Hidrográficas (CIOH o CCCP) Pacífico. Este centro de investigaciones se encuentra ubicado en Tumaco, en el pacífico 
colombiano.

## Tabla de contenidos

1. Objetivo
2. Alcance
3. Uso
4. Requerimientos
   1. Librerias
   2. Otros requerimientos
5. Licencia

## 1. Objetivo
Especificamente, esta herramienta busca facilitar la presentación de datos oceanográficos y meteorológicos, de forma
sencilla, a través de un conjunto de dashboards interactivos que permiten diferentes filtros y agrupaciones temporales.
Estos datos son presentados en forma de graficos de líneas, tablas de datos y rosas de viento.

## 2. Alcance
Este aplicativo web está dirigido a todas las personas que busquen visualizar datos oceanográficos y meteorológicos 
de seguimiento al "Fenómeno del Niño" en el pacífico colombiano. Los usuarios pueden de la comunidad en general o 
profesionales internos o externos a Dimar.

Adicionalmente, el código de la aplicación está orientado a ser escalable y fácil de leer. Permitiendo pensar en 
futuras adiciones de funcionalidades y recuros a esta. Esto, con miras en brindar un servicio más robusto en la 
visualización de dicho datos.

## 3. Uso

Esta aplicación está en proceso de despliegue, una vez se disponga la dirección web definitiva se hará pública y 
abierta al público para la consulta y visualización de datos. No obstante, existe una versión de prueba, de una versión 
antigua, que puede encontrarse en:
https://vienos.herokuapp.com/

## 4. Requerimientos:

La aplicación está construida en python 3.8.5 por lo que se necesitará de un ambiente con Python 3+ con las librerias 
adecuadas para correr de manera local.

### 4.1 Librerias

Esta plataforma está basada principalmente en las siguientes librerias:

- Flask
- Dash (1.21)
- Plotly
- Pandas
- Pyodbc
- Colorlover

Para ver una lista detallada de los requerimientos revisar el archivo
[requirements.txt](https://github.com/niveku/ViENOS/blob/main/requirements.txt).

Igualemente, las librerías necesarias se pueden instalar ejucatando el siguiente comando en la carpeta principal de la 
aplicación:
```
pip install - r requirements.txt
```
>**NOTA:** Es importante que la versión de Dash sea la versión 1.21, ya que la siguiente versión lanzada es la 2.0 en la
que se cambiaron aspectos importantes del funcionamiento e importación de librerias de este paquete. Por lo que aún
no es compatible con esta aplicación.


### 4.2 Otros requerimientos

Es necesario tener un archivo llamado "settings.py" en la raiz de la aplicación con los usuarios y contraseñas para el
ingreso a las bases de datos. Esto junto a un entorno o conexión VPN que permita la conexión con la base de datos.
De lo contrario, la aplicación trabajará de manera fuera de línea ("offline") con los archivos de respaldo .csv 
guardados.

```python
import settings

# Datos provenientes del archivo settings.py local
username = settings.username
password = settings.password
```

## 5. Arquitectura del sistema

Esta aplicación está construida enteramente en Python, ya que necesita una gran capacidad de transformación y agrupación
de datos. Para ello, se implementó agrupaciones y transformaciones de datos empleando la librería de Pandas para python.
Para la parte visual se trabajó con la librería de Dash para Python, la cual se especializa en la creación de dashboards 
interactivos web, basados en HTML+CSS, Plotly, Flask y React.

### 5.1 Arquitectura de la aplicación
```
ViENOS
| .gitignore
| app.py
| index.py
| Procfile
| README.md
| requirements.txt
| settings. py
|
|-- apps
|   | __init__.py
|   | components.py
|   | estacion5.py
|   | graphs.py
|   | meteo.py
|   | meteo_fcst.py
|   | misc.py
|   | ocean.py
|   | ocean_fcst.py
|   | windrose.py
|
|-- assets
|   | cecoldo_logo.png
|   | dash.css
|   | favicon.ico
|   | watermark.png
|
|-- datasets
|   | ESTACION5_OCEAN_Q.csv
|   | TUMACO_METEO_FCST_H.csv
|   | TUMACO_METEO_H.csv
|   | TUMACO_OCEAN_D.csv
|   | TUMACO_OCEAN_FCST_D.csv
```
- gitignore: Contiene la información de las carpetas y archivos a ignorar en el repositorio. Es importante que el 
archivo settings.py (con las contraseñas y usuarios) este referenciado acá.
- app.py: Módulo principal encargado de generar la aplicación y el servidor asociado.
- index.py Módulo que maneja la página principal y las conexiones a las distintas páginas de la aplicación.
- Procfile: Archivo de texto que maneja las interfaces de las apps en algunas plataformas de despliegue como heroku.
- README.md: Archivo de documentación básica de la aplicación.
- requirements.txt: Archivo de texto parametrizado que indica las librerías y versiones de Python necesarias para 
ejecutar el programa.
- settings.py: Módulo que almacena localmente contraseñas y usuarios requeridos para la conexión a la base de datos.


- **apps: Carpeta empaquetada con los códigos de cada parte de la aplicación:**
  + \_\_init\_\_.py: Archivo que indica la naturaleza empaquetada de la carpeta o módulo.
  + components.py: Módulo que se encarga de generar todos los componentes funcionales interactivos de los dashboards.
Es decir, los inputs, sliders, gráficas y tablas.
  + estacion5.py: Módulo que se encarga del funcionamiento y presentación de la página de "Estación 5" (/estacion5).
  + estacion5_table: Módulo que se encarga del funcionamiento y presentación de la página de tablas para 
"Estación 5" (/estacion5).
  + graphs.py: Módulo que se encarga de la creación y validación de los gráficos de la aplicación.
  + meteo.py: Módulo que se encarga del funcionamiento y presentación de la página de Meteorología (/meteo).
  + meteo_fcst.py: Módulo que se encarga del funcionamiento y presentación de la página de Predicción Meteorología
(/meteo_fcst).
  + misc.py: Módulo que se encarga de todas las funciones complementarias de la aplicación. Incluyen entre otras: 
conexiones a bases de datos, carga y adecuación de información, manejos de estilos, entre otros.
  + ocean.py: Módulo que se encarga del funcionamiento y presentación de la página de Oceanografía (/ocean).
  + ocean_fcst.py: Módulo que se encarga del funcionamiento de la página de predicciones oceanográficas (/ocean_fcst).
  + windrose.py: Módulo que se encarga de la manipulación de los datos originales para generar un DataFrame adecuado
para la presentación de la información en una rosa de vientos (Rose Diagram). Con las columnas y nombres estandarizados.
- **assets: Carpeta que contiene archivos e imágenes adicionales relacionados con la estética de la aplicación.**
  + ceoldo_logo.png: Logo de cecoldo empleado en versiones anteriores para generar un botón.
  + dash.css: Archivo de definición de estilos HTML-CSS para la aplicación y sus componentes.
  + favicon.ico: Logo que aparece en la pestaña de la página en los navegadores.
  + watermark.png: Logo de Dimar empleado para la marca de agua de la aplicación.
- **datasets: carpeta con los archivos .csv de respaldo de las tablas que maneja la aplicación.**

### 5.2 Arquitectura de la base de datos

La base de datos está alojada en un servidor de Dimar, por lo que es necesario tener las conexiones y permisos adecuados
para su consulta.

La base de datos se estructura de la siguiente manera:

```
BTASQLCLUSIG
|--- SIGDIMAR
|   |--- SIGDIMAR
|   |   | TUMACO_METEO_H
|   |   | TUMACO_METEO_FCST_H
|   |   | TUMACO_OCEAN_D
|   |   | TUMACO_OCEAN_FCST_D
|   |   | ESTACION5_OCEAN_Q
```

Estas tablas se transforman en estructuras DataFrame dentro de python utilizando las librerias de Pandas y pyodbc
de esta forma:

```python
import settings
import pandas as pd
import pyodbc

server = "BTASQLCLUSIG\\SIGDIMAR"  # Tener cuidado con el "\"
database = 'SIGDIMAR'

# Datos provenientes del archivo settings.py local
username = settings.username
password = settings.password

table = ""  # Tablas válidas:TUMACO_METEO_H, TUMACO_METEO_FCST_H, TUMACO_OCEAN_D, TUMACO_OCEAN_FCST_D, ESTACION5_OCEAN_Q

cnxn = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=' + server +
    ';DATABASE=' + database +
    ';UID=' + username +
    ';PWD=' + password
)

dataframe = pd.read_sql_query('SELECT * FROM [Esquema_Vienos].[' + table + ']', cnxn)
```

## Licencia
[MIT](https://choosealicense.com/licenses/mit/)

<center>Dimar 2021 ©</center>