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
                MONTH,
                COMMUNE,
                SEX,
                CRIME_TYPE,
                VALUE
    FROM        TARGETING.VW_FORECAST_CRIMES
"""
base_df = pd.read_sql_query(query, con = engine)
base_df["year_month"] = pd.to_datetime(base_df["year"].astype(str) + base_df["month"].astype(str), format = "%Y%m")
commune_list = base_df["commune"].unique()
color_scale = ["#1f78b4", "#33a02c", "#e31a1c", "#6a3d9a", "#ff7f00", "#b15928"]

# Define base layout using Bootstrap grid system.
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H3("Filters"),
                    html.Label("Commune:"),
                    html.Br(),
                    dcc.Dropdown(
                        id = "commune-dropdown",
                        options = [
                            {"label": f"Commune {i}", "value": i} for i in list(commune_list) + [": All"] if i != None
                        ],
                        value = ": All"
                    ),
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
                                            id = "forecast-crime-type-line-graph"
                                        )
                                    ]
                                )
                            ]
                        ),
                        html.H3("Forecast By Sex"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id = "sex-forecast-chapter-1-graph"
                                        )
                                    ],
                                    lg = 6,
                                    sm = 12
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id = "sex-forecast-chapter-2-graph"
                                        )
                                    ],
                                    lg = 6,
                                    sm = 12
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id = "sex-forecast-chapter-3-graph"
                                        )
                                    ],
                                    lg = 6,
                                    sm = 12
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id = "sex-forecast-chapter-4-graph"
                                        )
                                    ],
                                    lg = 6,
                                    sm = 12
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id = "sex-forecast-chapter-5-graph"
                                        )
                                    ],
                                    lg = 6,
                                    sm = 12
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id = "sex-forecast-chapter-6-graph"
                                        )
                                    ],
                                    lg = 6,
                                    sm = 12
                                )
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
        Output("forecast-crime-type-line-graph", "figure"),
        Output("sex-forecast-chapter-1-graph", "figure"),
        Output("sex-forecast-chapter-2-graph", "figure"),
        Output("sex-forecast-chapter-3-graph", "figure"),
        Output("sex-forecast-chapter-4-graph", "figure"),
        Output("sex-forecast-chapter-5-graph", "figure"),
        Output("sex-forecast-chapter-6-graph", "figure")
    ],
    [
        Input('commune-dropdown', 'value')
    ]
)
def update_graphs(commune):
    graphs_list = []

    # Filter the base dataframe using the selected filters, if they have values.
    # Each filter is cumulative and has a hierarchy.
    filtered_df = base_df.copy()

    if (commune and commune != ": All"):
        filtered_df = filtered_df[
            filtered_df["commune"] == commune
        ]

    traces_list = []

    for i, crime_type in enumerate(filtered_df["crime_type"].unique()):
        forecasting_current_df = filtered_df[
            (filtered_df["year"] == 2019) & (filtered_df["crime_type"] == crime_type)
        ]
        forecasting_future_df = filtered_df[
            (filtered_df["year"] == 2020) & (filtered_df["crime_type"] == crime_type)
        ]

        forecasting_current_grouped_df = forecasting_current_df.groupby(["year_month"]).sum().reset_index()
        forecasting_future_grouped_df = forecasting_future_df.groupby(["year_month"]).sum().reset_index()

        traces_list.append(
            go.Scatter(
                x = forecasting_current_grouped_df["year_month"].append(
                    pd.Series(forecasting_future_grouped_df["year_month"][0])
                ),
                y = forecasting_current_grouped_df["value"].append(
                    pd.Series(forecasting_future_grouped_df["value"][0])
                ),
                line = {
                    "color": color_scale[i]
                },
                name = crime_type + " (Current)",
                legendgroup = crime_type
            )
        )

        traces_list.append(
            go.Scatter(
                x = forecasting_future_grouped_df["year_month"],
                y = forecasting_future_grouped_df["value"],
                line = {
                    "dash": "dot",
                    "color": color_scale[i]
                },
                name = crime_type + " (Forecast)",
                legendgroup = crime_type
            )
        )

    graphs_list.append(
        go.Figure(
            data = traces_list,
            layout = {
                "height": 800,
                "legend": {
                    "yanchor": "top",
                    "y": -0.1,
                    "xanchor": "left",
                    "x": 0
                }
            }
        )
    )


    for crime_type in filtered_df["crime_type"].unique():
        traces_list = []

        forecasting_current_df = filtered_df[
            (filtered_df["year"] == 2019) & (filtered_df["crime_type"] == crime_type)
        ]
        forecasting_future_df = filtered_df[
            (filtered_df["year"] == 2020) & (filtered_df["crime_type"] == crime_type)
        ]

        forecasting_current_grouped_df = forecasting_current_df.groupby(["year_month", "sex"]).sum().reset_index()
        forecasting_future_grouped_df = forecasting_future_df.groupby(["year_month", "sex"]).sum().reset_index()

        for i, sex in enumerate(filtered_df["sex"].unique()):
            forecasting_current_sex_df = forecasting_current_grouped_df[
                forecasting_current_grouped_df["sex"] == sex
            ].reset_index()
            forecasting_future_sex_df = forecasting_future_grouped_df[
                forecasting_future_grouped_df["sex"] == sex
            ].reset_index()

            if (forecasting_current_sex_df.shape[0] == 0) or (forecasting_future_sex_df.shape[0] == 0):
                continue

            traces_list.append(
                go.Scatter(
                    x = forecasting_current_sex_df["year_month"].append(
                        pd.Series(forecasting_future_sex_df["year_month"][0])
                    ),
                    y = forecasting_current_sex_df["value"].append(
                        pd.Series(forecasting_future_sex_df["value"][0])
                    ),
                    line = {
                        "color": color_scale[i]
                    },
                    name = sex + " (Current)",
                    legendgroup = sex
                )
            )

            traces_list.append(
                go.Scatter(
                    x = forecasting_future_sex_df["year_month"],
                    y = forecasting_future_sex_df["value"],
                    line = {
                        "dash": "dot",
                        "color": color_scale[i]
                    },
                    name = sex + " (Forecast)",
                    legendgroup = sex
                )
            )

        graphs_list.append(
            go.Figure(
                data = traces_list,
                layout = {
                    "title": crime_type,
                    "legend": {
                        "yanchor": "top",
                        "y": -0.1,
                        "xanchor": "left",
                        "x": 0
                    }
                }
            )
        )

    return graphs_list
