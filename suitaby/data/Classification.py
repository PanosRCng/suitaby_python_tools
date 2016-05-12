#################################################
#
# Classification module
#
#

try:
	from suitaby.data.Utils import Utils
	import random
	from math import sqrt
except ImportError:
	print '(!) module do not found '	
	exit()


# K-Nearest-Neighbors classification algorithm
# 	- data, a dictionary with data for classification,
#		key: a number as id 
#       	value: the feature vector, is a list containing the values for the feature set in the same order
#	- labels, a dictionary with labels for the data
#		key: a number as id
#		value: the label
# 	- k, the number of the nearest neighbors
#	- setting, [classification/regression]
#		classification: if labels are qualitative data
#		regression: if labels are quantitative data
#
#	(*) uses euclidean distance as distance measurement technique
class KNN():


	def __init__(self, labels, data, k, setting):
	
		random.random()

		self.settings = ['classification', 'regression']

		# some input checks
		#if len(labels) == 0:
		#	print '(!) labels is empty'

		#if len(data) == 0:
		#	print '(!) data is empty'

		#if len(labels) != len(data):
		#	print '(!) labels and data must have the same size'

		#if not ( isinstance(k, (int,long)) ) or ( k <= 0 ):
		#	print '(!) k must be a positive integer'

		#if setting not in self.settings:
		#	print '(!) setting must be a proper setting'
			
		self.labels = labels
		self.data = data
		self.k = k
		self.setting = setting

		self.N = len(self.data)


	def categorize(self, element):

		dists = {}

		for number_id in self.data:
			dists[number_id] = Utils.euclidean_distance( self.data[number_id], element )

		s_dists = list( dists.values() )
		s_dists.sort()

		k_th = s_dists[self.k-1]

		k_labels = {}

		for number_id in dists:
			if dists[number_id] <= k_th:

				label = self.labels[number_id]

				if label in k_labels:
					k_labels[label] += 1
				else:
					k_labels[label] = 1

		return max(k_labels, key=k_labels.get)		


	def KFoldCV(self, k):		

		folds = {}

		for i in range(k):
			folds[i] = []

		fold_size = len( self.data ) / k

		if (self.N % k != 0):
			print str(k) + ' is not good k for folding, your dataset has size: ' + str( self.N )
			return -1

		if ( (fold_size * (k-1)) <= self.k  ):
			print str(k) + ' is not good k for folding, your dataset has size: ' + str( self.N )
			return -1

		picked = []

		fold_counter = 0

		while( len(picked) < self.N ):

			number_id = random.randint(0,self.N-1)

			if number_id not in picked:

				picked.append( number_id )
				folds[fold_counter].append( number_id )			

				if len(folds[fold_counter]) >= fold_size:
					fold_counter += 1

		KFoldCV_error = 0.0

		for fold in range(len(folds)):

			validation_set = folds[fold]

			train_set = []

			for element in self.data:
				if element not in validation_set:
					train_set.append( element )

			cv_er = self.ErrorRate(train_set, validation_set)

			KFoldCV_error += cv_er

		return KFoldCV_error / len(folds)


	def ErrorRate(self, train_set, validation_set):

		cv_er = 0.0

		for element in validation_set:

			predicted_label = self.validate(train_set, element)

			if self.setting == self.settings[0]:
				if self.labels[element] != predicted_label:
					cv_er += 1

			elif self.setting == self.settings[1]:

				cv_er += pow((self.labels[element] - predicted_label), 2) 

		return ( cv_er / len(validation_set) )


	def validate(self, train_set, element):

		dists = {}

		for number_id in train_set:
			dists[number_id] = Utils.euclidean_distance( self.data[number_id], self.data[element] )

		s_dists = list( dists.values() )
		s_dists.sort()

		k_th = s_dists[self.k-1]

		k_labels = {}

		for number_id in dists:
			if dists[number_id] <= k_th:

				label = self.labels[number_id]

				if label in k_labels:
					k_labels[label] += 1
				else:
					k_labels[label] = 1

		return max(k_labels, key=k_labels.get)



