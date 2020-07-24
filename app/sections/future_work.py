import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

activites_list = [
    {
        "title": "Lorem ipsum dolor sit amet",
        "description": """
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
            cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
            proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """,
        "picture": "graph_1.png"
    },
    {
        "title": "Lorem ipsum dolor sit amet",
        "description": """
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
            cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
            proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """,
        "picture": "graph_2.png"
    },
    {
        "title": "Lorem ipsum dolor sit amet",
        "description": """
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
            cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
            proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """,
        "picture": "graph_3.png"
    },
]

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
                                html.H4(activity["title"]),
                                html.P(activity["description"])
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
