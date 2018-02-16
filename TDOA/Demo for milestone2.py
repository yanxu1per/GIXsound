'''
Created on Jan 25, 2018

playground is for obtaining all kinds of sound and save them into separate pieces of file

@author: sadde
'''
from Predictor import *
from pyaudio import PyAudio, paInt16
import numpy as np
from datetime import datetime
import wave
import time

from scipy.io.wavfile import read
import scipy
import math
import wave

#using cross crelation. input two similar signal wave, yield b - a index 
def time_difference(a,b):
	af = scipy.fft(a)
	bf = scipy.fft(b)
	c = scipy.ifft(bf * scipy.conj(af))
	time_shift = np.argmax(abs(c))
	return time_shift

#input array,  an 2d array x:time  y:track number
def time_difference_mics(audio_data):
	time_differences_tracks = []
	track_number = len(audio_data)
	track_length = len(audio_data[0])
	for i in range(track_number):
		for j in range(i+1, track_number):
			temp_td = time_difference(audio_data[i], audio_data[j])
			if (track_length - temp_td) < temp_td:
				temp_td = temp_td - track_length
			time_differences_tracks.append(temp_td)
	return time_differences_tracks

#only based on 4mics
tdoa_array_index_dictionary = {'12':0, '13':1, '14':2, '23':3, '24':4, '34':5}
def closest_2mics_td(tdoa_array):
	d2mic_dic ={'mic1':0, 'mic2':0, 'td':0}
	position_dic = {1:0, 2:tdoa_array[0], 3:tdoa_array[1], 4:tdoa_array[2]}
	temp = zip(position_dic.values(),position_dic.keys())
	ordered_dic = sorted(temp)
	d2mic_dic['mic1'] = ordered_dic[0][1] 
	d2mic_dic['mic2'] = ordered_dic[1][1]
	key_string = str(ordered_dic[0][1])+str(ordered_dic[1][1]) if ordered_dic[1][1] > ordered_dic[0][1] else str(ordered_dic[1][1])+str(ordered_dic[0][1])
	d2mic_dic['td'] = tdoa_array[tdoa_array_index_dictionary[key_string]]
	return d2mic_dic

Frequency = 441000
SoundSpeed = 340
def degree_from_TDOA(d2mic_dic,d = 0.06):
	mic1 = d2mic_dic['mic1']
	mic2 = d2mic_dic['mic2']
	theta = math.acos((abs(d2mic_dic['td'])/Frequency) * 340 / d) - math.pi/4
	temp_degree =  theta/math.pi * 180
	if ( (mic1+1) == mic2) or (mic1==4 and mic2 == 1):
		degree = (mic1 - 1) * 90 + temp_degree
	else:
		degree = mic2 * 90 - temp_degree
	return degree

def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(4)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes(b"".join(data))
    wf.close()
    
def getsoundval(file):
    wf =  wave.open(file,"rb")
    params = wf.getparams()
    framesra,frameswav= params[2],params[3]
    datawav = wf.readframes(frameswav)
    wf.close()
    datause = np.fromstring(datawav,dtype = np.short)
    #print('data size:',datause.size)
    datause.shape = -1,4
    datause = datause.T
        #time = np.arange(0, frameswav)
        #time = np.arange(0, frameswav) * (1.0/framesra)       
    return datause  
    
NUM_SAMPLES = 2000 # size of PyAudio chunk
SAMPLING_RATE = 44100 # sampling rate
LEVEL = 2000 # threshold for recording
COUNT_NUM = 10 # in the NUM_SAMPLE samples, if COUNT_NUM samples' value bigger than LEVEL, then record
SAVE_LENGTH = 3 # the smallest record length = SAVE_LENGTH*NUM_SAMPLES

# audio stream on
pa = PyAudio()
stream = pa.open(format=paInt16, channels=4, rate=SAMPLING_RATE, input=True, input_device_index=6, frames_per_buffer=NUM_SAMPLES)


save_count = 0
save_buffer = []
# t = datetime.now()
savednum = 0
while savednum <= 20: # (t.now().minute-t.minute)<9:
    # read NUM_SAMPLES samples
    
    string_audio_data = stream.read(NUM_SAMPLES, exception_on_overflow =False)
    
    # transfer string from data document into array structure
    audio_data = np.fromstring(string_audio_data, dtype=np.short)
    
    # calculate how many samples have value bigger than LEVEL
    large_sample_count = np.sum(audio_data > LEVEL )
    #print (np.max(audio_data))
    #if np.max(audio_data)>2000:
        # print (t.now())
        #print (np.max(audio_data))
        #print(np.min(audio_data))
        #print(audio_data[1:7])
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
        time.sleep(0.03)    
    else:
        # write save_buffer into WAV, WAV file's name is the time when it is saved
        if len(save_buffer) > 0:
            filename = "now"+ ".wav" 
            save_wave_file(filename, save_buffer)
            #print(len("".join(save_buffer)))
            #audio_data = [[],[],[],[]]
            in_data_np = np.fromstring("".join(save_buffer), dtype=np.short)
            #for j in range(len(in_data_np)):
            #    audio_data[j%4].append(in_data_np[j])
            data = getsoundval("now.wav")
            td_array = time_difference_mics(data)
            print(degree_from_TDOA(closest_2mics_td(td_array)))
            save_buffer = []
            savednum += 1
            print(filename, savednum, 'saved')
            #predict = predictor(filename)
            #features = predict.time_difference_mics(predict.filename)
    
stream.close()
pa.terminate()
