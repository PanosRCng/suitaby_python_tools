###################################
#
# Utils module
#
# contains useful utilities
#


try:
	from math import sqrt
	from matplotlib.pyplot import *
except ImportError:
	print '(!) module do not found '	
	exit()


class Utils():

	@staticmethod
	def euclidean_distance(x1, x2):

		if len(x1) != len(x2):
			print '(!) vectors do not have the same size'
			return -1

		y = 0

		for i in range(len(x1)):
			y = y + ( pow(x1[i] - x2[i], 2) )

		return sqrt( y )


	@staticmethod
	def plot2D(x, y):

		if len(x) != len(y):
			print '(!) x and y must be of the same size'
			return -1

		plot(x, y, 'b-o')
		ylabel('error rate')
		xlabel('1/K')
		xlim( min(x) , max(x))
		ylim( min(y), max(y))
		show()





