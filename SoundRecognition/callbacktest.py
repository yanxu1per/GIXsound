from pyaudio import PyAudio, paInt16, paContinue
import numpy as np
from datetime import datetime
import wave
import time
from Predictor import *
import snowboydecoder
import sys
import signal
import time
import pdb
interrupted = False

NUM_SAMPLES = 2000 # size of PyAudio chunk
SAMPLING_RATE = 44100 # sampling rate
LEVEL = 3000 # threshold for recording
COUNT_NUM = 260 # in the NUM_SAMPLE samples, if COUNT_NUM samples' value bigger than LEVEL, then record
SAVE_LENGTH = 3 # the smallest record length = SAVE_LENGTH*NUM_SAMPLES

save_count=0

#my
def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]



detector = snowboydecoder.HotwordDetector(model, sensitivity=0.65)
#myend

train_val = []
train_labels = []
possible_sound = 0

with open('train_val.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        train_val.append(json.loads(line))

with open('train_label.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        train_labels.append(json.loads(line))



class RingBuffer(object):
    """Ring buffer to hold audio from PortAudio"""
    def __init__(self, size = 4096):
        self._buf = collections.deque(maxlen=size)

    def extend(self, data):
        """Adds data to the end of buffer"""
        self._buf.extend(data)

    def get(self):
        """Retrieves data from the beginning of buffer and clears it"""
        tmp = bytes(bytearray(self._buf))
        self._buf.clear()
        return tmp

sound_piece = np.array([])
sound_piece_wav = []
def print_callback(in_data, frame_count, time_info, status):
    #print(1)
    global possible_sound
    global save_count
    global sound_piece
    global sound_piece_wav
    audio_data = np.fromstring(in_data, dtype=np.short)
    
    large_sample_count = np.sum(audio_data > LEVEL )

    if large_sample_count > COUNT_NUM:
        save_count = SAVE_LENGTH
    else:
        save_count -= 1
    
    if save_count < 0:
        save_count = 0
        
    if save_count > 0:
        # save the block into save_buffer
        sound_piece = np.append(sound_piece, audio_data)
        sound_piece_wav.extend(in_data)
        possible_sound = 0
    else:
        possible_sound = 1
    return chr(0), paContinue

# audio stream on
pa = PyAudio()
stream = pa.open(format=paInt16, channels=4, rate=SAMPLING_RATE,
                 input=True, input_device_index=6,
                 frames_per_buffer=NUM_SAMPLES,
                 stream_callback=print_callback)

stream.start_stream()
while stream.is_active():
    
    data = sound_piece.copy()   
    if len(data) > 0 and possible_sound:
        data.shape = -1,4
        data = data.T
        predict = predictor()
        
        test_val = predict.time_difference_mics_inputlist(data)
        #print(test_val)
        if max(test_val)<=11:
            
            #sound4_list =[[],[],[],[]]
            # 
            sound4_list =[[],[],[],[]]            
            #print(len(sound_piece_wav))
            for i in range(len(sound_piece_wav)):
                sound4_list[i%4].extend(sound_piece_wav[i])
            #print(len(sound4_list[1]))
            data=''.join(sound4_list[1])
            
            #help recognition
            ans=detector.detect(data,
               sleep_time=0.03)
            print ans
            if ans==1:
                test_val[:] = [float(x)/11 for x in test_val]
                guess = predict.KNN_predict(test_val, train_val, train_labels)
                print('guess:', guess)
        else:
            print('Try again!')
        sound_piece = np.array([])
        sound_piece_wav = []
    #else:      
       #time.sleep(0.05)
       #print(len(data))
stream.stop_stream()
stream.close()
pa.terminate()
