"""Preprocess the audio files into smaller pieces for a quicker loading time."""

from typing import List
from pathlib import Path

import tqdm
import numpy as np
import pydub
from pydub import AudioSegment

from constants import ASSET_FOLDER, SPLIT_INTERVAL


test_files: List[str] = ["2011_audio.m4a", "2012_audio.m4a", "2023_audio.m4a"]


def splitter(sound, sound_name):
    """Split a large file into smaller ones."""
    offset = 0
    file_index = 0
    l = len(sound)

    print(f"Cutting {sound_name} into smaller pieces...")
    for _ in tqdm.tqdm(range(0, l, SPLIT_INTERVAL)):
        end = min(l, offset + SPLIT_INTERVAL)
        temp = sound[offset:end]
        offset = end

        temp.export(
            ASSET_FOLDER.joinpath(
                "processed/{}_{}_{}.mp3".format(
                    sound_name, file_index, SPLIT_INTERVAL
                ),
            ),
            format="mp3",
        )

        file_index += 1


for test_file in test_files:
    splitter(
        AudioSegment.from_file(ASSET_FOLDER.joinpath(test_file)),
        test_file
    )
