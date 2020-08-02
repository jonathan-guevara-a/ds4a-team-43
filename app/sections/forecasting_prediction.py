import json
import calendar
import pandas as pd
import joblib
import os
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
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

query = """
    SELECT      *
    FROM        CALI.TOTAL_FORECAST
"""
forecast_df = pd.read_sql_query(query, con = engine)
forecast_df["comuna"] = forecast_df["comuna"].astype(str)
forecast_df = forecast_df.drop(columns=["anio"])
forecast_df = forecast_df.rename(
    columns = {
        "asx": "ASX",
        "hom": "HOM",
        "hur": "HUR",
        "lep": "LEP",
        "ter": "TER",
        "hur_otros": "HUR_OTROS",
        "c_asx": "C_ASX",
        "c_hom": "C_HOM",
        "c_hur": "C_HUR",
        "c_lep": "C_LEP",
        "c_ter": "C_TER"
    }
)
forecast_df["HUR_TOTAL"] = forecast_df["HUR"] + forecast_df["HUR_OTROS"]

base_df["year_month"] = pd.to_datetime(base_df["year"].astype(str) + base_df["month"].astype(str), format = "%Y%m")
commune_list = base_df["commune"].unique()
color_scale = ["#1f78b4", "#33a02c", "#e31a1c", "#6a3d9a", "#ff7f00", "#b15928"]

labels = ["security", "insecurity"]
pesimistic = [0.686794, 0.313206]
base = [0.730697, 0.269303]
optimistic = [0.786205, 0.213795]
scenarios_list = [pesimistic, base, optimistic]
scenarios_titles_list = ["Pesimistic Scenario", "Baseline Prediction", "Optimistic Scenario"]
pie_graphs_list = []

for i, scenario in enumerate(scenarios_list):
    pie_graphs_list.append(
        go.Figure(
            data = {
               "values": scenario,
               "labels": labels,
               "textinfo": "none",
               "hoverinfo": "label+percent+name",
               "hole": 0.6,
               "type": "pie",
               "marker": {
                    "colors": [
                        "rgb(60,179,113)",
                        "rgb(255, 255, 255)"
                    ]
                }
            },
            layout = {
                "showlegend" : False,
                "annotations": [
                    {
                        "font": {"size": 20},
                        "showarrow": False,
                        "text": scenarios_titles_list[i],
                        "x": 0.50,
                        "y": 1.2
                     },
                    {
                        "font": {"size": 20},
                        "showarrow": False,
                        "text": str(round(scenario[0] * 100,2)) + "%",
                        "x": 0.50,
                        "y": 0.50
                     }
                ]
            }
        )
    )

# Define base layout using Bootstrap grid system.
layout = html.Div([
    html.Br(),
    html.H2("Forecasting", className = "text-center"),
    html.Br(),
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
                        )
                    ]
                )
            ],
            lg = 9,
            sm = 12
            )
        ]
    ),
    html.Br(),
    html.H2("Prediction", className = "text-center"),
    html.Br(),
    dbc.Row(
        children = [
            dbc.Col(
                children = [
                    html.P(
                        children = [
                            "According to historic data and the security perception behavior in Cali, we have estimated that the percentage of citizens for 2020 that feel secure in the city will be around ",
                            html.B("73.07%"),
                            ", with an expected minimum of ",
                            html.B("68.68%"),
                            " and an expected maximum of ",
                             html.B("78.62%.")
                        ],
                        className = "text-center"
                    ),
                    html.Br(),
                    html.H3("Prediction of Security Perception 2020", className = "text-center"),
                    dbc.Row(
                        children = [
                            dbc.Col(
                                children = [dcc.Graph(id = "prediction-1-pie-graph", figure = pie_graphs_list[0])],
                                sm = 4,
                                className = "p-0"
                            ),
                            dbc.Col(
                                children = [dcc.Graph(id = "prediction-2-pie-graph", figure = pie_graphs_list[1])],
                                sm = 4,
                                className = "p-0"
                            ),
                            dbc.Col(
                                children = [dcc.Graph(id = "prediction-3-pie-graph", figure = pie_graphs_list[2])],
                                sm = 4,
                                className = "p-0"
                            )
                        ]
                    ),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.P(
                        children = [
                            "Would you like to know your security perception score? where ",
                            html.B("100 is completely secure"),
                            " and ",
                            html.B("0 is completely insecure"),
                            ". If so, please answer the following survey and then press the ",
                            html.B("Calculate"),
                            " button."
                        ],
                        className = "text-center"
                    ),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dbc.Row(
                        children = [
                            dbc.Col(
                                children = [
                                    html.Label("Commune:"),
                                    html.Br(),
                                    dcc.Dropdown(
                                        id = "commune-prediction-dropdown",
                                        options = [
                                            {"label": f"Commune {str(i).zfill(2)}", "value": i} for i in range(1, 23)
                                        ]
                                    ),
                                    html.Br(),
                                    html.Label("Sex:"),
                                    html.Br(),
                                    dcc.Dropdown(
                                        id = "sex-prediction-dropdown",
                                        options = [
                                            {"label": "FEMALE", "value": "FEMENINO"},
                                            {"label": "MALE", "value": "MASCULINO"}
                                        ]
                                    ),
                                    html.Br(),
                                    html.Label("Age Range:"),
                                    html.Br(),
                                    dcc.Dropdown(
                                        id = "age-range-prediction-dropdown",
                                        options = [
                                            {"label": str(i).replace("Más de 90", "90+"), "value": f"{i}"} for i in ["10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "Más de 90"]
                                        ]
                                    ),
                                    html.Br(),
                                    html.Label("Do you think that corruption levels have changed in the last year in Cali? (1 - Not Agree, 5 - Completely Agree):"),
                                    html.Br(),
                                    dcc.Dropdown(
                                        id = "corruption-prediction-dropdown",
                                        options = [
                                            {"label": i, "value": i} for i in range(1, 6)
                                        ]
                                    ),
                                    html.Br(),
                                    html.Label("What do you think is the probability of receiving a punishment for committing a crime in your city? (1 - Low, 5 High):"),
                                    html.Br(),
                                    dcc.Dropdown(
                                        id = "punity-prediction-dropdown",
                                        options = [
                                            {"label": i, "value": i} for i in range(1, 6)
                                        ]
                                    ),
                                    html.Br(),
                                    html.Label("What is your satisfaction level about your borough? (1 - Not Satisfied, 5 - Highly Satisfied):"),
                                    html.Br(),
                                    dcc.Dropdown(
                                        id = "satisfaction-borough-prediction-dropdown",
                                        options = [
                                            {"label": i, "value": i} for i in range(1, 6)
                                        ]
                                    ),
                                    html.Br(),
                                    html.Label("What is your satisfaction level about your city? (1 - Not Satisfied, 5 - Highly Satisfied):"),
                                    html.Br(),
                                    dcc.Dropdown(
                                        id = "satisfaction-city-prediction-dropdown",
                                        options = [
                                            {"label": i, "value": i} for i in range(1, 6)
                                        ]
                                    ),
                                    html.Br(),
                                    html.Label("What is your satisfaction level about the work done by your Mayor? (1 - Not Satisfied, 5 - Highly Satisfied):"),
                                    html.Br(),
                                    dcc.Dropdown(
                                        id = "mayor-perception-prediction-dropdown",
                                        options = [
                                            {"label": i, "value": i} for i in range(1, 6)
                                        ]
                                    ),
                                    html.Br(),
                                    html.Label("How secure do you feel in your borough? (1 - Not Secure, 5 Highly Secure):"),
                                    html.Br(),
                                    dcc.Dropdown(
                                        id = "borough-security-prediction-dropdown",
                                        options = [
                                            {"label": i, "value": i} for i in range(1, 6)
                                        ]
                                    ),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Br()
                                ],
                                lg = 8,
                                sm = 12
                            ),
                            dbc.Col(
                                children = [
                                    dbc.Button("Predict", id = "predict-button", size="lg", color = "success", n_clicks = 0),
                                    html.P(html.H3("", id = "predict-output"))
                                ],
                                lg = 4,
                                sm = 12,
                                className = "text-center"
                            )
                        ]
                    )
                ],
                width = {"size": 10, "offset": 1}
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

@app.callback(
    Output("predict-output", "children"),
    [Input("predict-button", "n_clicks")],
    [
        State("commune-prediction-dropdown", "value"),
        State("sex-prediction-dropdown", "value"),
        State("age-range-prediction-dropdown", "value"),
        State("corruption-prediction-dropdown", "value"),
        State("punity-prediction-dropdown", "value"),
        State("satisfaction-borough-prediction-dropdown", "value"),
        State("satisfaction-city-prediction-dropdown", "value"),
        State("mayor-perception-prediction-dropdown", "value"),
        State("borough-security-prediction-dropdown", "value"),
    ]
)
def calculate_prediction(n_clicks, commune, sex, age_range, corruption, punity, satisfaction_borough, satisfaction_city, perception_mayor, borough_security):
    if n_clicks == 0:
        return ""

    if (commune is None or sex is None or age_range is None or corruption is None or punity is None or satisfaction_borough is None or satisfaction_city is None or perception_mayor is None or borough_security is None):
        return [html.Br(), html.Br(), html.B("Please answer all the questions.")]

    dict_input = {}
    dict_input["comuna"] = str(commune)
    dict_input["sexo"] = sex
    dict_input["rango_edad"] = age_range
    dict_input["corrupcion_bin"] = corruption
    dict_input["punidad_bin"] = punity
    dict_input["satisfaccion_barrio_bin"] = satisfaction_borough
    dict_input["satisfaccion_ciudad_bin"] = satisfaction_city
    dict_input["percepcion_alcalde_bin"] = perception_mayor
    dict_input["seguridad_barrio_bin"] = borough_security

    dict_input["corrupcion_bin"] = np.where(dict_input["corrupcion_bin"] < 3, 0, 1)
    dict_input["punidad_bin"] = np.where(dict_input["punidad_bin"] < 3, 0, 1)
    dict_input["satisfaccion_barrio_bin"] = np.where(dict_input["satisfaccion_barrio_bin"] < 3, 0, 1)
    dict_input["satisfaccion_ciudad_bin"] = np.where(dict_input["satisfaccion_ciudad_bin"] < 3, 0, 1)
    dict_input["percepcion_alcalde_bin"] = np.where(dict_input["percepcion_alcalde_bin"] < 3, 0, 1)
    dict_input["seguridad_barrio_bin"] = np.where(dict_input["seguridad_barrio_bin"] < 3, 0, 1)

    input_df = pd.DataFrame(dict_input,index=[0])

    input_df = pd.merge(input_df, forecast_df, on = ["comuna", "sexo"], how = "left")

    input_df = input_df.drop(columns = ["sexo"])
    input_df["comuna"] = pd.Categorical(input_df["comuna"],categories=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22"])
    input_df["rango_edad"] = pd.Categorical(input_df["comuna"],categories=["10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "Más de 90"])

    input_df = pd.get_dummies(input_df, columns=["comuna", "rango_edad"], drop_first = True)

    logistic_model = joblib.load("data/logistic_prediction1.pkl")

    cols_logistic = ["seguridad_barrio_bin", "punidad_bin", "satisfaccion_barrio_bin","satisfaccion_ciudad_bin","corrupcion_bin", "percepcion_alcalde_bin","ASX", "HUR_TOTAL", "LEP",
                     "TER", "C_HOM", "C_HUR", "C_LEP", "comuna_2", "comuna_3", "comuna_4","comuna_5", "comuna_6", "comuna_7", "comuna_8", "comuna_9", "comuna_10",
                     "comuna_11", "comuna_12", "comuna_13", "comuna_14", "comuna_15","comuna_16", "comuna_17", "comuna_18", "comuna_19", "comuna_20","comuna_21", "comuna_22",
                     "rango_edad_20-29","rango_edad_30-39", "rango_edad_40-49", "rango_edad_50-59","rango_edad_60-69", "rango_edad_70-79", "rango_edad_80-89","rango_edad_Más de 90"]

    security_rate = logistic_model.predict_proba(input_df[cols_logistic])[:,1]

    return [
        html.Br(),
        html.Br(),
        html.P(
            children = [
                "Your security score is: ",
                round(security_rate[0] * 100, 2)
            ]
        )
    ]
