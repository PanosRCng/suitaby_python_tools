#
#
#	!!!  outdated  !!!
#


###################################
#
# Utils module
#
# contains useful utilities
#


try:
	from suitaby.data.Dataset import Dataset
	from math import sqrt
	import matplotlib.pyplot as plt
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

		plt.plot(x, y, 'b-o')
		plt.ylabel('error rate')
		plt.xlabel('1/K')
		plt.xlim( min(x) , max(x))
		plt.ylim( min(y), max(y))
		plt.show()


	# (!) dataLines must be preprocessed
	@staticmethod
	def scatterPlot(dataLines, sizeTypeX, sizeTypeY):

		dataset = Dataset(dataLines)
	
		datasetWH = dataset.getDataset([sizeTypeX, sizeTypeY])
		xs = [line[0] for line in datasetWH if 0 not in line]
		ys = [line[1] for line in datasetWH if 0 not in line]

		plt.scatter(xs, ys)
		plt.ylabel(sizeTypeY)
		plt.xlabel(sizeTypeX)
		plt.show()



