"""Controls layout of the web app."""

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash_player


def add_layout(app: Dash):
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
        [
            dbc.Row(
                [
                html.H3("Video Player"),
                add_video_player(),
                html.H3("Video Selection"),
                add_video_selector(),
                ]
            ),
        ],
        width={
            "size": width,
        },
    )


def add_right_part(width: int):
    return dbc.Col(
        [
            html.Div("Right chicken"),
            dbc.Row(),
        ],
        width={
            "size": width,
        },
    )

def add_video_player():
    return dash_player.DashPlayer(
        id="player",
        url="https://www.youtube.com/watch?v=rd6qNEjJfps",
        controls=True,
        width="100%",
        height="450px",
    )

def add_video_selector():
    return dcc.Dropdown(
        id="video_selection_dropdown",
        options=[
            {'label': 'Hua Liang: An introduction to R (2012 CBIM Summer School)', 'value': '2012'},
            {'label': 'Hua Liang, PhD', 'value': '2011'},
            {'label': 'SFSN Presents Hua Liang', 'value': '2023'},
        ],
        value='2012'
        )
