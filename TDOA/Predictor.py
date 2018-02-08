'''
Created on Feb 7, 2018

used to predict direction of the sound source

@author: sadde
'''
from scipy.io.wavfile import read
import scipy
import numpy as np
import math

class predictor(object):
    '''
    use machine learning technique to calculate direction
    '''

    
    def __init__(self, filename):
        '''
        store value in self.sound
        '''
        self.filename = filename
    
    def time_difference(self, a,b):
        af = scipy.fft(a)
        bf = scipy.fft(b)
        c = scipy.ifft(bf * scipy.conj(af))
        time_shift = np.argmax(abs(c))
        return time_shift

    def time_difference_mics(self, file):
        time_differences_tracks = []
        origin_file_data = read(file)
        audio_data = np.array(origin_file_data[1],dtype=float)
        track_number = len(audio_data[0])
        audio_data = audio_data.T
        track_length = len(audio_data[0])
        for i in range(track_number):
            for j in range(i+1, track_number):
                temp_td = self.time_difference(audio_data[i], audio_data[j])
                if (track_length - temp_td) < temp_td:
                    temp_td = temp_td - track_length
                time_differences_tracks.append(temp_td)
        return time_differences_tracks
        
    def KNN_predict(self, test_val, train_val, train_label):
        
        distance = []
        test_val = np.array(test_val)
        for val in train_val:
            val = np.array(val)
            #print(np.linalg.norm(test_val-val, ord=1))
            distance.append(np.linalg.norm(test_val-val, ord=1))
        
        return train_label[distance.index(min(distance))]
        
        