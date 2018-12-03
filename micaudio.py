import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import threading
import sys
import time
from wavecalculations import WaveCalculations
from triangleplot import TrianglePlot

# Notes about how Microphone works
'''
	"RATE" is the "sampling rate", i.e. the number of frames per second
	"CHUNK" is the (arbitrarily chosen) number of frames the (potentially very long) 
		signals are split into in this example
	Yes, each frame will have 2 samples as "CHANNELS=2", but the term "samples" is 
		seldom used in this context (because it is confusing)
	Yes, size of each sample is 2 bytes (= 16 bits) in this example
	Yes, size of each frame is 4 bytes
	Yes, each element of "frames" should be 4096 bytes. sys.getsizeof() reports the storage 
		space needed by the Python interpreter, which is typically a bit more than the actual 
		size of the raw data.
	RATE * RECORD_SECONDS is the number of frames that should be recorded. Since the for 
		loop is not repeated for each frame but only for each chunk, the number of loops 
		has to be divided by the chunk size CHUNK. This has nothing to do with samples, 
		so there is no factor of 2 involved.
	If you really want to see the hexadecimal values, you can try something like [hex(x) 
		for x in frames[0]]. If you want to get the actual 2-byte numbers use the format 
		string '<H' with the struct module.
	'''

class Mic:
	
	def __init__(self, _index, _name, save_file = False, filename = "output"):
		self.index = _index # Integer of hardware device name
		self.name = _name # String of Hardware device name
		self.saveFile = save_file # Boolean file control the option to save to 
		self.fileName = filename
		self.frames = []
		self.data = []

		self.CHUNK = 1024
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 1
		self.RATE = 44100
		self.RECORD_SECONDS = 3


	# The function running on its own thread
	def record(self):
		#Setup the stream
		stream = self.p.open(format=self.FORMAT,
			channels=self.CHANNELS,
			rate=self.RATE,
			input=True,
			input_device_index=self.index,
			frames_per_buffer=self.CHUNK)

		print("Mic"+str(self.name)+" recording . . .")

		# Begin reading in data
		for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
			data = stream.read(self.CHUNK, exception_on_overflow=False)
			# frames.append(data)
			self.frames.append(np.fromstring(data, dtype=np.int16))
			# print(str(int.from_bytes(data, byteorder='little'))+ str('\n'))

		print("Mic"+str(self.name)+"done recording\n")

		stream.stop_stream()
		stream.close()
		self.p.terminate()

		# Data is stored as a numpy array
		self.data = np.hstack(self.frames)

		# If the user wants to save the Audio file
		if(self.saveFile):
			wf = wave.open(self.fileName, 'wb')
			wf.setnchannels(self.CHANNELS)
			wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
			wf.setframerate(self.RATE)
			wf.writeframes(b''.join(self.frames))
			wf.close()


	def setup(self):
		self.p = pyaudio.PyAudio()
		self.proc = threading.Thread(target=self.record)
		self.frames = []
		self.data = []

	def startthread(self):
		self.proc.start()

	def jointhread(self):
		self.proc.join()



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
			
	
	print(count)
	print("There are "+str(count)+" mics connected")


	# Instantiate the Mic objects
	mic1 = Mic(mic1_index, mic1_name, save_file=False, filename = "mic1output.wav")
	mic2 = Mic(mic2_index, mic2_name, save_file=False, filename = "mic2output.wav")
	mic3 = Mic(mic3_index, mic3_name, save_file=False, filename = "mic3output.wav")
	
	
	file = open("threading_FFTs.csv","w")
	file.write("All columns are FFT between each waveform\n") 
	file.write("Test#,w2:w1,w3:w1,w3:w2,w1:w2,w1:w3,w2:w3\n")
	#cor_w2->w1,cor_w3->w1,cor_w3->w2,cor_w1->w2,cor_w1->w3,cor_w2->w3\n")
	for i in range(200):
	
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
		
		a1 = a.findDifference()
		b1 = b.findDifference()
		c1 = c.findDifference()
		
		ar1 = ar.findDifference()
		br1 = br.findDifference()
		cr1 = cr.findDifference()
		'''
		ts_a1 = a.correlate()
		ts_b1 = b.correlate()
		ts_c1 = c.correlate()
		
		ts_ar1 = ar.correlate()
		ts_br1 = br.correlate()
		ts_cr1 = cr.correlate()
		'''
		
		file.write(str(i)+","+str(a1)+","+str(b1)+","+str(c1)+","+str(ar1)+","+str(br1)+","+str(cr1)+"\n")
		#","+str(ts_a1)+","+str(ts_b1)+","+str(ts_c1)+","+str(ts_ar1)+","+str(ts_br1)+","+str(ts_cr1)+"\n")
		'''
		fig = plt.figure(1)
		fig.suptitle("All waveforms of Mic Recordings")
		ax = plt.subplot(311)
		ax.set_title("Mic1 Waveform")
		ax.plot(data1)
		
		ax = plt.subplot(312)
		ax.set_title("Mic2 Waveform")
		ax.plot(data2)
		
		ax = plt.subplot(313)
		ax.set_title("Mic3 Waveform")
		ax.plot(data3)

		plt.show()
		'''

main()
