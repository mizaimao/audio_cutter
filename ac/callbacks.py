"""Callbacks for the app."""
from typing import Any, Dict, List, Tuple
from pathlib import Path

from dash import Dash, html, dcc, Input, Output, State, callback, dash_table
from dash.exceptions import PreventUpdate
from pydub import AudioSegment

from constants import VIDEOS, OUTPUT_FOLDER
from utils import timestamp_check, generate_preview, get_empty_figure
from runtime_manager import Control, EntryNotFoundError
from cutter import cut_audio, CutError


def add_callbacks(app: Dash, control: Control):
    @app.callback(Output("player", "url"), Input("video_selection_dropdown", "value"))
    def change_video(selected_video_id: int):
        return VIDEOS[str(selected_video_id)]

    @app.callback(
        [
            Output("preview_string", "children"),
            Output("wave_plot", "figure", allow_duplicate=True),
            Output("audio_player", "url", allow_duplicate=True),
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
        prevent_initial_call="initial_duplicate",
    )
    def make_cut(
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
        if len(quote_input) != 1:
            return (
                "Invalid quote input: quote cannot exceed one line.",
                get_empty_figure(),
                "",
            )

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

        if timestamp_error:  # If an error occurs, this string will not be empty.
            return timestamp_error, get_empty_figure(), ""

        if sum(time_input_list) == 0:
            return "Timestamps not entered.", get_empty_figure(), ""

        # 2. Cut audio and create temporary file.
        time_str = "{:02d}:{:02d}:{:03d}-{:02d}:{:02d}:{:03d}".format(*time_input_list)
        quote_input: str = quote_input[0]
        if not quote_input:
            return "Quote is empty.", get_empty_figure(), ""
        if not title_input:
            return "Title is empty.", get_empty_figure(), ""

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
            pass
        temp_path: str = control.update_temp_entry(cut_record)

        # 3. Make a plot and push to display.
        # As the second return item.
        # 4. Push audio to the player.
        # As the third return item.
        return (
            "Audio cut successful.",
            generate_preview(
                audio_obj=audio_obj,
                height=180,
                width=650,
            ),
            temp_path,
        )

    @app.callback(
        [
            Output("record_table", "children", allow_duplicate=True),
            Output("audio_player", "url", allow_duplicate=True),
        ],
        Input("submit_button", "n_clicks"),
        prevent_initial_call=True,
    )
    def submit_audio(
        n_clicks: int,
    ):
        new_url: str = control.add_entry()
        if new_url == "":
            raise PreventUpdate

        return (
            dash_table.DataTable(
                control.df.to_dict("records"),
                [{"name": i, "id": i} for i in control.df.columns],
            ),
            new_url,
        )

    @app.callback(
        [
            Output("start_min", "value"),
            Output("start_sec", "value"),
            Output("start_msec", "value"),
            Output("end_min", "value"),
            Output("end_sec", "value"),
            Output("end_msec", "value"),
            Output("quote_input", "value"),
            Output("title_input", "value"),
            Output("video_selection_dropdown", "value"),
            Output("wave_plot", "figure", allow_duplicate=True),
            Output("audio_player", "url", allow_duplicate=True),
        ],
        [
            Input("load_button", "n_clicks"),
        ],
        [State("load_input", "value")],
        prevent_initial_call=True,
    )
    def load_entry(
        n_clicks: int,
        load_input: str,
    ):
        # Sanity check
        try:
            load_input = int(load_input)
        except:
            raise PreventUpdate
        if load_input < 0:
            raise PreventUpdate

        input_meta: List[str] = None
        new_url: str = ""
        try:
            input_meta, new_url = control.load_entry(index=load_input)
        except EntryNotFoundError:
            raise PreventUpdate
        if new_url == "":
            raise PreventUpdate

        audio_obj: AudioSegment = AudioSegment.from_file(
            Path(__file__).parent.joinpath(new_url)
        )

        return (
            *input_meta,
            generate_preview(
                audio_obj=audio_obj,
                height=180,
                width=650,
            ),
            new_url,
        )
