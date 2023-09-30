#!/usr/bin/env python3

import pandas as pd
import numpy as np
import pydub
from pydub import AudioSegment
import datetime


SPLIT_INTERVAL=20000

audioPath = 'data/sample.aac'
testInterval = '0:30-1:3'

dfpath='data/export.csv'


def formatter_lv1(singleTS):
    tmpTS = []
    try: tmpTS = singleTS.split(':')
    except: raise ValueError('input error')
    lenTmpTs = len(tmpTS)
    totalmsec = 0
    formatted_str = ''

    if lenTmpTs == 3:
        totalmsec += int(tmpTS[0]) * 60 * 1000 + int(tmpTS[1]) * 1000 + int(tmpTS[2])
        formatted_str = '{:02d}:'.format(int(tmpTS[0])) + '{:02d}'.format(int(tmpTS[1])) 
    elif lenTmpTs == 2:
        totalmsec += int(tmpTS[0]) * 60 * 1000 + int(tmpTS[1]) * 1000
        formatted_str = '{:02d}:'.format(int(tmpTS[0])) + '{:02d}'.format(int(tmpTS[1])) 
    elif lenTmpTs == 1:
        totalmsec += int(tmpTS[0]) * 1000
        formatted_str = '00:' + '{:02d}'.format(int(tmpTS[0])) 
    
    else:
        raise ValueError('input error')

    return totalmsec, formatted_str


def formatter_lv0(timestring):
    if len(timestring) > 50:
        raise ValueError('too long')
    tmpstr = []
    try: tmpstr = timestring.split('-')
    except: raise ValueError('''must include '-' ''')
    assert len(tmpstr) == 2

    start, startstr = formatter_lv1(tmpstr[0])
    end, endstr = formatter_lv1(tmpstr[1])
    assert end > start

    return start, end, startstr+'-'+endstr




def file_finder(start, end, video_name):
    start_file = start // SPLIT_INTERVAL
    start_point = start % SPLIT_INTERVAL

    end_file = end // SPLIT_INTERVAL
    end_point = end % SPLIT_INTERVAL

    sound = AudioSegment.from_file('data/processed/{}_{}_{}.mp3'.format(video_name, start_file, SPLIT_INTERVAL))

    if start_file == end_file:
        return sound[start_point:end_point+1]        
    elif start_file < end_file:
        sound = sound[start_point:]
        left = start_file + 1 
        while left <= end_file:
            temp = AudioSegment.from_file('data/processed/{}_{}_{}.mp3'.format(video_name, left, SPLIT_INTERVAL))
            if left == end_file:
                temp = temp[:end_point]
            sound += temp
            left += 1
        return sound
    else:
        exit(1)
    


def cutter(video_name, timestr, quote, mono, edits):
    if not timestr:
        return True
    edits = max(0, int(edits))
    start, end, dispstr = formatter_lv0(timestr.replace(' ',''))
    
    export_file_name = dispstr.replace(':','_') + '_{}'.format(video_name) + ('_{}'.format(str(edits)) if edits else '') + '.mp3'

    # Determinant step
    interested = file_finder(start, end, video_name)
    try:
        interested.export('data/export/'+export_file_name, format='mp3')
    except:
        exit(1)
    
    # Adding entry to table
    currentDT = datetime.datetime.now()
    generate_time = currentDT.strftime("%m/%d/%Y %H:%M:%S")
    audio_length = '{:10.2f}'.format((end-start)/1000) +'s'
    # Index,Quotes,Time,Length,Submission,Download,Source
    df = pd.read_csv(dfpath,sep='\t')
    
    newRow = {'Index': df.shape[0]+1,
            'Quotes': quote,
            'Time': timestr,
            'Length':audio_length,
            'Submission':generate_time,
            'Download':'http://144.202.14.79/' + export_file_name,
            'Source': video_name,
            'Edits': edits,
            }

    df = df.append(newRow,ignore_index=True)
    df.to_csv(dfpath, sep='\t', index=False)

    print('execution ended')
    return 'Entry added: ' + dispstr

