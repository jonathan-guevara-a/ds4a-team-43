import json
import calendar
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from sqlalchemy import create_engine, text
from application import app

file = open("secure/database.txt", "r")
lines = file.readlines()
DB_USERNAME = lines[0].rstrip()
DB_PASSWORD = lines[1].rstrip()
file.close()

with open('data/cali_barrios.geojson', encoding = "utf-8") as geo:
    geojson = json.loads(geo.read())

engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@database-ds4a.chsrwcmrt1zt.us-east-2.rds.amazonaws.com/postgres", max_overflow = 20)

query = """
    SELECT      FECHAHORA,
                ACTIVIDAD.ID_BARRIO,
                BARRIO.BARRIO,
                BARRIO.COMUNA AS COMUNA,
                BARRIO.ESTRA_MODA,
                BARRIO.ZONA,
                BARRIO.AREA,
                TIPO_CRIMEN,
                CANTIDAD
    FROM        TARGETING.FCT_ACT_CRIMINAL AS ACTIVIDAD
                LEFT JOIN
                TARGETING.DIM_BARRIOS AS BARRIO
                    ON BARRIO.ID_BARRIO = ACTIVIDAD.ID_BARRIO
    WHERE       ACTIVIDAD.ID_BARRIO IS NOT NULL
"""

base_df = pd.read_sql_query(query, con = engine)

year_min = base_df["fechahora"].dt.year.min()
year_max = base_df["fechahora"].dt.year.max()
zone_list = sorted(base_df["zona"].unique())
commune_list = sorted(base_df["comuna"].unique())
borough_list = sorted(base_df["barrio"].unique())
crime_list = sorted(base_df["tipo_crimen"].unique())

grouped_year_df = base_df[["fechahora", "cantidad"]]\
.groupby([base_df["fechahora"].dt.year]).sum().reset_index().rename(columns = {"fechahora": "anio"})

grouped_year_crime_df = base_df[["fechahora", "tipo_crimen", "cantidad"]]\
.groupby([base_df["fechahora"].dt.year, "tipo_crimen"]).sum().reset_index().rename(columns = {"fechahora": "anio"})

year_line_figure = px.line(
    grouped_year_df,
    x = "anio",
    y = "cantidad",
    height = 700,
    color_discrete_sequence = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928"]
)

year_crime_line_figure = px.line(
    grouped_year_crime_df[~grouped_year_crime_df["tipo_crimen"].isin(["HURTO PERSONAS", "LESION PERSONAL"])],
    x = "anio",
    y = "cantidad",
    color = "tipo_crimen",
    height = 700,
    color_discrete_sequence = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928"]
)

layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Graph(
                        id="year-line-graph",
                        figure = year_line_figure
                    )
                ],
                lg = 6,
                sm = 12
            ),
            dbc.Col(
                [
                    dcc.Graph(
                        id="year-crime-line-graph",
                        figure = year_crime_line_figure
                    )
                ],
                lg = 6,
                sm = 12
            )
        ]
    )
])
