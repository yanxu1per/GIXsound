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
from Predictor import *
import sys
from os import listdir, makedirs, chdir
from os.path import join
import re
from soundetector import *
from collections import deque

def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(4)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes(b"".join(data))
    wf.close()

pattern = re.compile(r'.*\.wav')
originaldir = sys.path[0]
chdir(originaldir)

train_val = []
train_labels = []

with open('train_val.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        train_val.append(json.loads(line))

with open('train_label.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        train_labels.append(json.loads(line))

    
NUM_SAMPLES = 2000 # size of PyAudio chunk
SAMPLING_RATE = 44100 # sampling rate
LEVEL = 3000 # threshold for recording
COUNT_NUM = 260 # in the NUM_SAMPLE samples, if COUNT_NUM samples' value bigger than LEVEL, then record
SAVE_LENGTH = 1 # the smallest record length = SAVE_LENGTH*NUM_SAMPLES


save_count = 0
sound_piece = np.array([])
# t = datetime.now()
savednum = 0
# audio stream on
pa = PyAudio()
stream = pa.open(format=paInt16, channels=4, rate=SAMPLING_RATE, input=True, input_device_index=6, frames_per_buffer=NUM_SAMPLES)



while savednum <= 5: # (t.now().minute-t.minute)<9:
    #print(t.now().minute-t.minute)
    # read NUM_SAMPLES samples
    string_audio_data = stream.read(NUM_SAMPLES, exception_on_overflow = False)
    
    
    # transfer string from data document into array structure
    audio_data = np.fromstring(string_audio_data, dtype=np.short)
    
    # calculate how many samples have value bigger than LEVEL
    large_sample_count = np.sum(audio_data > LEVEL )
    #print (np.max(audio_data))
    #if np.max(audio_data)>2000:
    #    # print (t.now())
    #    print (np.max(audio_data))
    #    print(np.min(audio_data))
    #    print(audio_data[1:7])
    # if there's enough sample bigger than COUNT_NUM, save at least SAVE_LENGTH blocks
    if large_sample_count > COUNT_NUM:
        save_count = SAVE_LENGTH
    else:
        save_count -= 1
    
    if save_count < 0:
        save_count = 0
        
    if save_count > 0:
        # save the block into save_buffer
        sound_piece = np.append(sound_piece, audio_data)
        # print(len(sound_piece))
    else:
        # write save_buffer into WAV, WAV file's name is the time when it is saved
        if len(sound_piece) > 0:
            sound_piece.shape = -1,4
            sound_piece = sound_piece.T

            predict = predictor()
            test_val = predict.time_difference_mics_inputlist(sound_piece)
            sound_piece = np.array([])
            print(test_val)

            test_val[:] = [float(x)/11 for x in test_val]
            guess = predict.KNN_predict(test_val, train_val, train_labels)
            savednum += 1
            print('guess:', guess)
    print(savednum)
            
stream.close()
pa.terminate()


'''
from Predictor import *
import sys
from os import listdir, makedirs, chdir
from os.path import join
import re
from soundetector import *
from collections import deque

pattern = re.compile(r'.*\.wav')
originaldir = sys.path[0]
chdir(originaldir)

train_val = []
train_labels = []

with open('train_val.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        train_val.append(json.loads(line))

with open('train_label.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        train_labels.append(json.loads(line))

onlyfile = [f for f in listdir(originaldir) if pattern.match(f)]
for file in onlyfile:
        predict = predictor()
        #print(predict.filename)
        test_val = predict.time_difference_mics(file)
        print(test_val)
        
        test_val[:] = [float(x)/11 for x in test_val]
        guess = predict.KNN_predict(test_val, train_val, train_labels)
        print('guess:', guess)
'''
