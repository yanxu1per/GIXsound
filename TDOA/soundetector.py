'''
Created on Jan 27, 2018

@author: sadde
'''
import numpy as np
from datetime import datetime
from math import exp
from collections import deque
class soundetector(object):
    '''
    a class that contains all kinds of sound detection method,
    read wave file only!
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        # some lambda functions help us to transform frames and microsecond from one to the other
        self.microsecond2frame = lambda samplingrate, microsecond : int(samplingrate*microsecond/1000)
        self.frame2microsecond = lambda samplingrate, frames : frames/samplingrate*1000
        
        # lambda function to calculate the amplitude of the current point
        self.amplitude = lambda waveval: abs(waveval)
    def echofree(self, init_sound_strength, echo_delay, echo_decay, sound):
        '''
        echofree is a method to detect all the echo free sound within
        the last storedlength stream. It returns each echo free sound's
        starting and ending points.
        
        init_sound_strength, echo_delay, echo_decay are the three parameters
        that determine the characteristic of the system reaction.
        '''
        # a list which labels all the echo free parts within the last period
        arrivaltimemap = []
        soundlength = len(sound)
        abssound = [self.amplitude(sound[i]) for i in range(0,soundlength)]
        echomap = [self.echo_val(init_sound_strength, echo_delay, echo_decay,abssound[i-280:i]) for i in range(280, soundlength)]
        echofreemap = [abssound[i]>echomap[i]*7 for i in range(0, soundlength-280)]
        for i, val in enumerate(echofreemap):
            if i >= 2 and echofreemap[i-1] == 0 and val == 1:
                arrivaltimemap.append(1)
            else:
                arrivaltimemap.append(0)
        
        return arrivaltimemap, abssound, echofreemap ,echomap
    
    def absound(self, soundwave):
        absound = [self.amplitude(soundwave[i]) for i in range(0,len(soundwave))]
        return absound
    # a prospective pattern of the strength of echoes after a impulsive stimulus
    def h(self, init_sound_strength, echo_delay, echo_decay, t):
        '''
        init_sound_strength, echo_delay, echo_decay are the three parameters
        that determine the characteristic of the system reaction.
        echo_delay in microseconds, echo_decay in seconds
        '''
        if t<echo_delay:
            return 0
        else:
            h = lambda init_sound_strength, echo_delay, echo_decay, t : (init_sound_strength*
                                                                     exp(-(t-echo_delay)/echo_decay))
            return h(init_sound_strength, echo_delay, echo_decay, t)
    
    def echo_val(self, init_sound_strength, echo_delay, echo_decay, echopiece):
        '''
        form_length is the frame length period of measuring echo level 
        echopiece is the sound piece used to calculate echo level, it's a list
        '''
        echoval = 0
        # convolution of the soundpiece
        
        #print(len(echopiece))
        length = len(echopiece)
        for i, waveval in enumerate(echopiece):
            #print(i)
            t = self.frame2microsecond(44100, length-i)
            if t < echo_delay:
                break
            echoval += self.amplitude(waveval)*self.h(init_sound_strength, echo_delay, echo_decay, t)

            
        #print(echoval)
        return echoval
    # locate local max return the local maximal index in a list
    def locatelocmax(self, threshold, sound):
        noteindex = []
        abovethresh = []
        relativeindex = 0
        startflag = False
        for i, val in enumerate(sound):
            if val < threshold:
                if startflag is True:
                    noteindex.append(relativeindex+abovethresh.index(max(abovethresh)))
                    abovethresh = []
                relativeindex = i
                
                startflag = False
            else:
                startflag = True
                abovethresh.append(val)
        
        notelist = self.makenote(len(sound),noteindex)
        
        return notelist
    
    # makenote note 1 where the input index indicate
    def makenote(self, length, noteindex):
        notelist = []
        if noteindex != []:
            tmp = noteindex.pop(0)
        for i in range(0,length):
            if i == tmp:
                notelist.append(1)
                if noteindex != []:
                    tmp = noteindex.pop(0)
            else:
                notelist.append(0)
        
        
        return notelist
    
    # return the TDOA base on input dictionar, which has 4 channels' arrival feature
    def TDOA(self, arrivalmap):
        tdoalist = []
        length = len(arrivalmap[0])
        
        slidingwindow1 = deque(maxlen=70)
        slidingwindow2 = deque(maxlen=70)
        slidingwindow3 = deque(maxlen=70)
        slidingwindow4 = deque(maxlen=70)
        i = 0
        while i < length:
            # push one value in window each time
            slidingwindow1.append(arrivalmap[0][i])
            slidingwindow2.append(arrivalmap[1][i])
            slidingwindow3.append(arrivalmap[2][i])
            slidingwindow4.append(arrivalmap[3][i])
            i += 1
            '''
            # exam if the sliding windows are ready to return TDOA
            if 1 not in slidingwindow1[0:30] and 1 not in slidingwindow2[0:30] and 1 not in slidingwindow3[0:30] and 1 not in slidingwindow4[0:30]:
                if 1 in slidingwindow1[30:41] and 1 not in slidingwindow2[30:41] and 1 not in slidingwindow3[30:41] and 1 not in slidingwindow4[30:41]:
                    if 1 not in slidingwindow1[41:70] and 1 not in slidingwindow2[41:70] and 1 not in slidingwindow3[41:70] and 1 not in slidingwindow4[41:70]:
                    # return the index where the sound arrived
                        t1 = slidingwindow1[30:41].index(1)
                        t2 = slidingwindow2[30:41].index(1)
                        t3 = slidingwindow3[30:41].index(1)
                        t4 = slidingwindow4[30:41].index(1)
                        tdoalist.append([t1-t2,t2-t3,t3-t4,t4-t1,t1-t3,t2-t4])
                        i += 150
                        slidingwindow1 = deque(maxlen=70)
                        slidingwindow2 = deque(maxlen=70)
                        slidingwindow3 = deque(maxlen=70)
                        slidingwindow4 = deque(maxlen=70)
                
                
        return tdoalist
        
        '''