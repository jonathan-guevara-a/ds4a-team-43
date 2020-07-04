import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
from dash.dependencies import Input, Output
from sections import header, general, criminal_activity, citizens_perception, about_us, future_work

# Define the header layout.
layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Img(src = "assets/ds4a_colombia.svg")
            ]),
            width = 3
        ),
        dbc.Col(
            html.Div([
                html.H1("Team 43 - Criminal Activity vs Citizens Security Perception in Santiago de Cali")
            ])
        )
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("General", href = "general", id = "general-link")),
                    dbc.NavItem(dbc.NavLink("Criminal Activity", href = "criminal-activity", id = "criminal-activity-link")),
                    dbc.NavItem(dbc.NavLink("Citizens Perception", href = "citizens-perception", id = "citizens-perception-link")),
                    dbc.NavItem(dbc.NavLink("About Us", href = "about-us", id = "about-us-link")),
                    dbc.NavItem(dbc.NavLink("Future Work", href = "future-work", id = "future-work-link"))
                ],
                pills = True
            )
        )
    ])
])

# Define the callback to set the active section link.
@app.callback(
    [
        Output("general-link", "active"),
        Output("criminal-activity-link", "active"),
        Output("citizens-perception-link", "active"),
        Output("about-us-link", "active"),
        Output("future-work-link", "active")
    ],
    [Input("route", "pathname")]
)
def toggle_active_links(pathname):
    links = ["general", "criminal-activity", "citizens-perception", "about-us", "future-work"]

    if not pathname or pathname == "/":
        return [True, False, False, False, False]

    return [(pathname == "/{}".format(link)) for link in links]

# Define the callback to show the active section content.
@app.callback(
    Output("content", "children"),
    [Input("route", "pathname")]
)
def swith_content(active_link):
    print(active_link)

    if active_link in ["/", "/general"]:
        return general.layout
    elif active_link == "/criminal-activity":
        return criminal_activity.layout
    elif active_link == "/citizens-perception":
        return citizens_perception.layout
    elif active_link == "/about-us":
        return about_us.layout
    elif active_link == "/future-work":
        return future_work.layout

    return html.P("Please reload the page.")
