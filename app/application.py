import dash
import dash_bootstrap_components as dbc

# Create the Dash app object.
app = dash.Dash(__name__, suppress_callback_exceptions = True, external_stylesheets = [dbc.themes.BOOTSTRAP])
application = app.server
