"""Callbacks for the app."""
from typing import List

from dash import Dash, html, dcc, Input, Output,State, callback
from constants import VIDEOS

def add_callbacks(app: Dash):
    @app.callback(
        Output("player", "url"),
        Input("video_selection_dropdown", "value")
    )
    def change_video(selected_video_id: int):
        return VIDEOS[selected_video_id]

    @app.callback(
        Output("preview_string", "children"),
        [Input("time_button", "n_clicks")],
        [
            State("start_min", "value"),
            State("start_sec", "value"),
            State("start_msec", "value"),
            State("end_min", "value"),
            State("end_sec", "value"),
            State("end_msec", "value"),
            State("quote_input", "value"),
            State("title_input", "value"),
            State("video_selection_dropdown", "value"),
        ],
    )
    def update_output(
        n_click: int,
        start_min: int,
        start_sec: int,
        start_msec: int,
        end_min: int,
        end_sec: int,
        end_msec: int,
        quote_input: str,
        title_input: str,
        video_selected: str,
    ):
        result: str = "Invalid input"
        quote_input: str = quote_input.split("\n")
        if len(quote_input) != 1:
            return "Invalid quote input: quote cannot exceed one line."
        time_input_list: List[int] = [start_min, start_sec, start_msec, end_min, end_sec, end_msec]
        time_input_list = [x if x else 0 for x in time_input_list]
        if not sum(time_input_list):
            return "Timestamps cannot be empty."
        timeinput = "{:02d}:{:02d}:{:03d}-{:02d}:{:02d}:{:03d}".format(*time_input_list)
        print(timeinput)
        quote_input = quote_input[0]
        print(quote_input, timeinput, video_selected)

        #result = cutter.cutter(video_input, timeinput, quote_input, mono != [], -1)
        #return result