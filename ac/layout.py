"""Controls layout of the web app."""

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


def add_layout(app):
    app.layout = html.Div(
        [
            add_navbar(),
            dbc.Row(
                [
                    # Video and options.
                    add_left_part(6),
                    # Cutting time slots and records.
                    add_right_part(6),
                ]
            )
        ]
    )


def add_navbar():
    return dbc.NavbarSimple(
    children=[
    ],
    brand="Online Audio Cutter for Prof. Hua Liang's Videos.",
    brand_href="#",
    color="primary",
    dark=True,
)

def add_left_part(width: int):
    return dbc.Col(
        html.Div("A single, half-width column"),
        width={
            "size": width,
        },
    )


def add_right_part(width: int):
    return dbc.Col(
        html.Div("Right chicken"),
        width={
            "size": width,
        },
    )
