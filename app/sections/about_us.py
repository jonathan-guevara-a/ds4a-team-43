import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

profiles_list = [
    {
        "name": "Luz Elena Thompson Pinzón",
        "description": """
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat.
        """,
        "picture": "luz.jpg"
    },
    {
        "name": "Maria Camila Manrique Nuñez",
        "description": """
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat.
        """,
        "picture": "camila.jpg"
    },
    {
        "name": "Daniel Gaitán Forero",
        "description": """
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat.
        """,
        "picture": "daniel.jpg"
    },
    {
        "name": "Fabio Andrés Sánchez Bernal",
        "description": """
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat.
        """,
        "picture": "fabio.jpg"
    },
    {
        "name": "Jhon Alexander Parra Jiménez",
        "description": """
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat.
        """,
        "picture": "jhon.jpg"
    },
    {
        "name": "Jonathan Guevara Agudelo",
        "description": """
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat.
        """,
        "picture": "jonathan.jpg"
    },
    {
        "name": "Chris Earle",
        "description": """
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat.
        """,
        "picture": "ta-chris.jpg"
    },
    {
        "name": "Daniel Gil",
        "description": """
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat.
        """,
        "picture": "ta-daniel.jpg"
    },
    {
        "name": "Natesh Pillai",
        "description": """
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat.
        """,
        "picture": "natesh.jpg"
    }
]

profiles_html_list = []

for profile in profiles_list:
    profiles_html_list.append(
        dbc.Col(
            children = [
                dbc.Row(
                    children = [
                        dbc.Col(
                            children = [
                                html.Img(src = "assets/{}".format(profile["picture"]), className = "profile-picture")
                            ],
                            width = {"size": 3},
                            className = "text-center"
                        ),
                        dbc.Col(
                            children = [
                                html.H4(profile["name"]),
                                html.P(profile["description"])
                            ]
                        )
                    ],
                    className = "d-flex flex-wrap align-items-center"
                )
            ],
            width = {"size": 6},
            className = "p-3 mb-5"
        )
    )


layout = html.Div(
    children = [
        dbc.Row(
            children = [
                dbc.Col(
                    children = [
                        html.Br(),
                        html.H2("Team 43")
                    ],
                    className = "text-center"
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            children = [
                profiles_html_list[0],
                profiles_html_list[1]
            ]
        ),
        dbc.Row(
            children = [
                profiles_html_list[2],
                profiles_html_list[3]
            ]
        ),
        dbc.Row(
            children = [
                profiles_html_list[4],
                profiles_html_list[5]
            ]
        ),
        dbc.Row(
            children = [
                dbc.Col(
                    children = [
                        html.H2("Special Thanks"),
                        html.Br()
                    ],
                    className = "text-center"
                )
            ]
        ),
        dbc.Row(
            children = [
                profiles_html_list[6],
                profiles_html_list[7]
            ]
        ),
        dbc.Row(
            children = [
                dbc.Col(width={"size": 3}),
                profiles_html_list[8]
            ]
        )
    ]
)


