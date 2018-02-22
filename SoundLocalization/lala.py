# -*- coding: utf-8 -*-
'''
Created on Feb 7, 2018

This program is used to train machine learning model for future prediction

@author: sadde
'''

from Predictor import *
import sys
from os import listdir, makedirs, chdir
from os.path import join
import re
#from soundetector import *
from collections import deque
import numpy as np
import random
'''
# get the training feature from wav files
pattern = re.compile(r'.*\.wav')
train_val = []
train_label = []
originaldir = sys.path[0]
for i in range(8,38):
    mypath = join(sys.path[0],str(i*5))
    chdir(mypath)
    onlyfile = [f for f in listdir(mypath) if pattern.match(f)]# [join(mypath,f) for f in listdir(mypath) if pattern.match(f)]
    print(onlyfile)
    for file in onlyfile:
        predict = predictor(file)
        #print(predict.filename)
        features = predict.time_difference_mics(predict.filename)
        train_val.append([float(x)/11 for x in features])
        train_label.append(i*5)
        print(features, i*5)
'''

'''
# test the KNN
chdir(originaldir)
onlyfile = [f for f in listdir(originaldir) if pattern.match(f)]
for file in onlyfile:
        predict = predictor(file)
        #print(predict.filename)
        test_val = predict.time_difference_mics(predict.filename)
        print(test_val)
        guess = predict.KNN_predict(test_val, train_val, train_label)
        print('guess:', guess)
'''


# prepare to train a MLP
predict = predictor()
'''
train_val = [[0,0,1],[0,1,1],[1,0,1],[1,1,1]]
train_labels = [0,1,1,0]
'''

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

# shuffle the training set, although its batch gradient descent, its easier to get test set
zipped = list(zip(train_val, train_labels))
random.shuffle(zipped)
unzipped = list(zip(*zipped))
train_val = unzipped[0]
train_labels = unzipped[1]
print(len(train_labels))
'''
# get a net
net = predict.neural_network(3,6,1)
# training via BGD
trained_net = predict.train(net, 50000, predict.sigmoid, train_val, train_labels)#train_val[:520], [x for x in train_labels[:520]])

# test training result
for i, test_val in enumerate(train_val):#train_val[520:]):
        print(predict.MLP_guess(trained_net, test_val, predict.sigmoid), train_labels[i])

'''
# get a net
net = predict.neural_network(6,6,1)
# training via BGD
trained_net = predict.train(net, 5000, predict.sigmoid, train_val[:520], [float(x)/190 for x in train_labels[:520]])

# test training result
for i, test_val in enumerate(train_val[520:]):
        print(predict.MLP_guess(trained_net, test_val, predict.sigmoid), train_labels[i])


'''
chdir(originaldir)
fileObject = open('train_val.txt', 'w')  
for ip in train_val:  
    fileObject.write(str(ip))  
    fileObject.write('\n')  
fileObject.close() 

fileObject = open('train_label.txt', 'w')  
for ip in train_label:  
    fileObject.write(str(ip))  
    fileObject.write('\n')  
fileObject.close()
'''

