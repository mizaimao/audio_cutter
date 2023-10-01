"""Helper function and small modules."""

from typing import List

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from pydub import AudioSegment


def timestamp_check(
    start_min: int,
    start_sec: int,
    start_msec: int,
    end_min: int,
    end_sec: int,
    end_msec: int,
) -> str:
    time_error_flag: bool = True
    if start_min < end_min:
        time_error_flag = False
    elif start_min == end_min:
        if start_sec < end_sec:
            time_error_flag = False
        elif start_sec == end_msec:
            if start_msec < end_msec:
                time_error_flag = False
            else:
                pass
        else:
            pass
    else:
        pass

    if time_error_flag and sum([start_min, start_sec, start_msec]) != 0:
        return "Start timestamp is larger than or equal to end timestamp."
    return ""


def get_empty_figure(
    height: int = 180, width: int = 650, message: str = "Audio Preview Not Available"
):
    fig = go.Figure()
    return fig.update_layout(
        height=height,
        width=width,
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[
            {
                "text": message,
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 28},
            }
        ],
    )


def generate_preview(audio_obj: AudioSegment, height:int = 180, width: int = 650):
    """Make a wave plot."""
    samples: np.ndarray = np.array(audio_obj.get_array_of_samples())
    fig = px.line(samples, y=0, render_mode="webgl")  # "y=0" disables legend.
    fig.update_layout(
        yaxis_title="",
        yaxis_fixedrange=True,
    )
    # X-axis label.
    fig.update_xaxes(
        title="milliseconds",
    )
    return fig.update_layout(
        plot_bgcolor="white",
        margin=dict(t=0, l=5, b=0, r=5),
        height=height,
        width=width,
    ).update_xaxes(
        title="milliseconds", linecolor="lightgrey", gridcolor="lightgrey"
    ).update_yaxes(mirror=True, linecolor="lightgrey", gridcolor="lightgrey")
    
