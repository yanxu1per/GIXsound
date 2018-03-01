from pyaudio import PyAudio, paInt16, paContinue
import numpy as np
from datetime import datetime
import wave
import time
from Predictor import *
import socket

NUM_SAMPLES = 2000 # size of PyAudio chunk
SAMPLING_RATE = 44100 # sampling rate
LEVEL = 2000 # threshold for recording
COUNT_NUM = 260 # in the NUM_SAMPLE samples, if COUNT_NUM samples' value bigger than LEVEL, then record
SAVE_LENGTH = 1 # the smallest record length = SAVE_LENGTH*NUM_SAMPLES

save_count=0


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

#socket
obj = socket.socket()

obj.connect(("192.168.0.100",8098))
print('connected')
ret_bytes = obj.recv(1024)
ret_str = str(ret_bytes.encode("utf-8"))
obj.sendall(bytes("PI1".encode("utf-8")))
print(ret_str)

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

def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(4)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes(b"".join(data))
    wf.close()

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
        if max(test_val)<=11 and min(test_val)>=-11:
            '''
            #sound4_list =[[],[],[],[]]
            # 
            sound4_list =[[],[],[],[]]            
            print(len(sound_piece_wav))
            for i in range(len(sound_piece_wav)):
                sound4_list[i%4].extend(sound_piece_wav[i])
            print(len(sound4_list[1]))
            data=''.join(sound4_list[1])
            #help recognition
            '''
            test_val[:] = [float(x)/11 for x in test_val]
            features2 = predict.max_energy_mics_inputlist(data)
            features2 = [float(x) for x in features2]
            test_val.extend(features2)
            guess = predict.KNN_predict(test_val, train_val, train_labels, K=10)
            # print('guess:', guess)
            obj.sendall(bytes(("PI1_"+str(guess)).encode("utf-8")))
            
        #else:
            #print('Try again!')
        sound_piece = np.array([])
        sound_piece_wav = []
    #else:      
       #time.sleep(0.05)
       #print(len(data))
stream.stop_stream()
stream.close()
pa.terminate()
