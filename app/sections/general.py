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

# Read database parameters.
file = open("secure/database.txt", "r")
lines = file.readlines()
DB_HOST = lines[0].rstrip()
DB_NAME = lines[1].rstrip()
DB_USERNAME = lines[2].rstrip()
DB_PASSWORD = lines[3].rstrip()
file.close()

# Define base color scale for all graphs.
color_scale = [
    "#a6cee3",
    "#1f78b4",
    "#b2df8a",
    "#33a02c",
    "#fb9a99",
    "#e31a1c",
    "#fdbf6f",
    "#ff7f00",
    "#cab2d6",
    "#6a3d9a",
    "#ffff99",
    "#b15928"
]

# Read geojson files to be used in choropleth maps.
with open('data/cali_barrios.geojson', encoding = "utf-8") as geo:
    borough_geojson = json.loads(geo.read())

with open('data/cali_comunas.geojson', encoding = "utf-8") as geo:
    commune_geojson = json.loads(geo.read())

# Filter out the "corregimientos" in order to add a layer to the boroughs map.
base_commune_geojson = commune_geojson.copy()
base_commune_geojson["features"] = [feature for feature in base_commune_geojson["features"] if "mc_corregimientos" not in feature["properties"]["id_comuna"]]

# Create database connection.
engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}", max_overflow = 20)

# Retrieve summarized information to display.
query = """
    SELECT      YEAR,
                MONTH,
                CRIME_TYPE,
                BOROUGH_ID,
                BOROUGH_NAME,
                BOROUGH_COMMUNE,
                BOROUGH_STRATUM,
                BOROUGH_ZONE,
                TOTAL
    FROM        TARGETING.VW_CRIMES_YEAR_MONTH
"""
base_df = pd.read_sql_query(query, con = engine)

# Get from the dataframe the unique values from some columns that are going to be used as filters.
year_min = base_df["year"].min()
year_max = base_df["year"].max()
zone_list = sorted(base_df["borough_zone"].unique())
commune_list = sorted(base_df["borough_commune"].unique())
borough_list = sorted(base_df["borough_name"].unique())
crime_list = sorted(base_df["crime_type"].unique())

# Create an empty map to be displayed at start up.
map_figure = go.Figure(
    go.Choroplethmapbox(),
    layout = {
        "mapbox_style": "carto-positron",
        "mapbox_zoom": 11,
        "mapbox_center": {"lat": 3.420, "lon": -76.530},
        "height": 700,
        "margin": {
            "l": 0,
            "r": 0,
            "b": 0
        }
    }
)

# Define base layout using Bootstrap grid system.
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
                            i : {
                                "label": f"{i}",
                                "style": {"transform": "rotate(45deg)"}
                            } for i in range(year_min, (year_max + 1))
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
                            i : {
                                "label": f"{calendar.month_abbr[i]}",
                                "style": {"transform": "rotate(45deg)"}
                            } for i in range(1, 13)
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
                        id = "crime-type-dropdown",
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
                                    )
                                )
                            ]
                        )
                    ]
                )
            ],
            lg = 9,
            sm = 12)
        ]
    )
])

# Define callback to update all graphs according to the user's filter selections.
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
        Input('crime-type-dropdown', 'value'),
        Input('corregimientos-check', 'value')
    ]
)
def update_map(year, month, zone, commune, borough, crime, corregimientos):
    # Filter the base dataframe using the selected filters, if they have values.
    # Each filter is cumulative and has a hierarchy.
    filtered_df = base_df.copy()

    if (len(corregimientos) == 0):
        filtered_df = filtered_df[filtered_df["borough_zone"] != "Corregimiento"]

    if (year):
        filtered_df = filtered_df[
            (filtered_df["year"] >= year[0]) &
            (filtered_df["year"] <= year[1])
        ]

    if (month):
        filtered_df = filtered_df[
            (filtered_df["month"] >= month[0]) &
            (filtered_df["month"] <= month[1])
        ]

    if (zone):
        filtered_df = filtered_df[filtered_df["borough_zone"].isin(zone)]

    if (commune):
        filtered_df = filtered_df[filtered_df["borough_commune"].isin(commune)]

    if (borough):
        filtered_df = filtered_df[filtered_df["borough_name"].isin(borough)]

    if (crime):
        filtered_df = filtered_df[filtered_df["crime_type"].isin(crime)]

    # Get the boroughs with the most crimes.
    top_df = filtered_df[["borough_name", "total"]].groupby("borough_name").sum()\
        .sort_values(by = "total", ascending = False).reset_index().head(50)
    # Group the filtered df by borough_name and crime_type. This is used for the bar graph.
    filtered_crime_df = filtered_df[filtered_df["borough_name"].isin(top_df["borough_name"])]\
        .groupby(["borough_name", "crime_type"]).sum().reset_index()
    # Group the filtered df by borough_commune and crime_type (This is temporary). This is used for the bar graph.
    filtered_crime_commune_df = filtered_df.groupby (["borough_commune", "crime_type"]).sum().reset_index()
    # Group the filtered df by borough. This is used for the choropleth map.
    filtered_borough_df = filtered_df.groupby(
        ["borough_id", "borough_name", "borough_commune", "borough_zone", "borough_stratum"]
    ).sum().reset_index()
    # Group the filtered  df by borough_commune. This is used for the choropleth map.
    filtered_commune_df = filtered_df.groupby(["borough_commune", "borough_zone", "borough_stratum"]).sum().reset_index()
    # Define the borough data that will be displayed on the choropleth map when the user hovers on each polygon.
    filtered_borough_df["text"] = "Borough: " + filtered_borough_df["borough_name"] + \
        "<br />Commune: " + filtered_borough_df["borough_commune"].astype(str) + \
        "<br />Zone: " + filtered_borough_df["borough_zone"] + \
        "<br />Socioeconomical Level: " + filtered_borough_df["borough_stratum"].astype(str)
    # Define the commune data that will be displayed on the choropleth map when the user hovers on each polygon.
    filtered_commune_df["text"] = "Commune: " + filtered_borough_df["borough_commune"].astype(str) + \
        "<br />Zone: " + filtered_borough_df["borough_zone"] + \
        "<br />Socioeconomical Level: " + filtered_borough_df["borough_stratum"].astype(str)

    # Update the map with the new data.
    map_figure_1 = go.Figure(
        data = [
            go.Choroplethmapbox(
                geojson = borough_geojson,
                locations = filtered_borough_df["borough_id"],
                z = filtered_borough_df["total"],
                colorscale = "Viridis",
                marker_opacity = 0.5,
                marker_line_width=0.5,
                marker_line_color='gray',
                text = filtered_borough_df["text"]
            )
        ],
            layout = {
            "mapbox_style": "carto-positron",
            "mapbox_zoom": 11,
            "mapbox_center": {"lat": 3.420, "lon": -76.530},
            "mapbox_layers": [
                {
                    "sourcetype": "geojson",
                    "source": base_commune_geojson,
                    "type": "line",
                    "maxzoom": 13
                }
            ],
            "height": 700,
            "margin": {
                "l": 0,
                "r": 0,
                "b": 0
            }
        }
    )

    # Update the map with the new data.
    map_figure_2 = go.Figure(
        go.Choroplethmapbox(
            geojson = commune_geojson,
            locations = filtered_borough_df["borough_commune"],
            z = filtered_borough_df["total"],
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

    # Update the bar graph with the new data.
    bar_figure_1 = px.bar(
        filtered_crime_df,
        x = "borough_name",
        y = "total",
        color = "crime_type",
        height = 700,
        title = "Crimes per Borough",
        labels = {
            "borough_name": "Borough",
            "total": "Total",
            "crime_type": "Type of crime"
        },
        color_discrete_sequence = color_scale
    ).update_xaxes(categoryorder = "total descending")

    # Create a new columns with a longer name for the commune.
    filtered_crime_commune_df["commune_name"] = filtered_crime_commune_df["borough_commune"].apply(
        lambda x: "Commune " + x
    )

    # Update the bar graph with the new data.
    bar_figure_2 = px.bar(
        filtered_crime_commune_df,
        x = "commune_name",
        y = "total",
        color = "crime_type",
        height = 700,
        title = "Crimes per Commune",
        labels = {
            "commune_name": "Commune",
            "total": "Total",
            "crime_type": "Type of crime"
        },
        color_discrete_sequence = color_scale
    ).update_xaxes(type = "category", categoryorder = "total descending")

    # Return the figures to update.
    return [map_figure_1, bar_figure_1, map_figure_2, bar_figure_2]
