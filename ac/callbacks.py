"""Callbacks for the app."""
from typing import List, Tuple

from dash import Dash, html, dcc, Input, Output,State, callback
from constants import VIDEOS
from utils import timestamp_check

def add_callbacks(app: Dash):
    @app.callback(
        Output("player", "url"),
        Input("video_selection_dropdown", "value")
    )
    def change_video(selected_video_id: int):
        return VIDEOS[selected_video_id]

    @app.callback(
        [Output("preview_string", "children")],
        [Input("cut_button", "n_clicks")],
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
    ) -> Tuple[
        str
    ]:
        """
        Core function. The the following:
        1. Input sanity checks.
        2. Cut audio and generate audio file.
        3. Make a plot and push to display.
        4. Push audio to the player.
        """
        # 1. Sanity checks.
        result: str = "Invalid input"
        quote_input: str = quote_input.split("\n")
        if len(quote_input) != 1:
            return "Invalid quote input: quote cannot exceed one line."
        
        timestamp_error: str = timestamp_check(
            start_min=start_min, start_sec=start_sec, start_msec=start_msec,
            end_min=end_min, end_sec=end_sec, end_msec=end_msec
        )
        if timestamp_error:  # If an error occurs, this string will not be empty.
            return timestamp_error

        time_input_list: List[int] = [start_min, start_sec, start_msec, end_min, end_sec, end_msec]
        time_input_list = [x if x else 0 for x in time_input_list]
        if not sum(time_input_list):
            return "Timestamps cannot be empty."
        
        
        # 2. Cut audio and create temporary file.
        timeinput = "{:02d}:{:02d}:{:03d}-{:02d}:{:02d}:{:03d}".format(*time_input_list)
        print(timeinput)
        quote_input = quote_input[0]
        print(quote_input, timeinput, video_selected)

        #result = cutter.cutter(video_input, timeinput, quote_input, mono != [], -1)
        #return result

    @app.callback(
        Output("audio_player", "url"),
        Input("preview_button", "n_clicks"),
    )
    def make_entry(
        n_clicks: int,
    ):
        """
        Core function. Adds the entry information to the table and saves audio to file.
        """
        if not n_clicks:
            return "assets/oaic.mp3"

        content = ["assets/2011_audio.m4a", "assets/surch_pdf.mp3", "assets/to_implement.mp3"]

        return content[n_clicks % 2]
    
    # @app.callback(
    #     Output("audio_player", "url"),
    #     Input("submit_button", "n_clicks"),
    # )
    # def update_output(
    #     n_click: int,
    # ):
    #     return None