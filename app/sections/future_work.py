import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Define list with information about the future work: title, description and picture to show.
activites_list = [
    {
        "title": "Lorem ipsum dolor sit amet",
        "description": [
            "Incorporate XGBoost predictive model into the website.",
"            Development and interpretation of a Causal Analysis Model, to identify the causal relationship between people's perception of security and actual criminal activity."
        ],
        "picture": "graph_1.png"
    },
    {
        "title": "Lorem ipsum dolor sit amet",
        "description": [
            "Capture the person's actual score of security perception, to allow the model to continue learning.",
            "Attach this work with Chispa for further dissemination."
        ],
        "picture": "graph_2.png"
    },
    {
        "title": "Lorem ipsum dolor sit amet",
        "description": [
            "Make this work available in Spanish for access to citizenship.",
            "Continue the analysis for 2020 - in the hope of having all the details of the data again - and make an analysis of the impact of COVID-19 on criminal activity and the perception of the people of Cali.",
            "Generate this development for other municipalities in Colombia."
        ],
        "picture": "graph_3.png"
    },
]

# Transform each activity group into a Dash component in order to be visualized.
activities_html_list = []

for i, activity in enumerate(activites_list):
    width = {"size": 6}

    if (i % 2 != 0):
        width["offset"] = 6

    activities_html_list.append(
        dbc.Col(
            children = [
                dbc.Row(
                    children = [
                        dbc.Col(
                            children = [
                                html.Img(src = "assets/{}".format(activity["picture"]), className = "activity-picture")
                            ],
                            width = {"size": 3},
                            className = "text-center"
                        ),
                        dbc.Col(
                            children = [
                                html.Ul([html.Li(element) for element in activity["description"]])
                            ]
                        )
                    ],
                    className = "d-flex flex-wrap align-items-center"
                )
            ],
            width = width,
            className = "p-3 mb-5"
        )
    )

# Define base layout using Bootstrap grid system.
layout = html.Div(
    children = [
        html.Br(),
        html.Br(),
        dbc.Row(
            children = [
                activities_html_list[0]
            ]
        ),
        dbc.Row(
            children = [
                activities_html_list[1]
            ]
        ),
        dbc.Row(
            children = [
                activities_html_list[2]
            ]
        )
    ]
)
