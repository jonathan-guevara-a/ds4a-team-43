import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from application import app
from dash.dependencies import Input, Output
from sections import header, general, criminal_activity, citizens_perception, about_us, future_work

layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    html.Img(src = "assets/ds4a_colombia.svg")
                ]),
                lg = 3,
                md = 4,
                sm = 12
            ),
            dbc.Col(
                html.Div(
                    [
                        html.H2("Team 43 - Criminal Activity vs Citizens Security Perception in Santiago de Cali"),
                    ],
                    className = "text-center"
                )
            ),
        ],
        className = "mx-0 p-3 d-flex flex-wrap align-items-center"
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Tabs(
                    [
                        dbc.Tab(label = "General", tab_id = "general-tab"),
                        dbc.Tab(label = "Criminal Activity", tab_id = "criminal-activity-tab"),
                        dbc.Tab(label = "Citizens Perception", tab_id = "citizens-perception-tab"),
                        dbc.Tab(label = "About Us", tab_id = "about-us-tab"),
                        dbc.Tab(label = "Future Work", tab_id = "future-work-tab")
                    ],
                    id = "navigation-tabs",
                    active_tab = "general-tab"
                )
            )
        ],
        className = "mx-0 p-3"
    )
])

@app.callback(
    Output("content", "children"),
    [Input("navigation-tabs", "active_tab")]
)
def switch_tab(active_tab):
    if active_tab == "general-tab":
        return general.layout
    elif active_tab == "criminal-activity-tab":
        return criminal_activity.layout
    elif active_tab == "citizens-perception-tab":
        return citizens_perception.layout
    elif active_tab == "about-us-tab":
        return about_us.layout
    elif active_tab == "future-work-tab":
        return future_work.layout

    return html.P("Please reload the page.")
