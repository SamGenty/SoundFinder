from 3micaudio import Mic

def determineDirection(wave1offset, wave2offset, mic2, mic1):
	if (wave1offset > wave2offset):
		print("Sound is closer to mic"+str(mic2)+"\n")
	else:
		print("Sound is closer to mic"+str(mic1)+"\n")

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
	mic1 = Mic(mic1_index, mic1_name, save_file=True, filename = "mic1output.wav")
	mic2 = Mic(mic2_index, mic2_name, save_file=True, filename = "mic2output.wav")
	mic3 = Mic(mic3_index, mic3_name, save_file=True, filename = "mic3output.wav")
	
	foldern = str(angleOfSound)+"degTests/"
	file = open(foldern+str(angleOfSound)+"degrees.csv","w")
	file.write(str(angleOfSound)+"testid,w2:w1,w3:w1,w3:w2,w1:w2,w1:w3,w2:w3,w1avg,w1min,w3max,w2avg,w2min,w2max,w3avg,w3min,w3max\n")

	for i in range(100):
	
		#Setup threads for mics
		mic1.setup()
		mic2.setup()
		mic3.setup()

		#Start and stop threads here for each mic
		mic1.startthread()
		mic2.startthread()
		mic3.startthread()
		
		mic1.jointhread()
		mic2.jointhread()
		mic3.jointhread()
		

		data1 = mic1.data
		data2 = mic2.data
		data3 = mic3.data
		
		
		
		a = WaveCalculations("wave1", "wave2", data1, data2)
		b = WaveCalculations("wave2", "wave3", data2, data3)
		c = WaveCalculations("wave1", "wave3", data1, data3)
		
		ar = WaveCalculations("wave2", "wave1", data2, data1)
		br = WaveCalculations("wave3", "wave2", data3, data2)
		cr = WaveCalculations("wave3", "wave1", data3, data1)
		
		# wave 2 offset
		a1 = a.findDifference()
		b1 = b.findDifference()
		c1 = c.findDifference()
		
		# wave 1 offset
		ar1 = ar.findDifference()
		br1 = br.findDifference()
		cr1 = cr.findDifference()
		
		


		file.write(str(i)+","+str(a1)+","+str(b1)+","+str(c1)+","+str(ar1)+","+str(br1)+","+str(cr1)+","+str(mic1.avg)+","+str(mic1.min)+","+str(mic1.max)+","+str(mic2.avg)+","+str(mic2.min)+","+str(mic2.max)+","+str(mic3.avg)+","+str(mic3.min)+","+str(mic3.max)+"\n")
		
		# Save each wav file from each microphone for later analysis
		mic1.fileName = foldern+"mic1wave_"str(i)+".wav"
		mic2.fileName = foldern+"mic2wave_"str(i)+".wav"
		mic3.fileName = foldern+"mic3wave_"str(i)+".wav"

		mic1.savefile()
		mic2.savefile()
		mic3.savefile()

# Detect the same signal by all microphones?

main()


#mic1wave_1
#mic2wave_1
#mic3wave_1
