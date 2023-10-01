"""Controls layout of the web app."""

from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
import dash_player

from utils import get_empty_figure
from runtime_manager import Control


TIMESTAMP_INSTRUCTION: str = """
Timestamps: Input start and end timestamps to cut the audio. Format is **minute:second:milliseconds**  
**Example**: 25:54:720 - 25:57:000 (Empty fields are treated as zeros)   
"""
QUOTE_INSTRUCTION: str = """
Quote: What our great professor said in this quote.  
**Example**: Oh actually I ge... I count...   
"""
TITLE_INSTRUCTION: str = """
Title: Used for naming the download files.  
**Example**: oaic  
"""

MINSEC_INPUT_STYLE = {
    "width": "10%",
    "display": "inline-block",
    "min": "0",
    "max": "59",
}
MSEC_INPUT_STYLE = {"width": "11%", "display": "inline-block", "min": "0", "max": "999"}


def add_layout(app: Dash, control: Control):
    app.layout = html.Div(
        [
            # Add storage.
            dcc.Store(id="audio_file_path"),
            # Add main layout.
            add_navbar(),
            dbc.Row(
                [
                    # Video and options.
                    add_left_part(7, control=control),
                    # Cutting time slots and records.
                    add_right_part(5),
                ]
            ),
        ]
    )


def add_navbar():
    return dbc.NavbarSimple(
        children=[],
        brand="Online Audio Cutter for Prof. Hua Liang's Videos.",
        brand_href="#",
        color="primary",
        dark=True,
    )


def add_left_part(width: int, control: Control):
    return dbc.Col(
        [
            dbc.Row(
                [
                    html.H3("Video Selection"),
                    add_video_selector(),
                    html.Hr(),
                    add_video_player(width=width),
                    html.Hr(),
                    html.Div(
                        dash_table.DataTable(
                            control.df.to_dict("records"),
                            [{"name": i, "id": i} for i in control.df.columns],
                        ),
                        id="record_table",
                    ),
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
            dbc.Row(
                [
                    add_time_inputs(),
                    add_loader(),
                    add_dual_buttons(),
                    add_audio_preview_panes(),
                ]
            ),
        ],
        width={
            "size": width,
        },
    )


def add_dual_buttons():
    return html.Div(
        [
            dbc.Button(
                "Load",
                id="load_button",
                color="success",
                className="me-1",
            ),
            dbc.Button("Submit", id="submit_button", color="warning", className="me-1"),
        ],
        className="d-grid d-md-flex justify-content-md-around",
    )


def add_loader():
    return html.Div(
        [
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Markdown("Load by index", id="submission_string"),
                    ),
                    dbc.Col(
                        dbc.Input(
                            id="load_input",
                            type="number",
                            min=0,
                            placeholder="",
                            value="",
                            style={"width": "20%"},
                        )
                    ),
                ]
            ),
            html.Hr(),
        ]
    )


def add_audio_preview_panes():
    return dbc.Col(
        [
            dcc.Graph(id="wave_plot", figure=get_empty_figure(height=250, width=600)),
            dbc.Row(
                [
                    dash_player.DashPlayer(
                        id="audio_player",
                        url="assets/surch_pdf.mp3",
                        controls=True,
                        width="80%",
                        height="45px",
                    ),
                ]
            ),
        ]
    )


def add_time_inputs():
    return html.Div(
        [
            html.H3("Inputs here"),
            dcc.Markdown(TIMESTAMP_INSTRUCTION),
            html.Div(
                [
                    dcc.Input(
                        id="start_min",
                        type="number",
                        style=MINSEC_INPUT_STYLE,
                        min=0,
                        max=59,
                        value="",
                    ),
                    html.Div(
                        dcc.Markdown(" :"),
                        style={
                            "width": "1%",
                            "display": "inline-block",
                            "marginLeft": "5",
                        },
                    ),
                    dcc.Input(
                        id="start_sec",
                        type="number",
                        style=MINSEC_INPUT_STYLE,
                        min=0,
                        max=59,
                        value="",
                    ),
                    html.Div(
                        dcc.Markdown(" :"),
                        style={
                            "width": "1%",
                            "display": "inline-block",
                            "marginLeft": "5",
                        },
                    ),
                    dcc.Input(
                        id="start_msec",
                        type="number",
                        style=MSEC_INPUT_STYLE,
                        min=0,
                        max=999,
                        value="",
                    ),
                    html.Div(
                        dcc.Markdown("  to "),
                        style={
                            "width": "3%",
                            "display": "inline-block",
                            "marginLeft": "8",
                        },
                    ),
                    dcc.Input(
                        id="end_min",
                        type="number",
                        style=MINSEC_INPUT_STYLE,
                        min=0,
                        max=59,
                        value="",
                    ),
                    html.Div(
                        dcc.Markdown(" :"),
                        style={
                            "width": "1%",
                            "display": "inline-block",
                            "marginLeft": "5",
                        },
                    ),
                    dcc.Input(
                        id="end_sec",
                        type="number",
                        style=MINSEC_INPUT_STYLE,
                        min=0,
                        max=59,
                        value="",
                    ),
                    html.Div(
                        dcc.Markdown(" :"),
                        style={
                            "width": "1%",
                            "display": "inline-block",
                            "marginLeft": "5",
                        },
                    ),
                    dcc.Input(
                        id="end_msec",
                        type="number",
                        style=MSEC_INPUT_STYLE,
                        min=0,
                        max=999,
                        value="",
                    ),
                ],
                style={
                    "width": "600",
                    "vertical-align": "middle",
                    "marginBottom": "10",
                },
                className="container",
            ),
            dcc.Markdown(QUOTE_INSTRUCTION),
            dbc.Input(
                id="quote_input",
                placeholder="Enter quote...",
                value="",
                style={"width": "85%"},
            ),
            dcc.Markdown(TITLE_INSTRUCTION),
            dbc.Input(
                id="title_input",
                placeholder="Enter title...",
                value="",
                style={"width": "30%"},
            ),
            html.Label(""),  # Spacer.
            dbc.Button("Cut", id="cut_button"),
            dcc.Markdown("before chicken", id="preview_string"),
        ],
        style={"margin": "0px 0px 0px 0px"},  # top right bottom left
    )


def add_video_player(width: int):
    height: int = int(450 // 6 * width)
    return dash_player.DashPlayer(
        id="player",
        url="https://www.youtube.com/watch?v=rd6qNEjJfps",
        controls=True,
        width="100%",
        height=f"{height}px",
    )


def add_video_selector():
    return dcc.Dropdown(
        id="video_selection_dropdown",
        options=[
            {
                "label": "Hua Liang: An introduction to R (2012 CBIM Summer School)",
                "value": "2012",
            },
            {"label": "Hua Liang, PhD", "value": "2011"},
            {"label": "SFSN Presents Hua Liang", "value": "2023"},
        ],
        value="2012",
    )
