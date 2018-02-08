'''
Created on Feb 7, 2018

@author: sadde
'''

from Predictor import *
import sys
from os import listdir, makedirs, chdir
from os.path import join
import re
from soundetector import *
import matplotlib.pyplot as plt
from collections import deque

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
        train_val.append(features)
        train_label.append(i*5)
        print(features, i*5)

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

