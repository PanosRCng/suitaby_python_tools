#
#
#	!!!  outdated  !!!
#


###################################
#
# Model module
#
# contains some models
#

try:
	from suitaby.data.Dataset import Dataset
	from suitaby.data.Classification import KNN
	from suitaby.data.Utils import Utils
except ImportError:
	print '(!) module do not found '	
	exit()


class KNNModel():


	#constructor 
	#
	# - dataLines, list, preprocessed size data
	# - features, a list with the sizeTypes, for example ['WAIST', 'CHEST', 'HIPS']
	# - y, the dependent variable, for example when features are ['WAIST', 'CHEST', 'HIPS'] and y is 'HIPS'
	#	the model will use ['WAIST', 'CHEST'] as data to predict 'HIPS'
	def __init__(self, dataLines, features, y):
	
		self.data = {}
		self.labels = {}

		dataset = Dataset(dataLines)
		model_dataset = dataset.getDataset(features)

		predict_index = features.index(y)
		data_indices = []

		for i in range(len(features)):
			if features[i] == y:
				continue
			data_indices.append(i)

		id_counter = 0

		for element in model_dataset:
	
			# reject data with missing values
			if 0 in element:
				continue

			self.labels[id_counter] = element[predict_index]
			self.data[id_counter] = [ element[i] for i in data_indices ]
			id_counter += 1	


	def measure(self):

		x = []
		y = []

		for i in range( len(self.data) ):
			k = i+1

			knn = KNN(self.labels, self.data, k, 'regression')
			KFoldCV_error = knn.KFoldCV( len(self.data) )

			if KFoldCV_error > -1:
				x.append( 1.0 / k )
				y.append( KFoldCV_error )

		Utils.plot2D(x,y) 


	def predict(self, element, k):

		knn = KNN(self.labels, self.data, k, 'regression')

		return knn.categorize(element)


	def getModel(self):

		return 'model'




