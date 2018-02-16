'''
Created on Feb 7, 2018

used to predict direction of the sound source

@author: sadde
'''
from scipy.io.wavfile import read
import scipy
import numpy as np
import math
import json

class predictor(object):
    '''
    use machine learning technique to calculate direction
    '''

    
    def __init__(self):
        '''
        lalala
        '''
    
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
        print(audio_data)
        for i in range(track_number):
            for j in range(i+1, track_number):
                temp_td = self.time_difference(audio_data[i], audio_data[j])
                if (track_length - temp_td) < temp_td:
                    temp_td = temp_td - track_length
                time_differences_tracks.append(temp_td)
        return time_differences_tracks

    def time_difference_mics_inputlist(self, audio_data):
        time_differences_tracks = []
        '''
        track_number = len(audio_data[0])
        audio_data = audio_data.T
        track_length = len(audio_data[0])
        '''
        track_number = audio_data.shape[0]
        track_length = audio_data.shape[1]
        for i in range(track_number):
            for j in range(i+1, track_number):
                temp_td = self.time_difference(audio_data[i], audio_data[j])
                # this makes we get the reasonable time difference
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

    def readdata(self, train_val_name, train_labels_name):
        train_val = []
        train_labels = []

        with open(train_val_name, 'r') as f:
            data = f.readlines()
            for line in data:
                train_val.append(json.loads(line))

        with open(train_labels_name, 'r') as f:
            data = f.readlines()
            for line in data:
                train_labels.append(json.loads(line))

        return train_val, train_labels
        
        
