#!/usr/bin/env python3

import numpy as np
import pydub
from pydub import AudioSegment

SPLIT_INTERVAL=20000 # 1000 ms or 1 sec

testfiles = ['2011', '2012']


def splitter(sound, sound_name):
    offset = 0
    file_index = 0
    l = len(sound)
    for i in range(0, l, SPLIT_INTERVAL):
        end = min(l, offset + SPLIT_INTERVAL)
        temp = sound[offset:end]
        offset = end

        temp.export('data/processed/{}_{}_{}.mp3'.format(sound_name, file_index, SPLIT_INTERVAL), format='mp3')

        file_index += 1

for testfile in testfiles: 
	splitter(AudioSegment.from_file('data/'+testfile+'.mp3'),testfile)
