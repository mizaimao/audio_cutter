"""Callbacks for the app."""
from typing import Any, Dict, List, Tuple

from dash import Dash, html, dcc, Input, Output, State, callback
from pydub import AudioSegment

from constants import VIDEOS, OUTPUT_FOLDER
from utils import timestamp_check, generate_preview, get_empty_figure
from runtime_manager import Control
from cutter import cut_audio, CutError


def add_callbacks(app: Dash, control: Control):
    @app.callback(Output("player", "url"), Input("video_selection_dropdown", "value"))
    def change_video(selected_video_id: int):
        return VIDEOS[selected_video_id]

    @app.callback(
        [
            Output("preview_string", "children"),
            Output("wave_plot", "figure"),
            Output("audio_player", "url"),
            # Output("submission_string", "children")
        ],
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
    ) -> Tuple[str]:
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
        print("AAA")
        if len(quote_input) != 1:
            print("HHERER")
            return (
                "Invalid quote input: quote cannot exceed one line.",
                get_empty_figure(),
                "",
            )

        print("BBB")
        _time_input_list: List[str] = [
            start_min,
            start_sec,
            start_msec,
            end_min,
            end_sec,
            end_msec,
        ]
        time_input_list: List[int] = [int(x) if x else 0 for x in _time_input_list]
        timestamp_error: str = timestamp_check(*time_input_list)

        print("CCC", timestamp_error)
        if timestamp_error:  # If an error occurs, this string will not be empty.
            return timestamp_error, get_empty_figure(), ""

        if sum(time_input_list) == 0:
            return "Timestamps not entered.", get_empty_figure(), ""

        print("DDD")
        print(quote_input, type(quote_input))
        print(title_input, type(title_input))
        # 2. Cut audio and create temporary file.
        time_str = "{:02d}:{:02d}:{:03d}-{:02d}:{:02d}:{:03d}".format(*time_input_list)
        quote_input: str = quote_input[0]
        print(quote_input, time_str, video_selected)
        print("EEE")

        audio_obj: AudioSegment = None
        cut_record: Dict[str, Any] = None

        try:
            audio_obj, cut_record = cut_audio(
                video_name=video_selected,
                time_str=time_str,
                quote=quote_input,
                title=title_input,
                mono=False,
                edits=0,
            )
        except CutError:
            print("ERROR")
            pass

        print("FFF")
        temp_path: str = control.update_temp_entry(cut_record)
        print("GGG")
        print(cut_record)

        # 3. Make a plot and push to display.

        # 4. Push audio to the player.
        # As the second return item.
        return (
            "Audio cut successful.",
            generate_preview(
                audio_obj=audio_obj,
                height=180,
                width=650,
            ),
            temp_path,
        )

    # @app.callback(
    #     Output("audio_player", "url"),
    #     Input("submit_button", "n_clicks"),
    # )
    # def update_output(
    #     n_clicks: int,
    # ):
    #     A = ["assets/saves/r_powerful.mp3", "assets/2011_audio.m4a"]
    #     if not n_clicks:
    #         n_clicks = 0
    #     print(A[n_clicks % 2])
    #     return A[n_clicks % 2]
