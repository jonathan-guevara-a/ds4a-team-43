import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Define list with information about the team members and special thanks entities: name, description and picture to show.
profiles_list = [
    {
        "name": "Luz Elena Thompson Pinzón",
        "description": [
            "Computer Systems Engineer.",
            "22 years of experience working with Business Intelligence.",
            "Currently working as an architect and analytics leader."
        ],
        "picture": "luz.jpg"
    },
    {
        "name": "Maria Camila Manrique Nuñez",
        "description": [
            "Industrial Engineer.",
            "Master Degree in Industrial Engineering.",
            "Currently working in Business Intelligence."
        ],
        "picture": "camila.jpg"
    },
    {
        "name": "Daniel Gaitán Forero",
        "description": [
            "Electronic Engineer.",
            "Master degree in Engineering.",
            "Currently working as a Data Scientist / Data Engineer."
        ],
        "picture": "daniel.jpg"
    },
    {
        "name": "Fabio Andrés Sánchez Bernal",
        "description": [
            "Production Engineer.",
            "Currently working in Business Analytics."
        ],
        "picture": "fabio.jpg"
    },
    {
        "name": "Jhon Alexander Parra Jiménez",
        "description": [
            "Industrial Engineer.",
            "Currently doing his master degree in Analytics.",
            "Has worked with risk analytics and information security."
        ],
        "picture": "jhon.jpg"
    },
    {
        "name": "Jonathan Guevara Agudelo",
        "description": [
            "Computer Systems Engineer.",
            "Currently working as a Software Developer and Consultant."
        ],
        "picture": "jonathan.jpg"
    },
    {
        "name": "Chris Earle",
        "description": [
            "Skilled in statistical/econometric analysis.",
            "Founder of consultancy in business analytics."
        ],
        "picture": "ta-chris.jpg"
    },
    {
        "name": "Daniel Gil",
        "description": [
            "Statistician.",
            "Master degree in Statistics."
        ],
        "picture": "ta-daniel.jpg"
    },
    {
        "name": "Natesh Pillai",
        "description": [
            "Tenured Professor, Harvard University.",
            "Chief scientist at Correlation One.",
            "PhD in Statistics."
        ],
        "picture": "natesh.jpg"
    },
    {
        "name": "Chispa",
        "description": [
            "Organization that produces initiatives that improve quality of life in Cali.",
            "They find and implement solutions to problems that impact the quality of life of citizens of Cali.",
            "They join the dots between smart ideas and smart people who work to improve Cali.",
            html.A("https://chis.pa/en/", href = "https://chis.pa/en/")
        ],
        "picture": "chispa.jpg"
    }
]

# Transform each activity group into a Dash component in order to be visualized.
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
                                html.Ul([html.Li(element) for element in profile["description"]])
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

# Define base layout using Bootstrap grid system.
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
                dbc.Col(width={"size": 3}),
                profiles_html_list[9]
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


