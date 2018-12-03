import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import threading
import sys
import time
from wavecalculations import WaveCalculations


'''
Author: Samuel Genty
School: Texas A&M University
Date: 11/27/2018
Computer Science and Engineering 18'

##################################

Description:
This python script contains the Mic object which is responsible
for recording an audio signal via any USB audio device that is plugged 
into the OS. 

##################################

Technical aspects:
I am using the pyaudio python package that contains an
out of the box API solution for recording audio from a USB device.
In my object design I created a method that is spawned on its own thread
so that multiple microphones that can record an audio environment at almost the same time.
I calibrated each USB Audio microphone with each other so the audio data can be synchronized.
I calculate the maximum, minimum,  and average of each audio signal as well to do volume calculations for
determining where the audio sound is coming from

#######################################
'''
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
		self.frames1 = []
		self.data = []

		self.CHUNK = 1024
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 1
		self.RATE = 44100
		self.RECORD_SECONDS = 2


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
			self.frames1.append(data)
			self.frames.append(np.fromstring(data, dtype=np.int16))
			# print(str(int.from_bytes(data, byteorder='little'))+ str('\n'))

		print("Mic"+str(self.name)+"done recording\n")

		stream.stop_stream()
		stream.close()
		self.p.terminate()
	
		# Data is stored as a numpy array
		self.data = np.hstack(self.frames)
		self.maxx = np.max(self.data)
		self.minn= np.min(self.data)
		self.avg = np.average(self.data)
		return

	def savefile(self):
		if(self.saveFile):
			wf = wave.open(self.fileName, 'wb')
			wf.setnchannels(self.CHANNELS)
			wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
			wf.setframerate(self.RATE)
			wf.writeframes(b''.join(self.frames1))
			wf.close()


	def setup(self):
		self.p = pyaudio.PyAudio()
		self.proc = threading.Thread(target=self.record)
		self.frames = []
		self.frames1 = []
		self.data = []

	def setuplive(self):
		self.proc1 = threading.Thread(target=self.plot_data)
		i=0
		f,ax = plt.subplots(2)
        # Prepare the Plotting Environment with random starting values
		x = np.arange(10000)
		y = np.random.randn(10000)

		    # Plot 0 is for raw audio data
		li, = ax[0].plot(x, y)
		ax[0].set_xlim(0,1000)
		ax[0].set_ylim(-20000, 20000)
		ax[0].set_title("Raw Audio Signal")
		# Plot 1 is for the FFT of the audio
		li2, = ax[1].plot(x, y)
		ax[1].set_xlim(0,5000)
		ax[1].set_ylim(-100,100)
		ax[1].set_title("Fast Fourier Transform")
		# Show the plot, but without blocking updates
		plt.pause(0.01)
		plt.tight_layout()


		self.audio = pyaudio.PyAudio()

		# start Recording
		self.stream1 = self.audio.open(format=self.FORMAT,
		                    channels=self.CHANNELS,
		                    rate=self.RATE,
		                    input=True,
		                    input_device_index=self.index)
		self.keep_going = True

	def plotty(in_data):
		audio_data = np.fromstring(in_data, np.int16)
		# Fast Fourier Transform, 10*log10(abs) is to scale it to dB
		# and make sure it's not imaginary
		dfft = 10.*np.log10(abs(np.fft.rfft(audio_data)))

		# Force the new data into the plot, but without redrawing axes.
		# If uses plt.draw(), axes are re-drawn every time
		#print audio_data[0:10]
		#print dfft[0:10]
		#print
		li.set_xdata(np.arange(len(audio_data)))
		li.set_ydata(audio_data)
		li2.set_xdata(np.arange(len(dfft))*10.)
		li2.set_ydata(dfft)

		# Show the updated plot, but without blocking
		plt.pause(0.01)
		if self.keep_going:
		    return True
		else:
		    return False

	def plot_data(self):
		stream.start_stream()
		while self.keep_going:
			plotty(self.stream1.read(self.CHUNK, exception_on_overflow = False))


	def startthread(self):
		self.proc.start()

	def jointhread(self):
		self.proc.join()

	def startlivethread(self):
		self.proc1.start()

	def joinlivethread(self):
		self.proc1.join()