import pyaudio
from realTimeAudio import LiveAudio


'''
Author: Samuel Genty
School: Texas A&M University
Date: 11/27/2018
Computer Science and Engineering 18'
'''

def main():
	p = pyaudio.PyAudio()
	mic1_index = 0
	mic1_name = ''

	# The following for loop is for printing plugged in Audio devices
	# Which ever audio device has the word USB in it is probably our microphone 
	count = 0
	for i in range(p.get_device_count()):
		dev = p.get_device_info_by_index(i)
		print(str(dev['name']))
		if('Audio' in str(dev['name']) and count == 0):
			mic1_index = i
			mic1_name = count + 1
			count  = count + 1
			continue
		
	#print(str(p.get_device_info_by_index(mic1_index)['defaultSampleRate']))
	print("There are "+str(count)+" mics connected")
	# def __init__(self, _index, _name, save_file = False, filename = "output"):

	a = LiveAudio(mic1_index)



main()
