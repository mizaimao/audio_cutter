"""Callbacks for the app."""
from typing import Dict
from dash import Dash, html, dcc, Input, Output, callback

VIDEOS: Dict[str, str] = {
    "2011": "https://www.youtube.com/watch?v=xeU5gl3w-OE&t=2146s&pp=ygUJaHVhIGxpYW5n",
    "2012": "https://www.youtube.com/watch?v=rd6qNEjJfps&t=1281s&pp=ygUJaHVhIGxpYW5n",
    "2023": "https://www.youtube.com/watch?v=IWIvy7GM7DI&t=1822s&pp=ygUJaHVhIGxpYW5n",
}


def add_callbacks(app: Dash):
    @app.callback(
        Output("player", "url"),
        Input("video_selection_dropdown", "value")
    )
    def change_video(selected_video_id: int):
        return VIDEOS[selected_video_id]
