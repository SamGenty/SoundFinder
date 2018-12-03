import pyaudio
from wavecalculations import WaveCalculations
from triangleplot import TrianglePlot
from bmicaudio import Mic

'''
Author: Samuel Genty
School: Texas A&M University
Date: 11/27/2018
Computer Science and Engineering 18'

##################################

Description:
This python script contains the testing methods that carry out the audio analysis
of the audio files coming in from the Mic objects.

##################################

Audio Analysis Step / Design:
	1. First read in the USB microphones hardware index value and save them
	2. Instantiate the Mic Objects and setup the threads for recording
	3. Begin the recordings of 2 microphones at a time
			- Mic 1 and 2 record first
			- Mic 1 and 3 record second
			- Mic 2 and 3 record last
	4. Each audio file is saved and the TDOA is calculated using fast fourier transforms
	5. Using these calculated TDOA values from each pair of mic recordings, we can accurately determine which
			mic is closest to the sound being made in the environment
	6. Once we know the closest mic to the sound, we then take the ratio of the other two microphones peak amplitude
			and then estimate where on the triangle visualization and display the result 

#######################################
'''


def determineDirection(offset1, offset2, mic1, mic2):
	if(offset1== offset2):
		print("Sounds are equidistant !")
		return 4
	if (offset1 > offset2):
		print("Sound is closer to mic"+str(mic1)+"\n")
		return mic1
	else:
		print("Sound is closer to mic"+str(mic2)+"\n")
		return mic2

def fromWhere(a,b,c):
	if a == b:
		print("sound hit mic1 first")
		return a
	if b == c:
		print("sound hit mic3 first")
		return b
	if a == c:
		print("Sound hit mic2 first")
		return a
	print("Inconsistent sound location!")
	return 0

def pinpointQuadrant(w1, w2, x, y):
	ratio = w1.maxx / w2.maxx
	arr = [[9.5,20], [7.64, 16], [3.77,9.30], [0,3], [5,4.7], [13.8,4.5], [20, 3.5], [17.5, 9.4], [13, 16.8]]
	if(x==2 and y==3):
		if(ratio > 1.1):
			return arr[1]
		elif(ratio < 1.1 and ratio > 0.9):
			return arr[0]
		else:
			return arr[8]
	if(x == 1 and y == 3):
		if(ratio > 1.1):
			return arr[2]
		elif(ratio < 1.1 and ratio > 0.9):
			return arr[3]
		else:
			return arr[4]
	if(x == 1 and y == 2):
		if(ratio > 1.1):
			return arr[7]
		elif(ratio < 1.1 and ratio > 0.9):
			return arr[6]
		else:
			return arr[5]
	return[9.5,10]


def main():
	p = pyaudio.PyAudio()
	mic1_index = 0
	mic1_name = ''
	mic2_index = 0
	mic2_name = ''
	mic3_index = 0
	mic3_name = ''

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
		if('Audio' in str(dev['name']) and count == 1):
			mic2_name = count + 1
			mic2_index = i
			count  = count + 1
			continue
		if('Audio' in str(dev['name']) and count == 2):
			mic3_name = count + 1
			mic3_index = i
			count  = count + 1
			break

	print("There are "+str(count)+" mics connected")


	# Instantiate the Mic objects
	mic1 = Mic(mic1_index, mic1_name, save_file=False)
	mic2 = Mic(mic2_index, mic2_name, save_file=False)
	mic3 = Mic(mic3_index, mic3_name, save_file=False)
	

	for i in range(100):
		print("Beginning test : "+str(i))
		#Record mic 1 and mic 2 pair
		mic1.setup()
		mic2.setup()
		mic1.startthread()
		mic2.startthread()
		mic1.jointhread()
		mic2.jointhread()
		t1_data1 = mic1.data
		t1_data2 = mic2.data
		aa1 = mic1
		bb1 = mic2
		
		#Record mic 1 and mic 3 pair
		mic1.setup()
		mic3.setup()
		mic1.startthread()
		mic3.startthread()
		mic1.jointhread()
		mic3.jointhread()
		aa2= mic1
		cc2 = mic3
		
		t2_data1 = mic1.data
		t2_data3 = mic3.data
		
		#Record mic 2 and mic 3 pair
		mic2.setup()
		mic3.setup()
		mic2.startthread()
		mic3.startthread()
		mic2.jointhread()
		mic3.jointhread()
		t3_data2 = mic2.data
		t3_data3 = mic3.data
		bb3 = mic2
		cc3 = mic3
			
		t1 = WaveCalculations("wave1", "wave2", t1_data1, t1_data2)
		t2 = WaveCalculations("wave1", "wave3", t2_data1, t2_data3)
		t3 = WaveCalculations("wave2", "wave3", t3_data2, t3_data3)
		
		t1r = WaveCalculations("wave2", "wave1", t1_data2, t1_data1)
		t2r = WaveCalculations("wave3", "wave1", t2_data3, t2_data1)
		t3r = WaveCalculations("wave3", "wave2", t3_data3, t3_data2)
		
		# wave 1 and 3 offset
		a1 = t1.findDifference()
		b1 = t2.findDifference()
		c1 = t3.findDifference()
		
		# wave 2 and 3 offset
		ar1 = t1r.findDifference()
		br1 = t2r.findDifference()
		cr1 = t3r.findDifference()
		

		r1 = determineDirection(ar1, a1, 1, 2)
		r2 = determineDirection(br1, b1, 1, 3)
		r3 = determineDirection(cr1, c1, 2, 3)

		soundlocation_index = fromWhere(r1,r2,r3)
		x = [0,0]
		if(soundlocation_index == 1):
			x = pinpointQuadrant(bb3, cc3, 2, 3)
		elif(soundlocation_index == 2):
			x = pinpointQuadrant(aa2, cc2, 1, 3)
		else:
			x = pinpointQuadrant(aa1, bb1, 1, 2)
		TrianglePlot(x)

# Detect the same signal by all microphones?

main()


