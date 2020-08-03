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
    SELECT      DATE_TIME,
                CRIME_TYPE,
                CRIME_CHAPTER,
                BOROUGH_ID,
                BOROUGH_NAME,
                BOROUGH_COMMUNE,
                BOROUGH_STRATUM,
                BOROUGH_ZONE,
                AGE_RANGE,
                SEX,
                REPLACE(EDUCATION, '-', 'NO APLICA') AS EDUCATION,
                QUANTITY
    FROM        TARGETING.VW_CRIMES_VICTIM_DATETIME
"""
base_df = pd.read_sql_query(query, con = engine)
base_df["year"] = base_df["date_time"].dt.year
base_df["month"] = base_df["date_time"].dt.month
base_df["day"] = base_df["date_time"].dt.dayofweek
base_df["day_name"] = base_df["date_time"].dt.day_name()
base_df["hour"] = base_df["date_time"].dt.hour
base_df["year_month"] = pd.to_datetime(base_df["year"].astype(str) + base_df["month"].astype(str), format = "%Y%m")

# Get from the dataframe the unique values from some columns that are going to be used as filters.
year_min = base_df["year"].min()
year_max = base_df["year"].max()
zone_list = sorted(base_df["borough_zone"].unique())
commune_list = sorted(base_df["borough_commune"].unique())
borough_list = sorted(base_df["borough_name"].unique())
crime_list = sorted(base_df["crime_type"].unique())

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
                                    [
                                        dcc.Graph(
                                            id="year-crime-line-graph"
                                        )
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id="day-hour-bar-graph"
                                        )
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id="age-graph"
                                        )
                                    ],
                                    lg = 6,
                                    sm = 12
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id="education-graph"
                                        )
                                    ],
                                    lg = 6,
                                    sm = 12
                                )
                            ]
                        ),
                        html.H3("Victims By Sex"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id="sex-chapter-1-graph"
                                        )
                                    ],
                                    lg = 6,
                                    sm = 12
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id="sex-chapter-2-graph"
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
                                            id="sex-chapter-3-graph"
                                        )
                                    ],
                                    lg = 6,
                                    sm = 12
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id="sex-chapter-4-graph"
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
                                            id="sex-chapter-5-graph"
                                        )
                                    ],
                                    width = {"size": 6, "offset": 3}
                                )
                            ]
                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.H3("One Of The Most Concerning Crime Increasing (Sexual Abuse)"),
                        html.Br(),
                        html.P(
                            children = [
                                " Image below left show the sexual abuse during 2019. Most cases of this type of crime occurred in commune 15, ",
                                " well known for its high demand of social interests housing and consolidation of moderately developed areas as ",
                                " well as another focus of sexual abuse  is the Downtown of Cali.  Additionally, image below right, shows how ",
                                " sexual abuse have been increasing during the last year, particularly 2017-2019, with many cases during the last ",
                                " year, while as clear the color as cases increases and vice versa."
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Img(src = "assets/criminal_activity_sexual_abuse_1.png", className = "column-picture")
                                    ],
                                    width = {"size": 5, "offset": 1}
                                    className = "text-center"
                                ),
                                dbc.Col(
                                    [
                                        html.Img(src = "assets/criminal_activity_sexual_abuse_2.png", className = "column-picture")
                                    ],
                                    lg = 5,
                                    className = "text-center"
                                )
                            ]
                        ),
                        html.P(
                            children = [
                                " Sexual abuse is increasing as we can observe in image below, where in blue line it shows the total cases (sexual abuse) ",
                                " by month throughout the years (2010-2019). Whilst the red line corresponds to moving average over 12 periods, showing an ",
                                " increased tendency during the last years. "
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Img(src = "assets/criminal_activity_sexual_abuse_3.png", className = "column-picture")
                                    ],
                                    width = {"size": 6, "offset": 3}
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
        Output('year-crime-line-graph', 'figure'),
        Output('day-hour-bar-graph', 'figure'),
        Output('age-graph', 'figure'),
        Output('education-graph', 'figure'),
        Output('sex-chapter-1-graph', 'figure'),
        Output('sex-chapter-2-graph', 'figure'),
        Output('sex-chapter-3-graph', 'figure'),
        Output('sex-chapter-4-graph', 'figure'),
        Output('sex-chapter-5-graph', 'figure'),
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
def update_graphs(year, month, zone, commune, borough, crime, corregimientos):
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

        # Get the dataframe grouped by year-month and crime_type.
    grouped_year_month_crime_df = filtered_df[["year_month", "crime_type", "quantity"]].groupby(["year_month", "crime_type"]).sum().reset_index()
    # Get the dataframe by grouped by month.
    grouped_month_df = filtered_df[["month", "quantity"]].groupby(["month"]).sum().reset_index()
    # Get the dataframe by grouped by month.
    grouped_day_hour_df = filtered_df[["day", "day_name", "hour", "quantity"]].groupby(["day", "day_name", "hour"]).sum().reset_index()
    # Get the dataframe by grouped by age_range.
    grouped_age_df = filtered_df[["age_range", "quantity"]].groupby(["age_range"]).sum().reset_index()
    # Get the dataframe by grouped by education.
    grouped_education_df = filtered_df[["education", "quantity"]].groupby(["education"]).sum().reset_index()
    # Get the dataframe by grouped by crime_chapter and sex.
    grouped_sex_chapter_df = filtered_df[filtered_df["sex"].isin(["MALE", "FEMALE"])][["year_month", "crime_chapter", "sex", "quantity"]].groupby(["year_month", "crime_chapter", "sex"]).sum().reset_index()


    # Define the list that will containg the traces for the graph by crime_type.
    base_data = []

    # Create a trace (frame) for each crime_type through the years.
    for crime_type in grouped_year_month_crime_df["crime_type"].unique():
        crime_type_df = grouped_year_month_crime_df[grouped_year_month_crime_df["crime_type"] == crime_type]

        base_data.append(
            go.Scatter(
                x = crime_type_df["year_month"],
                y = crime_type_df["quantity"],
                name = crime_type,
                mode = "lines"
            )
        )

    # Create the line graph with the total per crime_type per year.
    year_crime_line_figure = go.Figure(
        data = base_data,
        layout = {
            "height": 500,
            "title": "Crimes by Year-Month",
            "colorway": color_scale
        }
    )

    day_hour_bar_figure = go.Figure(
        layout = {
            "height": 500,
            "title": "Crimes by Day-Hour"
        }
    ).add_bar(
        x = [grouped_day_hour_df["day_name"], grouped_day_hour_df["hour"]],
        y = grouped_day_hour_df["quantity"],
    )

    age_bar_figure = go.Figure(
        data = [
            go.Bar (
                x = grouped_age_df["age_range"],
                y = grouped_age_df["quantity"],
                marker = {
                    "color": color_scale
                }
            )
        ],
        layout = {
            "title": "Victims by Age",
            "colorway": color_scale
        }
    )

    education_bar_figure = go.Figure(
        data = [
            go.Bar (
                x = grouped_education_df["education"],
                y = grouped_education_df["quantity"],
                marker = {
                    "color": color_scale
                }
            )
        ],
        layout = {
            "title": "Victims by Education",
        }
    )

    # Create the bar graph with the total crimes per month
    months_list = grouped_month_df["month"].unique()
    month_bar_figure = go.Figure(
        data = [
            go.Bar( x = grouped_month_df["month"], y = grouped_month_df["quantity"])
        ],
        layout = {
            "height": 700,
            "title": "Total Crimes by Month",
            "xaxis": {
                "tickvals": months_list,
                "ticktext": [calendar.month_abbr[month] for month in months_list]
            }
        }
    )

    sex_chapter_graphs_list = []

    for chapter in grouped_sex_chapter_df["crime_chapter"].unique():
        sex_chapter_graphs_list.append(
            px.line(
                grouped_sex_chapter_df[grouped_sex_chapter_df["crime_chapter"] == chapter],
                x = "year_month",
                y = "quantity",
                color = "sex",
                title = chapter
            )
        )

    return [year_crime_line_figure, day_hour_bar_figure, age_bar_figure, education_bar_figure] + sex_chapter_graphs_list
