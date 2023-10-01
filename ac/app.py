from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from layout import add_layout
from callbacks import add_callbacks
from runtime_manager import Control

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

control: Control = Control()
add_layout(app)
add_callbacks(app, control)

if __name__ == "__main__":
    app.run(debug=False)
