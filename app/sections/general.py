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
    borough_geojson = json.loads(geo.read())

with open('data/cali_comunas.geojson', encoding = "utf-8") as geo:
    commune_geojson = json.loads(geo.read())

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
base_df["year"] = base_df["fechahora"].dt.year
base_df["month"] = base_df["fechahora"].dt.month

year_min = base_df["year"].min()
year_max = base_df["year"].max()
zone_list = sorted(base_df["zona"].unique())
commune_list = sorted(base_df["comuna"].unique())
borough_list = sorted(base_df["barrio"].unique())
crime_list = sorted(base_df["tipo_crimen"].unique())

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
                        value = []
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
                lg = 3,
                sm = 12,
                className = "pr-5"
            ),
            dbc.Col([
                dcc.Loading(
                    type = "graph",
                    children = [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Graph(
                                        id="map-graph",
                                        figure = map_figure
                                    ),
                                    lg = 6,
                                    sm = 12
                                ),
                                dbc.Col(
                                    dcc.Graph(
                                        id="map-graph-2",
                                        figure = map_figure
                                    ),
                                    lg = 6,
                                    sm = 12
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Graph(
                                        id="bar-graph"
                                    ),
                                    lg = 6,
                                    sm = 12
                                ),
                                dbc.Col(
                                    dcc.Graph(
                                        id="bar-graph-2"
                                    ),
                                    lg = 6,
                                    sm = 12
                                )
                            ]
                        )
                    ]
                )
            ])
        ]
    )
])

@app.callback(
    [
        Output('map-graph', 'figure'),
        Output('bar-graph', 'figure'),
        Output('map-graph-2', 'figure'),
        Output('bar-graph-2', 'figure')
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
    filtered_df = base_df.copy()

    if (len(corregimientos) == 0):
        filtered_df = filtered_df[filtered_df["zona"] != "Corregimiento"]

    if (year):
        filtered_df = filtered_df[(filtered_df["year"] >= year[0]) & (filtered_df["year"] <= year[1])]

    if (month):
        filtered_df = filtered_df[(filtered_df["month"] >= month[0]) & (filtered_df["month"] <= month[1])]

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
    filtered_crime_commune_df = filtered_df.groupby (["comuna", "tipo_crimen"]).sum().reset_index()
    filtered_borough_df = filtered_df.groupby(["id_barrio", "barrio", "comuna", "zona", "estra_moda", "area"]).sum().reset_index()
    filtered_commune_df = filtered_df.groupby(["comuna", "zona", "estra_moda", "area"]).sum().reset_index()
    filtered_borough_df["text"] = "Borough: " + filtered_borough_df["barrio"] + \
        "<br />Commune: " + filtered_borough_df["comuna"].astype(str) + \
        "<br />Zone: " + filtered_borough_df["zona"] + \
        "<br />Socioeconomical Level: " + filtered_borough_df["estra_moda"].astype(str) + \
        "<br />Area: " + filtered_borough_df["area"].astype(str)
    filtered_commune_df["text"] = "Commune: " + filtered_borough_df["comuna"].astype(str) + \
        "<br />Zone: " + filtered_borough_df["zona"] + \
        "<br />Socioeconomical Level: " + filtered_borough_df["estra_moda"].astype(str) + \
        "<br />Area: " + filtered_borough_df["area"].astype(str)

    map_figure_1 = go.Figure(
        go.Choroplethmapbox(
            geojson = borough_geojson,
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
        height = 700,
        margin = dict(l = 0, r = 0, b = 0),
        title_text = 'Total Crimes per Borough'
    )

    map_figure_2 = go.Figure(
        go.Choroplethmapbox(
            geojson = commune_geojson,
            locations = filtered_borough_df["comuna"],
            z = filtered_borough_df["cantidad"],
            colorscale = "Viridis",
            marker_opacity = 0.5,
            marker_line_width=0.5,
            marker_line_color='gray',
            text = filtered_commune_df["text"]
        )
    ).update_layout(
        mapbox_style = "carto-positron",
        mapbox_zoom = 11,
        mapbox_center = {"lat": 3.420, "lon": -76.530},
        height = 700,
        margin = dict(l = 0, r = 0, b = 0),
        title_text = 'Total Crimes per Commune',
    )

    bar_figure_1 = px.bar(
        filtered_crime_df,
        x = "barrio",
        y = "cantidad",
        color = "tipo_crimen",
        height = 700,
        title = "Crimes per Borough",
        labels = {
            "barrio": "Borough",
            "cantidad": "Total",
            "tipo_crimen": "Type of crime"
        },
        color_discrete_sequence = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928"]
    ).update_xaxes(categoryorder = "total descending")

    filtered_crime_commune_df["label_comuna"] = filtered_crime_commune_df["comuna"].apply(lambda x: "Commune " + x)

    bar_figure_2 = px.bar(
        filtered_crime_commune_df,
        x = "label_comuna",
        y = "cantidad",
        color = "tipo_crimen",
        height = 700,
        title = "Crimes per Commune",
        labels = {
            "label_comuna": "Commune",
            "cantidad": "Total",
            "tipo_crimen": "Type of crime"
        },
        color_discrete_sequence = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928"]
    ).update_xaxes(type = "category", categoryorder = "total descending")\

    return [map_figure_1, bar_figure_1, map_figure_2, bar_figure_2]
