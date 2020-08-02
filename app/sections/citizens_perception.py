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

# Create database connection.
engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}", max_overflow = 20)

# Retrieve summarized information to display.
query = """
    SELECT      YEAR,
                AGE_RANGE,
                EDUCATION_CODE,
                EDUCATION,
                SOCIAL_STRATUM,
                INSECURE,
                SECURE,
                TOTAL
    FROM        TARGETING.VW_PERCEPTION_VARIABLES_YEAR
"""
base_df = pd.read_sql_query(query, con = engine)

# Get from the dataframe the unique values from some columns that are going to be used as filters.
year_min = base_df["year"].min()
year_max = base_df["year"].max()

# Define base layout using Bootstrap grid system.
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H3("Filters"),
                    html.Label("Year:"),
                    html.Br(),
                    dcc.Slider(
                        id = "year-slider",
                        dots = True,
                        min = year_min,
                        max = year_max,
                        value = year_max,
                        step = 1,
                        marks = {
                            i : {
                                "label": f"{i}",
                                "style": {"transform": "rotate(45deg)"}
                            } for i in range(year_min, (year_max + 1))
                        }
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
                                    [
                                        dcc.Graph(
                                            id = "perception-age-bar-graph"
                                        )
                                    ],
                                    lg = 5,
                                    sm = 12
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id = "perception-year-age-bar-graph"
                                        )
                                    ],
                                    lg = 7,
                                    sm = 12
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id = "perception-education-bar-graph"
                                        )
                                    ],
                                    lg = 5,
                                    sm = 12
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id = "perception-year-education-bar-graph"
                                        )
                                    ],
                                    lg = 7,
                                    sm = 12
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id = "perception-stratum-bar-graph"
                                        )
                                    ],
                                    lg = 5,
                                    sm = 12
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id = "perception-year-stratum-bar-graph"
                                        )
                                    ],
                                    lg = 7,
                                    sm = 12
                                ),
                            ]
                        ),
                    ]
                )
            ],
            lg = 9,
            sm = 12
            )
        ]
    )
])

# Define callback to update all graphs according to the user's filter selections.
@app.callback(
    [
        Output("perception-age-bar-graph", "figure"),
        Output("perception-year-age-bar-graph", "figure"),
        Output("perception-education-bar-graph", "figure"),
        Output("perception-year-education-bar-graph", "figure"),
        Output("perception-stratum-bar-graph", "figure"),
        Output("perception-year-stratum-bar-graph", "figure")
    ],
    [
        Input('year-slider', 'value')
    ]
)
def update_graphs(year):
    # Filter the base dataframe using the selected filters, if they have values.
    # Each filter is cumulative and has a hierarchy.
    filtered_df = base_df.copy()
    variables_list = ["age_range", "education", "social_stratum"]
    titles_list = ["Age Range", "Education Level", "Socioeconomical Level"]
    graphs_list = []

    if (year):
        filtered_df = filtered_df[
            filtered_df["year"] == year
        ]

    for i, variable in enumerate(variables_list):
        if variable == "education":
            variable_group_list = [variable + "_code", variable]
        else:
            variable_group_list = [variable]

        perception_variable_df = filtered_df.groupby(variable_group_list).sum().reset_index()
        perception_variable_df["insecure_percentage"] = round(perception_variable_df["insecure"] / perception_variable_df["total"] * 100, 2)
        perception_variable_df["secure_percentage"] = round(perception_variable_df["secure"] / perception_variable_df["total"] * 100, 2)

        perception_year_variable_df = base_df.groupby(["year"] + variable_group_list).sum().reset_index()
        perception_year_variable_df["insecure_percentage"] = round(perception_year_variable_df["insecure"] / perception_year_variable_df["total"] * 100, 2)
        perception_year_variable_df["secure_percentage"] = round(perception_year_variable_df["secure"] / perception_year_variable_df["total"] * 100, 2)

        graphs_list.append(
            go.Figure(
                data = [
                    go.Bar(
                        x = perception_variable_df[variable],
                        y = perception_variable_df["insecure_percentage"],
                        marker_color = "#fb9a99",
                        name = "% Insecure"
                    ),
                    go.Bar(
                        x = perception_variable_df[variable],
                        y = perception_variable_df["secure_percentage"],
                        marker_color = "#b2df8a",
                        name = "% Secure"
                    )
                ],
                layout = go.Layout(
                    barmode = "stack",
                    title = "Security Perception per " + titles_list[i],
                    xaxis_title = "Year " + str(year),
                    yaxis_title = "Percentage (%)"
                )
            )
        )

        graphs_list.append(
            go.Figure(
                layout = go.Layout(
                    barmode = "relative",
                    bargap = 0.3,
                    title = "Security Perception by Year",
                    xaxis_title = "Year / " + titles_list[i],
                    yaxis_title = "Percentage (%)"
                )
            ).add_bar(
                x = [perception_year_variable_df["year"], perception_year_variable_df[variable]],
                y = perception_year_variable_df["secure_percentage"],
                marker_color = "#b2df8a",
                name = "% Secure"
            ).add_bar(
                x = [perception_year_variable_df["year"], perception_year_variable_df[variable]],
                y = perception_year_variable_df["insecure_percentage"],
                marker_color = "#fb9a99",
                name = "% Insecure"
            )
        )

    return graphs_list
