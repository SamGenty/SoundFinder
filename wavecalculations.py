from scipy import signal, fftpack, correlate
import numpy

'''
	If you want circular correlation and for big signal size, you can use the convolution/Fourier transform theorem with the caveat that correlation is very similar to but not identical to convolution.
	a = numpy.array([0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 0, 0, 0, 0, 0])
    b = numpy.array([0, 0, 0, 0, 0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 0])
	A = fftpack.fft(a)
	B = fftpack.fft(b)
	Ar = -A.conjugate()
	Br = -B.conjugate()
	numpy.argmax(numpy.abs(fftpack.ifft(Ar*B))) -> 4
	numpy.argmax(numpy.abs(fftpack.ifft(A*Br))) -> 17

'''
class WaveCalculations:
	def __init__(self, n1, n2, _w1_data, _w2_data):
		self.wave1 = _w1_data
		self.wave2 = _w2_data
		self.name1 = n1
		self.name2 = n2
		#nsamples = self.wave1.size

	def findDifference(self):
		a = self.wave1
		b = self.wave2
		A = fftpack.fft(a)
		B = fftpack.fft(b)
		Ar = -A.conjugate()
		self.offset =  numpy.argmax(numpy.abs(fftpack.ifft(Ar*B)))
		print("Differences from : "+self.name2+" from : "+self.name1+" = "+ str(self.offset))
		return self.offset
		
	#doesn't really work =( use FFT instead since signals arent the same
	def correlate(self):
		A = self.wave1
		B = self.wave2
		nsamples = A.size
		# regularize datasets by subtracting mean and dividing by s.d.
		numpy.subtract(A, A.mean(), out=A, casting="unsafe")
		numpy.divide(A, A.std(), out=A, casting="unsafe")
		numpy.subtract(B, B.mean(), out=B, casting="unsafe")
		numpy.divide(B, B.std(), out=B, casting="unsafe")

		# Find cross-correlation
		xcorr = correlate(A, B)

		# delta time array to match xcorr
		dt = numpy.arange(1-nsamples, nsamples)

		recovered_time_shift = dt[xcorr.argmax()]
		print("Time shift of : "+self.name1+" and "+self.name2+" => "+ str(recovered_time_shift))
		return recovered_time_shift
		
		
		
		
		
		
		
		
