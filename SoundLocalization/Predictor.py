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
        
    # This returns a three layer neural network with definable network topology
    # get a net and the function adds bias weights for you
    def neural_network(self, inputnum, hiddenneuralnum, outputnum):
        syn0 = 2*np.random.random((inputnum+1, hiddenneuralnum)) - 1
        syn1 = 2*np.random.random((hiddenneuralnum, outputnum)) - 1
        net = {'hidden_layer': syn0, 'output_layer': syn1}
        
        return net
    
    # This returns a trained neural network and plot the loss along the way
    def train(self, net, epoch, activition_func, train_val, train_label):
        net0 = net.copy()
        # add bias to input
        train_val = np.array(train_val)
        b = np.ones(len(train_val))
        train_val = np.c_[b,train_val]
        # print(train_val.shape)
        train_label = np.array([train_label]).T
        # Batch Gradient Descent
        for i in range(1, epoch):
            x = np.dot(train_val, net0['hidden_layer'])
            l1 = activition_func(x)
            # print(l1.shape)
            '''
            # add bias unit to the second layer
            b = np.ones(len(l1))
            l1 = np.c_[b,l1]
            # print('l1:',l1.shape)
            '''
            x = np.dot(l1, net0['output_layer'])
            l2 = activition_func(x)
            # print(l2.shape)
            # backward propagation
            l2_error = train_label - l2
            # print loss every 100 epoch
            if (i%200) == 0:
                print(np.mean(np.abs(l2_error)))
                
            l2_delta = l2_error*(l2*(1-l2)) # gradient of matrix
            # print('l2_delta:',l2_delta.shape)
            l1_delta = l2_delta.dot(net0['output_layer'].T)*(l1*(1-l1))
            # print('l1_delta:',l1_delta.shape)
            net0['output_layer'] += 0.1*l1.T.dot(l2_delta)
            # print('train_val:',train_val.T.shape)
            # be careful, the bias unit's delta does not propagate back
            net0['hidden_layer'] += 0.1*train_val.T.dot(l1_delta)
            
        return net0
    
    # The sigmoid function or you can write it in lambda func
    def sigmoid(self, x):
        return 1/(1+np.exp(-x))
    
    # The relu function
    def relu(self, x):
        return np.max(0, x) # needs correction!!! wrong

    # This returns the guess based on trained net
    def MLP_guess(self, net, test_val, activition_func):
        # add bias to input
        test_val = np.array([test_val])
        b = np.ones(1)
        test_val = np.c_[b,test_val]
        
        x = np.dot(test_val, net['hidden_layer'])
        l1 = activition_func(x)
        '''
        # add bias unit to the second layer
        b = np.ones(len(l1))
        l1 = np.c_[b,l1]
        '''
        x = np.dot(l1, net['output_layer'])
        l2 = activition_func(x)
        guess = l2
        return guess*190
