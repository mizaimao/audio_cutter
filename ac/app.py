#!/usr/bin/env python3
import os
import time
from textwrap import dedent

import dash
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State
import numpy as np
import pandas as pd

import cutter

DEBUG = True
FRAMERATE = 24.0
WAIT = 3
INSTRUCTION = """#### Instructions:
 Input a time interval below, followed by a quote.   
 Time format is (0 if empty):  
 **minute:second:milliseconds** to **minute:second:milliseconds**   
 Then input a one-line quote in the textbox
"""

record_path = "data/export.csv"
global df
cell_style = [
    {"if": {"column_id": "Index"}, "width": "4%", "textAlign": "left"},
    {"if": {"column_id": "Quotes"}, "width": "63%", "textAlign": "left"},
    {"if": {"column_id": "Time"}, "width": "10%"},
    {"if": {"column_id": "Length"}, "width": "5%"},
    {"if": {"column_id": "Submission"}, "width": "10%"},
    {"if": {"column_id": "Download"}, "width": "0%"},
    {"if": {"column_id": "Edits"}, "width": "3%"},
    {"if": {"column_id": "Source"}, "width": "5%"},
]
CSSSTYLE = [
    {
        "selector": ".dash-cell div.dash-cell-value",
        "rule": "display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;",
    }
]
STYLE_TABLE_STYLE = {"overflowX": "scroll", "overflowY": "scroll", "maxHeight": 500}
MINSEC_INPUT_STYLE = {
    "width": "10%",
    "display": "inline-block",
    "min": "0",
    "max": "59",
}
MSEC_INPUT_STYPE = {"width": "11%", "display": "inline-block", "min": "0", "max": "999"}

df = pd.read_csv(record_path, sep="\t")

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


# Custom Script for Heroku
if "DYNO" in os.environ:
    app.scripts.config.serve_locally = False
    app.scripts.append_script(
        {
            "external_url": "https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js"
        }
    )

app.title = "R Fragment Extractor"
app.scripts.config.serve_locally = True
app.config["suppress_callback_exceptions"] = True


def load_data(path):
    data_dict = {"root_round": root_round}

    if DEBUG:
        print(f"{path} loaded.")
    return data_dict


# Main App
app.layout = html.Div(
    [
        # Banner display
        html.Div(
            [
                html.H2(
                    "I want to ask how many people once used R? (Pre-Release)",
                    id="title",
                ),
                html.Img(
                    src="http://144.202.14.79/R.gif",
                    style={"width": "75px", "height": "75px"},
                ),
                # html.Img(src="https://www.r-project.org/Rlogo.png",style={'width' : '60px','height':'60px'})
            ],
            className="banner",
        ),
        # Body
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    ["Video placeholder"],
                                    id="div-video-player",
                                    style={
                                        "color": "rgb(255, 255, 255)",
                                        "margin-bottom": "-30px",
                                    },
                                ),
                                html.Div(
                                    [
                                        "Footage Selection:",
                                        dcc.Dropdown(
                                            options=[
                                                {
                                                    "label": "Hua Liang: An introduction to R (2012 CBIM Summer School)",
                                                    "value": "2012",
                                                },
                                                {
                                                    "label": "Generalized Additive Partial Linear Models with High-dimensional Covariates",
                                                    "value": "2011",
                                                },
                                            ],
                                            value="2012",
                                            id="dropdown-footage-selection",
                                            clearable=False,
                                        ),
                                    ],
                                ),
                                html.Div(
                                    [
                                        dcc.Markdown(INSTRUCTION),
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
                                                    style=MSEC_INPUT_STYPE,
                                                    min=0,
                                                    max=999,
                                                    value="",
                                                ),
                                                html.Div(
                                                    dcc.Markdown(" to"),
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
                                                    style=MSEC_INPUT_STYPE,
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
                                        dcc.Textarea(
                                            id="quotearea",
                                            placeholder="Enter quote...",
                                            value="",
                                            style={"width": "95%"},
                                        ),
                                        html.Button("Submit", id="button"),
                                        html.Div(
                                            id="output-container-button",
                                            children="Enter a time interval, and a quote then press submit",
                                        ),
                                    ],
                                    style={
                                        "margin": "30px 20px 15px 20px"
                                    },  # top right bottom left
                                ),
                            ],
                            className="six columns",
                            style={"margin-bottom": "20px"},
                        ),
                        html.Div(
                            [  # Right part of the page
                                html.Div(
                                    id="html_table",
                                    children=dash_table.DataTable(
                                        id="record_table",
                                        css=CSSSTYLE,
                                        columns=[
                                            {
                                                "name": i,
                                                "id": i,
                                                "hidden": True
                                                if i == "Download"
                                                else False,
                                            }
                                            for i in df.columns
                                        ],
                                        data=df.to_dict("index"),
                                        style_cell_conditional=cell_style,
                                        style_table=STYLE_TABLE_STYLE,
                                    ),
                                    style={
                                        "margin_top": "60px",
                                        "margin_left": "60px",
                                    },
                                ),
                                html.Div(
                                    [  # Right lower Downloading
                                        html.Div(dcc.Markdown("### Options")),
                                        html.Div(
                                            [
                                                html.Div(
                                                    dcc.Dropdown(
                                                        id="dl-dropdown",
                                                        options=[
                                                            {"label": x, "value": x}
                                                            for x in df["Index"]
                                                        ],
                                                        # multi=True,
                                                        # searchable=False,
                                                        placeholder="Select an index to download",
                                                        value=1,
                                                    ),
                                                    style={"height": "120%"},
                                                    className="six columns",
                                                ),
                                                html.Div(
                                                    html.Button("Edit", id="edit"),
                                                    className="three columns",
                                                ),
                                                html.Div(
                                                    html.A(
                                                        "Download",
                                                        style={"fontSize": "30"},
                                                        id="download-link",
                                                        download="",
                                                        href="",
                                                        target="_blank",
                                                    ),
                                                    className="three columns",
                                                ),
                                            ]
                                        ),
                                        html.P("", id="preview"),
                                        html.Div(
                                            dcc.Markdown(children="", id="editstr")
                                        ),
                                    ],
                                    style={
                                        "width": "70%",
                                        "display": "inline-block",
                                        "vertical-align": "middle",
                                        "horizontal-align": "middle",
                                        "margin": "10px 40px 10px 40px",
                                    },
                                    className="row",
                                ),
                            ],
                            className="six columns",
                            style={"margin-bottom": "20px"},
                        ),
                    ],
                    className="row",
                ),
            ],
            className="container scalable",
        ),
    ]
)


# Data Loading
@app.server.before_first_request
def load_all_footage():
    global data_dict, url_dict
    # Load the dictionary containing all the variables needed for analysis
    url_dict = {
        "2012": "https://www.youtube.com/watch?v=rd6qNEjJfps&t=564s",
        "2011": "https://www.youtube.com/watch?v=xeU5gl3w-OE",
    }
    df = pd.read_csv(record_path, sep="\t")


# Footage Selection
@app.callback(
    Output("div-video-player", "children"),
    [
        Input("dropdown-footage-selection", "value"),
    ],
)
def select_footage(footage):
    url = url_dict[footage]  # Find desired footage
    return []


# Submission
@app.callback(
    dash.dependencies.Output("output-container-button", "children"),
    [dash.dependencies.Input("button", "n_clicks")],
    [
        dash.dependencies.State("start_min", "value"),
        dash.dependencies.State("start_sec", "value"),
        dash.dependencies.State("start_msec", "value"),
        dash.dependencies.State("end_min", "value"),
        dash.dependencies.State("end_sec", "value"),
        dash.dependencies.State("end_msec", "value"),
        dash.dependencies.State("quotearea", "value"),
        dash.dependencies.State("dropdown-footage-selection", "value"),
    ],
)
def update_output(
    n_click,
    start_min,
    start_sec,
    start_msec,
    end_min,
    end_sec,
    end_msec,
    quote,
    video_input,
    mono,
):
    result = "Invalid input"
    quote = quote.split("\n")
    if len(quote) != 1:
        return result
    timeinputlist = [start_min, start_sec, start_msec, end_min, end_sec, end_msec]
    timeinputlist = [x if x else 0 for x in timeinputlist]
    if not sum(timeinputlist):
        return "Enter a time interval, and a quote then press submit"
    timeinput = "{:02d}:{:02d}:{:03d}-{:02d}:{:02d}:{:03d}".format(
        timeinputlist[0],
        timeinputlist[1],
        timeinputlist[2],
        timeinputlist[3],
        timeinputlist[4],
        timeinputlist[5],
    )
    print(timeinput)
    quoteinput = quote[0]
    print(quoteinput, timeinput, video_input)
    result = cutter.cutter(video_input, timeinput, quoteinput, mono != [], -1)
    return result


# Update table
@app.callback(
    dash.dependencies.Output("html_table", "children"),
    [dash.dependencies.Input("button", "n_clicks")],
    [],
)
def update_table(n_click):
    time.sleep(WAIT)
    global df
    df = pd.read_csv(record_path, sep="\t")
    return dash_table.DataTable(
        css=CSSSTYLE,
        columns=[
            {
                "name": i,
                "id": i,
                "hidden": True if i == "Download" else False,
                "align": "left" if i == "Quotes" else "right",
            }
            for i in df.columns
        ],
        style_table=STYLE_TABLE_STYLE,
        data=df.to_dict("rows"),
        style_cell_conditional=cell_style,
    )


# Update Download
@app.callback(
    dash.dependencies.Output("dl-dropdown", "options"),
    [dash.dependencies.Input("button", "n_clicks")],
    [],
)
def update_dropdown(n_click):
    time.sleep(WAIT + 1)
    return [{"label": x, "value": x} for x in df["Index"]]


@app.callback(
    dash.dependencies.Output("dl-dropdown", "value"),
    [dash.dependencies.Input("button", "n_clicks")],
    [],
)
def update_dropdown(n_click):
    time.sleep(WAIT + 1)
    return df.shape[0]


"""
@app.callback(
    dash.dependencies.Output('editstr', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [])
def update_dropdown(n_click):
    time.sleep(WAIT+1)
    return ''
"""


# Download
@app.callback(
    dash.dependencies.Output("download-link", "href"),
    [dash.dependencies.Input("dl-dropdown", "value")],
)
def update_download_link(audio_index):
    return df.iloc[int(audio_index) - 1]["Download"]


@app.callback(
    dash.dependencies.Output("preview", "children"),
    [dash.dependencies.Input("dl-dropdown", "value")],
)
def update_download_link(audio_index):
    return df.iloc[int(audio_index) - 1]["Quotes"]


# Editing
@app.callback(
    dash.dependencies.Output("editstr", "children"),
    [
        dash.dependencies.Input("button", "n_clicks"),
        dash.dependencies.Input("edit", "n_clicks"),
    ],
    [dash.dependencies.State("dl-dropdown", "value")],
)
def update_download_link(submit, n_clicks, video_index):
    if not n_clicks:
        return ""
    print(submit, n_clicks)

    video_edits = df.iloc[video_index - 1]["Edits"]
    return "##### Use left side input boxes to edit.   Current edit: {}".format(
        video_edits
    )


external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",  # Normalize the CSS
    "https://fonts.googleapis.com/css?family=Open+Sans|Roboto"  # Fonts
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdn.rawgit.com/xhlulu/9a6e89f418ee40d02b637a429a876aa9/raw/base-styles.css",
    "https://cdn.rawgit.com/plotly/dash-object-detection/875fdd6b/custom-styles.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "https://codepen.io/chriddyp/pen/brPBPO.css",
]
for css in external_css:
    app.css.append_css({"external_url": css})


# Running the server
if __name__ == "__main__":
    app.run_server(debug=1, host="0.0.0.0", port=22222)
