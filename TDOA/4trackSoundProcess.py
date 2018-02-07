from scipy.io.wavfile import read
import scipy
import numpy as np

#using cross crelation. input two similar signal wave, yield b - a index 
def time_difference(a,b):
	af = scipy.fft(a)
	bf = scipy.fft(b)
	c = scipy.ifft(bf * scipy.conj(af))
	time_shift = np.argmax(abs(c))
	return time_shift
#test time difference
a21=np.array([0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 0, 0, 0, 0, 0])
a22=np.array([0, 0, 0, 0, 0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 0])
# print(len(audio_data[0]))
print(time_difference(a21,a22))

#input file name,  an 2d array x:time  y:track number
def time_difference_mics(file):
	time_differences_tracks = []
	origin_file_data = read(file)
	audio_data = np.array(origin_file_data[1],dtype=float)
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



def degree_from_TDOA(tdoa, distance):
	degree
	return degree


# a.append(read("2018-02-06_20_28_46.wav"))
# a.append(read("2018-02-06_20_28_47.wav"))
# a.append(read("2018-02-06_20_28_48.wav"))

td_array = time_difference_mics("2018-02-06_20_28_46.wav")
print(td_array)




