import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from application import app
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import calendar
import json
from dash.dependencies import Input, Output
from sqlalchemy import create_engine, text

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
    FROM        TARGETING.FCT_ACTIVIDAD_CRIMINAL AS ACTIVIDAD
                LEFT JOIN
                TARGETING.DIM_BARRIOS AS BARRIO
                    ON BARRIO.ID_BARRIO = ACTIVIDAD.ID_BARRIO
    WHERE       ACTIVIDAD.ID_BARRIO IS NOT NULL
"""

df = pd.read_sql_query(query, con = engine)

year_min = df["fechahora"].dt.year.min()
year_max = df["fechahora"].dt.year.max()
zone_list = sorted(df["zona"].unique())
commune_list = sorted(df["comuna"].unique())
borough_list = sorted(df["barrio"].unique())
crime_list = sorted(df["tipo_crimen"].unique())

map_figure = go.Figure(
    go.Choroplethmapbox()
)

map_figure.update_layout(
    mapbox_style = "carto-positron",
    mapbox_zoom = 11,
    mapbox_center = {"lat": 3.420, "lon": -76.530},
    height = 700
)

layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H3("Filters"),
                    html.Label("Year:"),
                    html.Br(),
                    dcc.RangeSlider(
                        id = "year-slider",
                        dots = True,
                        min = year_min,
                        max = year_max,
                        value = [year_min, year_max],
                        step = 1,
                        marks = {
                            i : f"{i}" for i in range(year_min, (year_max + 1))
                        }
                    ),
                    html.Br(),
                    html.Br(),
                    html.Label("Month:"),
                    html.Br(),
                    dcc.RangeSlider(
                        id = "month-slider",
                        dots = True,
                        min = 1,
                        max = 12,
                        value = [1, 12],
                        step = 1,
                        marks = {
                            i : f"{calendar.month_abbr[i]}" for i in range(1, 13)
                        }
                    ),
                    html.Br(),
                    html.Br(),
                    dcc.Checklist(
                        id = "corregimientos-check",
                        options = [
                            {"label": "   Include \"Corregimientos\"", "value": "Y"},
                        ],
                        value = ["Y"]
                    ),
                    html.Br(),
                    html.Label("Zone:"),
                    html.Br(),
                    dcc.Dropdown(
                        id = "zone-dropdown",
                        options = [
                            {"label": f"{i}", "value": i} for i in zone_list
                        ],
                        multi = True
                    ),
                    html.Br(),
                    html.Label("Commune:"),
                    html.Br(),
                    dcc.Dropdown(
                        id = "commune-dropdown",
                        options = [
                            {"label": f"Commune {i}", "value": i} for i in commune_list
                        ],
                        multi = True
                    ),
                    html.Br(),
                    html.Label("Borough:"),
                    html.Br(),
                    dcc.Dropdown(
                        id = "borough-dropdown",
                        options = [
                            {"label": f"{i.title()}", "value": i} for i in borough_list
                        ],
                        multi = True
                    ),
                    html.Br(),
                    html.Label("Crime:"),
                    html.Br(),
                    dcc.Dropdown(
                        id = "crime-dropdown",
                        options = [
                            {"label": f"{i.title()}", "value": i} for i in crime_list
                        ],
                        multi = True
                    )
                ],
                lg = 4,
                sm = 12
            ),
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="map-graph",
                                    figure = map_figure
                                )
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="bar-graph"
                                )
                            )
                        ]
                    )
                ],
                lg = 8,
                sm = 12
            )
        ],
        className = "p-3"
    )
])

@app.callback(
    [
        Output('map-graph', 'figure'),
        Output('bar-graph', 'figure')
    ],
    [
        Input('year-slider', 'value'),
        Input('month-slider', 'value'),
        Input('zone-dropdown', 'value'),
        Input('commune-dropdown', 'value'),
        Input('borough-dropdown', 'value'),
        Input('crime-dropdown', 'value'),
        Input('corregimientos-check', 'value')
    ]
)
def update_map(year, month, zone, commune, borough, crime, corregimientos):
    print(corregimientos)
    filtered_df = df.copy()

    if (len(corregimientos) == 0):
        filtered_df = filtered_df[filtered_df["zona"] != "Corregimiento"]

    if (year):
        filtered_df = filtered_df[(filtered_df["fechahora"].dt.year >= year[0]) & (filtered_df["fechahora"].dt.year <= year[1])]

    if (month):
        filtered_df = filtered_df[(filtered_df["fechahora"].dt.month >= month[0]) & (filtered_df["fechahora"].dt.month <= month[1])]

    if (zone):
        filtered_df = filtered_df[filtered_df["zona"].isin(zone)]

    if (commune):
        filtered_df = filtered_df[filtered_df["comuna"].isin(commune)]

    if (borough):
        filtered_df = filtered_df[filtered_df["barrio"].isin(borough)]

    if (crime):
        filtered_df = filtered_df[filtered_df["tipo_crimen"].isin(crime)]

    top_df = filtered_df[["barrio", "cantidad"]].groupby("barrio").sum().sort_values(by = "cantidad", ascending = False).reset_index().head(20)
    filtered_crime_df = filtered_df[filtered_df["barrio"].isin(top_df["barrio"])].groupby(["barrio", "tipo_crimen"]).sum().reset_index()
    filtered_borough_df = filtered_df.groupby(["id_barrio", "barrio", "comuna", "zona", "estra_moda", "area"]).sum().reset_index()
    filtered_borough_df["text"] = "Borough: " + filtered_borough_df["barrio"] + \
        "<br />Commune: " + filtered_borough_df["comuna"].astype(str) + \
        "<br />Zone: " + filtered_borough_df["zona"] + \
        "<br />Socioeconomical Level: " + filtered_borough_df["estra_moda"].astype(str) + \
        "<br />Area: " + filtered_borough_df["area"].astype(str)

    map_figure = go.Figure(
        go.Choroplethmapbox(
            geojson = geojson,
            locations = filtered_borough_df["id_barrio"],
            z = filtered_borough_df["cantidad"],
            colorscale = "Viridis",
            marker_opacity = 0.5,
            marker_line_width=0.5,
            marker_line_color='gray',
            text = filtered_borough_df["text"]
        )
    ).update_layout(
        mapbox_style = "carto-positron",
        mapbox_zoom = 11,
        mapbox_center = {"lat": 3.420, "lon": -76.530},
        height = 700
    )

    bar_figure = px.bar(
        filtered_crime_df,
        x = "barrio",
        y = "cantidad",
        color = "tipo_crimen",
        height = 700,
        color_discrete_sequence = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
    ).update_xaxes(categoryorder = "total descending")

    return [map_figure, bar_figure]
