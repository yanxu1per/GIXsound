from scipy.io.wavfile import read
import scipy
import numpy as np
import math

#using cross crelation. input two similar signal wave, yield b - a index 
def time_difference(a,b):
	af = scipy.fft(a)
	bf = scipy.fft(b)
	c = scipy.ifft(bf * scipy.conj(af))
	time_shift = np.argmax(abs(c))
	return time_shift
#test time difference
#a21=np.array([0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 0, 0, 0, 0, 0])
#a22=np.array([0, 0, 0, 0, 0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 0])
# print(len(audio_data[0]))
#print(time_difference(a21,a22))

#input file name,  an 2d array x:time  y:track number
def time_difference_mics(file):
	time_differences_tracks = []
	origin_file_data = read(file)
	audio_data = np.array(origin_file_data[1],dtype=float)
	print(audio_data[0])
	track_number = len(audio_data[0])
	audio_data = audio_data.T
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


Frequency = 44100
SoundSpeed = 340
def degree_from_TDOA(d2mic_dic,d = 0.06):
	mic1 = d2mic_dic['mic1']
	mic2 = d2mic_dic['mic2']
	theta = math.acos((d2mic_dic['td']/Frequency) * 340 / d) - math.pi/4
	temp_degree =  theta/math.pi * 180
	if ( (mic1+1) == mic2) or (mic1==4 and mic2 == 1):
		degree = (mic1 - 1) * 90 + temp_degree
	else:
		degree = mic2 * 90 - temp_degree
	return degree


# a.append(read("2018-02-06_20_28_46.wav"))
# a.append(read("2018-02-06_20_28_47.wav"))
# a.append(read("2018-02-06_20_28_48.wav"))

td_array = time_difference_mics("2018-02-08_01_16_34.wav")
print(degree_from_TDOA(closest_2mics_td(td_array)))
print(td_array)
