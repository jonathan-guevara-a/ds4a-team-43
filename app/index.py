import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from application import app
from sections import header

app.title = "DS4A - Team 43"

app.layout = html.Div([
    dcc.Location(id = "route", refresh = False),
    header.layout,
    html.Div(id = "content", className = "px-3")
])

if __name__ == "__main__":
    app.run_server(host = "0.0.0.0", debug = False)
