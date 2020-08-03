import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from application import app
from dash.dependencies import Input, Output
from sections import header, general, criminal_activity, citizens_perception, forecasting_prediction, about_us, future_work

# Define base layout using Bootstrap grid system.
layout = html.Div(
    children = [
        dbc.Row(
            children = [
                dbc.Col(
                    children = [
                        html.Div(
                            children = [
                                html.Img(src = "assets/ds4a_colombia.svg")
                            ]
                        )
                    ],
                    lg = {"size": 3, "offset": 1},
                    md = {"size": 4, "offset": 1},
                    sm = {"size": 12, "offset": 1}
                ),
                dbc.Col(
                    children = [
                        html.Div(
                            children = [
                                html.H1(
                                    children = [
                                        "Criminal Activity vs Citizens Security",
                                        html.Br(),
                                        "Perception in Santiago de Cali"
                                    ]
                                ),
                            ],
                            className = "text-center"
                        )
                    ]
                ),
                dbc.Col(
                    children = [],
                    width = {"size": 1}
                )
            ],
            className = "mx-0 p-10 d-flex flex-wrap align-items-center main-header cali-background primary-color",

        ),
        dbc.Row(
            children = [
                dbc.Col(
                    children = [
                        dbc.Tabs(
                            children = [
                                dbc.Tab(
                                    label = "General", tab_id = "general-tab"
                                ),
                                dbc.Tab(
                                    label = "Criminal Activity", tab_id = "criminal-activity-tab"
                                ),
                                dbc.Tab(
                                    label = "Citizens Perception", tab_id = "citizens-perception-tab"
                                ),
                                dbc.Tab(
                                    label = "Forecasting / Prediction", tab_id = "forecasting-prediction-tab"
                                ),
                                dbc.Tab(
                                    label = "About Us", tab_id = "about-us-tab"
                                ),
                                dbc.Tab(
                                    label = "Future Work", tab_id = "future-work-tab"
                                )
                            ],
                            id = "navigation-tabs",
                            active_tab = "general-tab"
                        )
                    ]
                )
            ],
            className = "mx-0 secondary-color"
        )
    ]
)

# Define callback to display the content from the selected tab.
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
    elif active_tab == "forecasting-prediction-tab":
        return forecasting_prediction.layout
    elif active_tab == "about-us-tab":
        return about_us.layout
    elif active_tab == "future-work-tab":
        return future_work.layout

    return html.P("Please reload the page.")
