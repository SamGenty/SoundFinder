from 3micaudio import Mic

def determineDirection(offset1, offset2, mic1, mic2):
	if(offset == offset):
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
	ratio = w1.max / w2.max
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


def main(angleOfSound, numberOfIterations):
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
	mic1 = Mic(mic1_index, mic1_name, save_file=True)
	mic2 = Mic(mic2_index, mic2_name, save_file=True)
	mic3 = Mic(mic3_index, mic3_name, save_file=True)
	
	foldern = str(angleOfSound)+"degTests/"
	file = open(foldern+str(angleOfSound)+"degrees.csv","w")
	file.write(str(angleOfSound)+"testid,w2:w1,w3:w1,w3:w2,w1:w2,w1:w3,w2:w3,w1avg,w1min,w3max,w2avg,w2min,w2max,w3avg,w3min,w3max\n")

	for i in range(100):
		print("Beginning test : "+str(i))
		

		#First, do mic 1 and mic 2 pair
		mic1.setup()
		mic2.setup()
		mic1.startthread()
		mic2.startthread()
		mic1.jointhread()
		mic2.jointhread()
		t1_data1 = mic1.data
		t1_data2 = mic2.data

		#Second, do mic 1 and mic 3 pair
		mic1.setup()
		mic3.setup()
		mic1.startthread()
		mic3.startthread()
		mic1.jointhread()
		mic3.jointhread()
		t2_data1 = mic1.data
		t2_data3 = mic3.data

		#Third, do mic 2 and mic 3 pair
		mic2.setup()
		mic3.setup()
		mic2.startthread()
		mic3.startthread()
		mic2.jointhread()
		mic3.jointhread()
		t3_data2 = mic2.data
		t3_data3 = mic3.data

			
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

		if(soundlocation_index == 1):
			x = pinpointQuadrant(t3_data2, t3_data3, 2, 3)
		elif(soundlocation_index == 2):
			x = pinpointQuadrant(t2_data1, t2_data3, 1, 3)
		else:
			x = pinpointQuadrant(t1_data1, t1_data2, 1, 2)





		'''
		file.write(str(i)+","+str(a1)+","+str(b1)+","+str(c1)+","+str(ar1)+","+str(br1)+","+str(cr1)+","+str(mic1.avg)+","+str(mic1.min)+","+str(mic1.max)+","+str(mic2.avg)+","+str(mic2.min)+","+str(mic2.max)+","+str(mic3.avg)+","+str(mic3.min)+","+str(mic3.max)+"\n")
		
		# Save each wav file from each microphone for later analysis
		mic1.fileName = foldern+"mic1wave_"str(i)+".wav"
		mic2.fileName = foldern+"mic2wave_"str(i)+".wav"
		mic3.fileName = foldern+"mic3wave_"str(i)+".wav"

		mic1.savefile()
		mic2.savefile()
		mic3.savefile()
		'''

# Detect the same signal by all microphones?

main()


#mic1wave_1
#mic2wave_1
#mic3wave_1
