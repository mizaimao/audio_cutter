"""Helper function and small modules."""

from typing import List

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