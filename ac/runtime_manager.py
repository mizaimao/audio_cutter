"""Class to control runtime IO."""

from pathlib import Path
from typing import Any, Dict, Tuple, List
import json
import tempfile
import shutil
import datetime
import os

import pandas as pd

from constants import ASSET_FOLDER, OUTPUT_FOLDER

DEFAULT_COLS: List[str] = ['Index', 'Title', 'Quotes', 'Source', 'Length', 'Edits', 'Time', 'Submission']


class Control:
    def __init__(self):

        self.index_file: Path = ASSET_FOLDER.joinpath("index.json")
        self.df_file: Path = ASSET_FOLDER.joinpath("records.csv")
        
        self.temp_dir: Path = Path(tempfile.mkdtemp())
        self.temp_pointer: Path = None
        self.parent: Path = Path(__file__).parent

        self.current_index: int = self.load_index()
        self.df: pd.DataFrame = self.load_df()
        self.current_entry: Dict[str, Any] = None
        

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
            df = pd.read_csv(self.df_file)
        return df

    def update_df(self):
        self.df.to_csv(self.df_file)


    def update_temp_entry(self, new_entry: Dict[str, Any]):
        if self.temp_pointer is not None:
            os.remove(self.parent.joinpath(self.temp_pointer))

        temp_file_name: str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
        shutil.move(
            self.parent.joinpath("assets/temp.mp3"),
            self.parent.joinpath(f"assets/{temp_file_name}.mp3"),
        )
        self.temp_pointer = f"assets/{temp_file_name}.mp3"

        self.current_entry = new_entry
        return self.temp_pointer

    def get_new_preview_path(self) -> str:
        """
        The player would stick with the cached file so we have to make a new url if we
        want to refresh it. Otherwise if we keep using the old url/path, it will not
        update.
        """


    def add_entry(self):
        
        new_entry: Dict[str, Any] = self.current_entry
        new_entry["Index"] = self.current_index
        self.df = pd.concat(
            [
                self.df,
                pd.DataFrame.from_dict([new_entry], orient="columns"),
            ]
        )
        # Now update index and save stuffs to disk.
        self.current_index += 1
        self.update_index()
        self.update_df()
        # Save the audio file.
        shutil.copy(
            self.parent.joinpath(self.temp_pointer),
            self.parent.joinpath(f"assets/{new_entry['Title']}_{new_entry['Source']}.mp3")
        )
