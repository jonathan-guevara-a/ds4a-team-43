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

# Create database connection.
engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}", max_overflow = 20)

# Retrieve summarized information to display.
query = """
    SELECT      YEAR,
                CRIME_TYPE,
                BOROUGH_ID,
                BOROUGH_NAME,
                BOROUGH_COMMUNE,
                BOROUGH_STRATUM,
                BOROUGH_ZONE,
                TOTAL
    FROM        TARGETING.VW_CRIMES_YEAR
"""
base_df = pd.read_sql_query(query, con = engine)

# Get the dataframe by year.
grouped_year_df = base_df[["year", "total"]].groupby(["year"]).sum().reset_index()
# Get the dataframe by year and crime_type.
grouped_year_crime_df = base_df[["year", "crime_type", "total"]].groupby(["year", "crime_type"]).sum().reset_index()

# Get from the dataframe the extreme values to be used for the graphs.
year_min = grouped_year_df["year"].min()
year_max = grouped_year_df["year"].max()
total_min = grouped_year_df["total"].min()
total_max = grouped_year_df["total"].max()

# Create the line graph with the total per year.
year_line_figure = go.Figure(
    go.Scatter(
        x = grouped_year_df["year"],
        y = grouped_year_df["total"]
    ),
    layout = go.Layout(
        xaxis = {
            "range": [year_min - 1, year_max + 1],
            "autorange": False
        },
        yaxis = {
            "range": [0, total_max + 10000],
            "autorange": False
        },
        # Define the button that will trigger the graph animation.
        updatemenus = [
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None]
                    }
                ],
                "x": 0.57,
                "y": -0.1
            }
        ]
    ),
    # Define the frames for each year step.
    frames = [
        go.Frame(
            data = [
                go.Scatter(
                    x = grouped_year_df[grouped_year_df["year"] <= year]["year"],
                    y = grouped_year_df[grouped_year_df["year"] <= year]["total"]
                )
            ]
        )
        for year in range(year_min, year_max + 1)
    ]
)

# Get from the dataframe the extreme values to be used for the graphs.
year_min = grouped_year_crime_df["year"].min()
year_max = grouped_year_crime_df["year"].max()
count_min = grouped_year_crime_df["total"].min()
count_max = grouped_year_crime_df["total"].max()

# Define the list that will containg the frames for the graph by crime_type.
base_data = []
frames_data = []

# Create a trace (frame) for each crime_type through the years.
for crime_type in grouped_year_crime_df["crime_type"].unique():
    crime_type_df = grouped_year_crime_df[grouped_year_crime_df["crime_type"] == crime_type]

    base_data.append(
        go.Scatter(
            x = crime_type_df["year"],
            y = crime_type_df["total"],
            name = crime_type
        )
    )

# Create a trace (frame) for each crime_type for each year step.
for year in range(year_min, year_max + 1):
    frame_year_data = []

    for crime_type in grouped_year_crime_df["crime_type"].unique():
        crime_type_df = grouped_year_crime_df[
            (grouped_year_crime_df["crime_type"] == crime_type) &
            (grouped_year_crime_df["year"] <= year)
        ]

        frame_year_data.append(
            go.Scatter(
                x = crime_type_df["year"],
                y = crime_type_df["total"],
                name = crime_type
            )
        )

    frames_data.append(
        go.Frame (
            data = frame_year_data
        )
    )

# Create the line graph with the total per crime_type per year.
year_crime_line_figure = go.Figure(
    data = base_data,
    layout = go.Layout(
        xaxis = {
            "range": [year_min - 1, year_max + 1],
            "autorange": False
        },
        yaxis = {
            "range": [- (count_max * 0.1), count_max + 10000],
            "autorange": False
        },
        updatemenus = [
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None]
                    }
                ],
                "x": 0.57,
                "y": -0.1
            }
        ],
        colorway = color_scale
    ),
    frames = frames_data
)

# Define base layout using Bootstrap grid system.
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
