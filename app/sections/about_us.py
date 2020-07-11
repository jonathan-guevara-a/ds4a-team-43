import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


layout = html.Div([
    html.H2("Team 43", className = "text-center"),
    html.Br(),
    html.Br(),
    html.H4("Daniel Gaitán Forero", className = "text-center"),
    html.H4("Fabio Andrés Sánchez Bernal", className = "text-center"),
    html.H4("Jhon Alexander Parra Jiménez", className = "text-center"),
    html.H4("Jonathan Guevara Agudelo", className = "text-center"),
    html.H4("Luz Elena Thompson Pinzón", className = "text-center"),
    html.H4("Maria Camila Manrique Nuñez", className = "text-center"),
    html.Br(),
    html.Br(),
    dbc.Row(
        dbc.Col(
            [
                html.P("Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                html.P("Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                html.P("Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            ],
            width={"size": 6, "offset": 3},
            className = "text-center"
        )
    )
])


