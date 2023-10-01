"""Class to control runtime IO."""

from pathlib import Path
from typing import Any, Dict, Tuple, List
import json
import tempfile
import shutil
import datetime
import os

import pandas as pd

from constants import ASSET_FOLDER, TEMP_PREFIX

DEFAULT_COLS: List[str] = [
    "Index",
    "Title",
    "Quotes",
    "Source",
    "Length",
    "Edits",
    "Time",
    "Submission",
]


class EntryNotFoundError(Exception):
    pass


class Control:
    def __init__(self):
        # Check or make record files.
        self.index_file: Path = ASSET_FOLDER.joinpath("index.json")
        self.df_file: Path = ASSET_FOLDER.joinpath("records.csv")

        # Create placeholders for paths
        self.temp_dir: Path = Path(tempfile.mkdtemp())
        self.temp_pointer: Path = None
        self.parent: Path = Path(__file__).parent

        # Resume previous records.
        self.current_index: int = self.load_index()
        self.df: pd.DataFrame = self.load_df()
        self.current_entry: Dict[str, Any] = None

        # Check or create necessary folders.
        self.check_folders()

    def check_folders(self):
        """Check existing files and create folders if necessary."""
        p_folder: Path = self.parent.joinpath("assets/processed")
        s_folder: Path = self.parent.joinpath("assets/saves")
        t_folder: Path = self.parent.joinpath("assets/temp")

        for folder in [p_folder, s_folder, t_folder]:
            folder.mkdir(parents=True, exist_ok=True)

        if len(list(p_folder.glob("*.mp3"))) == 0:
            raise FileNotFoundError(f"No processed files found in {p_folder}.")
        self.remove_temp_files()

    def remove_temp_files(self):
        """Clean temp folder."""
        for temp_path in self.parent.joinpath("assets/temp/").glob(
            TEMP_PREFIX + "*.mp3"
        ):
            os.remove(temp_path)

    def load_index(self) -> int:
        index: int = -1
        if not self.index_file.is_file():
            json.dump(-1, open(self.index_file, "w"))
        else:
            index = json.load(open(self.index_file))
        return index + 1

    def update_index(self):
        json.dump(self.current_index, open(self.index_file, "w"))

    def load_df(self) -> pd.DataFrame:
        if not self.df_file.is_file():
            df: pd.DataFrame = pd.DataFrame()
            df[DEFAULT_COLS] = None
        else:
            df = pd.read_csv(self.df_file, index_col=[0])
        return df

    def update_df(self):
        self.df.to_csv(self.df_file)

    def update_temp_entry(self, new_entry: Dict[str, Any]):
        """
        The player (or browser) would automatically cache seen path to audio files.
        In order to refresh it every time we generate a cut audio, we need to have a different
        name.
        """
        if self.temp_pointer is not None:
            old_file_path: Path = self.parent.joinpath(self.temp_pointer)
            if old_file_path.is_file():
                os.remove(old_file_path)

        temp_file_name: str = TEMP_PREFIX + datetime.datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S_%f"
        )
        shutil.move(
            self.parent.joinpath("assets/temp/temp.mp3"),
            self.parent.joinpath(f"assets/temp/{temp_file_name}.mp3"),
        )
        self.temp_pointer = f"assets/temp/{temp_file_name}.mp3"

        self.current_entry = new_entry
        return self.temp_pointer

    def add_entry(self) -> str:
        """
        Submit current (temp) entry to df and give the temp audio file a name.
        Returns finalized path of moved audio file.
        """
        if self.current_entry is None:
            return ""

        # Complete df entry dict, and update df.
        new_entry: Dict[str, Any] = self.current_entry
        new_entry["Index"] = self.current_index
        self.df = pd.concat(
            [
                self.df,
                pd.DataFrame.from_dict([new_entry], orient="columns"),
            ]
        )
        self.df = self.df[DEFAULT_COLS]
        # Now update index and save stuffs to disk.
        self.current_index += 1
        self.update_index()
        self.update_df()
        # Save the audio file.
        new_url: Path = f"assets/saves/{new_entry['Title']}_{new_entry['Source']}.mp3"
        shutil.copy(
            self.parent.joinpath(self.temp_pointer),
            self.parent.joinpath(new_url),
        )
        # Remove previous temp files.
        self.remove_temp_files()

        # Clear current entry to prevent duplicates.
        self.current_entry = None

        return new_url

    def load_entry(self, index: int):
        """Use an index to load an audio piece and meta."""
        assert isinstance(index, int), f"Unexpected index type: {type(index)}."

        _record: List[Dict[str, Any]] = self.df[self.df["Index"].isin([index])].to_dict(
            "records"
        )
        if len(_record) != 1:
            raise EntryNotFoundError
        record: Dict[str, Any] = _record[0]

        times: List[str] = record["Time"].split("-")
        # start_min, sec, msec, end_min, sec, msec
        entry_times: List[int] = Control.split_time(times[0]) + Control.split_time(
            times[1]
        )

        quote: str = record["Quotes"]
        title: str = record["Title"]
        video: str = record["Source"]

        # Copy original audio to a temp one and get address.
        audio_short_url: str = f"assets/saves/{record['Title']}_{record['Source']}.mp3"
        temp_file_name: str = TEMP_PREFIX + datetime.datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S_%f"
        )
        shutil.copy(
            self.parent.joinpath(audio_short_url),
            self.parent.joinpath(f"assets/temp/{temp_file_name}.mp3"),
        )
        self.temp_pointer = f"assets/temp/{temp_file_name}.mp3"

        # Update current pointer.
        self.current_entry = {
            "Title": title,
            "Quotes": quote,
            "Time": record["Time"],
            "Length": record["Length"],
            "Submission": record["Submission"],
            "Source": str(video),
            "Edits": 0,
        }

        return (
            entry_times + [quote, title, video],
            self.temp_pointer,
        )

    @staticmethod
    def split_time(time_str: str) -> Tuple[int, int, int]:
        return [str(x) for x in time_str.split(":")]
