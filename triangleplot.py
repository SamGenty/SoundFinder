import numpy as np 
import matplotlib.pyplot as plt
from pylab import text

class TrianglePlot:
	def __init__(self, point):
		self.X = np.array([[2,5], [17,5], [9.5, 18], point])
		self.Y = ['blue', 'blue', 'blue', 'red']
		plt.figure()
		plt.scatter(self.X[:, 0], self.X[:, 1], s = 100, color = self.Y[:])
		plt.xlim([-5, 25])
		plt.ylim([-5, 25])
		text(2.3, 5, "Mic2", fontsize=11)
		text(17.3, 5, "Mic3", fontsize=11)
		text(9.8, 18, "Mic1", fontsize=11)
		text(point[0]+0.5, point[1], "Sound", fontsize=9)
		plt.show()

a = TrianglePlot([17,15])


'''

left
s1 = 25 = 63.5 cm
s2 20.75 = 52.705 cm
b1 .25 = .635 cm
b2 .25 = .635
e 15.5 = 39.37 cm

right 
s1 = 23 = 58.42 cm
s2 = 21 = 53.34 cm
b1  = .25 = .635
b2 = .25 = .635
e = 15.5 = 39.37 cm

'''