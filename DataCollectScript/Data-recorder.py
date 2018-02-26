'''
Created on Jan 25, 2018

playground is for obtaining all kinds of sound and save them into separate pieces of file

@author: sadde
'''

from pyaudio import PyAudio, paInt16
import numpy as np
from datetime import datetime
import wave
import time
from os import makedirs, path,chdir
import sys
import pdb


def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(4)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes(b"".join(data))
    wf.close()
    
def print_callback(in_data, frame_count, time_info, status):
    print(1)    
    
NUM_SAMPLES = 2000 # size of PyAudio chunk
SAMPLING_RATE = 44100 # sampling rate
LEVEL = 1800 # threshold for recording
COUNT_NUM = 10 # in the NUM_SAMPLE samples, if COUNT_NUM samples' value bigger than LEVEL, then record
SAVE_LENGTH = 3 # the smallest record length = SAVE_LENGTH*NUM_SAMPLES

# audio stream on
pa = PyAudio()
stream = pa.open(format=paInt16, channels=4, rate=SAMPLING_RATE,
                 input=True, input_device_index=6,
                 frames_per_buffer=NUM_SAMPLES)
for yan in range(186,362,2):
    fname = str(yan)
    newpath = path.join(sys.path[0], fname)
    print newpath
    if not path.exists(newpath):
        makedirs(newpath)
    chdir(newpath)
    save_count = 0
    save_buffer = []
    # t = datetime.now()
    savednum = 0
    while savednum <= 8: # (t.now().minute-t.minute)<9:
        #print(t.now().minute-t.minute)
        # read NUM_SAMPLES samples
        
        string_audio_data = stream.read(NUM_SAMPLES, exception_on_overflow = False)
        
        # transfer string from data document into array structure
        audio_data = np.fromstring(string_audio_data, dtype=np.short)
        
        # calculate how many samples have value bigger than LEVEL
        large_sample_count = np.sum(audio_data > LEVEL )
        #print (np.max(audio_data))
        if np.max(audio_data)>2000:
            # print (t.now())
            print (np.max(audio_data))
            print(np.min(audio_data))
            print(audio_data[1:7])
        # if there's enough sample bigger than COUNT_NUM, save at least SAVE_LENGTH blocks
        if large_sample_count > COUNT_NUM:
            save_count = SAVE_LENGTH
        else:
            save_count -= 1
        
        if save_count < 0:
            save_count = 0
            
        if save_count > 0:
            # save the block into save_buffer
            save_buffer.append(string_audio_data)
            
        else:
            # write save_buffer into WAV, WAV file's name is the time when it is saved
            if len(save_buffer) > 0:
                filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".wav" 
                save_wave_file(filename, save_buffer)
                save_buffer = []
                savednum += 1
                print(filename, savednum, 'saved')
    pdb.set_trace()
    
stream.close()
pa.terminate()
