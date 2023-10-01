from typing import Dict
from pathlib import Path

VIDEOS: Dict[str, str] = {
    "2011": "https://www.youtube.com/watch?v=xeU5gl3w-OE&t=2146s&pp=ygUJaHVhIGxpYW5n",
    "2012": "https://www.youtube.com/watch?v=rd6qNEjJfps&t=1281s&pp=ygUJaHVhIGxpYW5n",
    "2023": "https://www.youtube.com/watch?v=IWIvy7GM7DI&t=1822s&pp=ygUJaHVhIGxpYW5n",
}

DEFAULT_AUDIO_SOURCES: Dict[str, str] = {
    "2011": "assets/2011_audio.m4a",
    "2012": "assets/2012_audio.m4a",
    "2023": "assets/2023_audio.m4a",
}

SPLIT_INTERVAL: int = 20000  # in ms, 1000 ms == 1 sec
ASSET_FOLDER: Path = Path(__file__).parent.joinpath("assets")
OUTPUT_FOLDER: Path = Path(__file__).parent.joinpath("saves")