#!/usr/bin/env python3
import datetime
from pathlib import Path

import pandas as pd
import numpy as np
import pydub
from pydub import AudioSegment

from ac.constants import ASSET_FOLDER, DEFAULT_AUDIO_SOURCES, SPLIT_INTERVAL, OUTPUT_FOLDER


audioPath = "data/sample.aac"
testInterval = "0:30-1:3"

dfpath = "data/export.csv"


def formatter_lv1(singleTS):
    tmpTS = []
    try:
        tmpTS = singleTS.split(":")
    except:
        raise ValueError("input error")
    lenTmpTs = len(tmpTS)
    totalmsec = 0
    formatted_str = ""

    if lenTmpTs == 3:
        totalmsec += int(tmpTS[0]) * 60 * 1000 + int(tmpTS[1]) * 1000 + int(tmpTS[2])
        formatted_str = "{:02d}:".format(int(tmpTS[0])) + "{:02d}".format(int(tmpTS[1]))
    elif lenTmpTs == 2:
        totalmsec += int(tmpTS[0]) * 60 * 1000 + int(tmpTS[1]) * 1000
        formatted_str = "{:02d}:".format(int(tmpTS[0])) + "{:02d}".format(int(tmpTS[1]))
    elif lenTmpTs == 1:
        totalmsec += int(tmpTS[0]) * 1000
        formatted_str = "00:" + "{:02d}".format(int(tmpTS[0]))

    else:
        raise ValueError("input error")

    return totalmsec, formatted_str


def formatter_lv0(time_string: str):
    if len(time_string) > 50:
        raise ValueError("too long")
    tmpstr = []
    try:
        tmpstr = time_string.split("-")
    except:
        raise ValueError("""must include '-' """)
    assert len(tmpstr) == 2

    start, startstr = formatter_lv1(tmpstr[0])
    end, endstr = formatter_lv1(tmpstr[1])
    assert end > start

    return start, end, startstr + "-" + endstr


def file_finder(start, end, video_name):
    start_file = start // SPLIT_INTERVAL
    start_point = start % SPLIT_INTERVAL

    end_file = end // SPLIT_INTERVAL
    end_point = end % SPLIT_INTERVAL

    sound = AudioSegment.from_file(
        ASSET_FOLDER.joinpath(
            "processed/{}_{}_{}.mp3".format(video_name, start_file, SPLIT_INTERVAL)
        )
        
    )

    if start_file == end_file:
        return sound[start_point : end_point + 1]
    elif start_file < end_file:
        sound = sound[start_point:]
        left = start_file + 1
        while left <= end_file:
            temp = AudioSegment.from_file(
                ASSET_FOLDER.joinpath(
                    "processed/{}_{}_{}.mp3".format(video_name, left, SPLIT_INTERVAL)
                )
            )
            if left == end_file:
                temp = temp[:end_point]
            sound += temp
            left += 1
        return sound
    else:
        exit(1)


def cut_audio(video_name: str, time_str: str, quote: str, mono: bool, edits: int):
    """
    Given a time range (in time_str), use the correct source (in video_name) to cut the requested
    small piece of audio. Updates the meta table as well.
    """
    if not time_str:
        return True
    edits = max(0, int(edits))
    start, end, dispstr = formatter_lv0(time_str.replace(" ", ""))

    export_file_name = (
        dispstr.replace(":", "_")
        + "_{}".format(video_name)
        + ("_{}".format(str(edits)) if edits else "")
        + ".mp3"
    )

    # Determinant step
    interested = file_finder(start, end, video_name)
    try:
        interested.export(
            OUTPUT_FOLDER.joinpath(
                export_file_name, format="mp3"
            )
        )
    except:
        exit(1)

    # Adding entry to table
    currentDT = datetime.datetime.now()
    generate_time = currentDT.strftime("%m/%d/%Y %H:%M:%S")
    audio_length = "{:10.2f}".format((end - start) / 1000) + "s"
    # Index,Quotes,Time,Length,Submission,Download,Source
    df = pd.read_csv(dfpath, sep="\t")

    newRow = {
        "Index": df.shape[0] + 1,
        "Quotes": quote,
        "Time": time_str,
        "Length": audio_length,
        "Submission": generate_time,
        "Download": "http://144.202.14.79/" + export_file_name,
        "Source": video_name,
        "Edits": edits,
    }

    df = df.append(newRow, ignore_index=True)
    df.to_csv(dfpath, sep="\t", index=False)

    print("execution ended")
    return "Entry added: " + dispstr
