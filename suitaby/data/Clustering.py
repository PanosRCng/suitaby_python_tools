###################################
#
# clustering module
#
# contains clustering algorithms
#

try:
	from suitaby.data.Utils import Utils
	import random
except ImportError:
	print '(!) module do not found '	
	exit()


class CL_Unsupervised():


	def __init__(self):
	
		random.random()

		self.mean_methods = ['centroids', 'medoids']

		# just an empty row
		self.empty_row = []

		# just set a very big number for a max
		self.big_number = 100000000000 


	# K-Means clustering algorithm
	# 	- data, a list with elements for clustering, 
	#       	every element (feature vector) is a list containing the values for the feature set in the same order
	# 	- k, number of disired clusters
	#	- mean_method, the method for the means calulation, 'centroids'/'medoids'
	#
	#	(*) uses euclidean distance as distance measurement technique
	#	    uses the absolute error minimization as the stopping criterion for the medoids mean method
	#	    uses the mean of squared errors minimization as stopping criterion for the centroids mean method
	#	    tries to converge to the global optimum, by running multiple times with different initial random means
	#
	def KMeans(self, data, k, mean_method):

		means = {}
		K = {}

		# some input checks
		if len(data) == 0:
			print '(!) data is empty'
			return -1

		if not ( isinstance(k, (int,long)) ) or ( k <= 0 ):
			print '(!) k must be a positive integer'
			return -1

		if mean_method not in self.mean_methods:
			print '(!) mean_method must be one of the mean method keywords'
			return -1

		empty_row = []
		for i in range(len(data[0])):
			self.empty_row.append(0.0)

		min_AE = self.big_number

		# run multiple times with different initial random means, to avoid converge to local optimum
		for i in range(10):

			# pick random means from the dataset
			for cluster in range(k):
				means[cluster] =  data[ random.randint(0,len(data)-1) ]

			local_K, local_means, local_AE = self.KMeansCore(data, k, mean_method, means)

			if local_AE < min_AE:
				min_AE = local_AE
				K = local_K
				means = local_means

		return (K, means)


	def KMeansCore(self, data, k, mean_method, means):

		K = {}
	
		min_AE = self.big_number
		prev_AE = 0
		min_means = {}
		min_K = {}

		iter_flag = True

		# do iterative relocation, until nothing changes
		while(iter_flag):

			for cluster in range(k):
				K[cluster] = []

			# assign each element to the cluster which has the closest mean
			for element in data:

				# for start, just set a big max number, and just pick the cluster 0 as the closest cluster
				min_dist = self.big_number
				closest_cluster = 0

				for cluster in range(k):

					dist = Utils.euclidean_distance( means[cluster], element )

					if dist < min_dist:
						min_dist = dist
						closest_cluster = cluster

				K[closest_cluster].append( element )
				means[closest_cluster] = element


			# calculate new mean for each cluster
	
			if mean_method == self.mean_methods[0]:
				for cluster in range(k):
					means[cluster] = self.getCentroid( K[cluster] )
			elif mean_method == self.mean_methods[1]:
				for cluster in range(k):
					means[cluster] = self.getMedoid( K[cluster] )	

			# calculate the absolute error
			if mean_method == self.mean_methods[0]:
				AE = self.MSE(K, means)
			elif mean_method == self.mean_methods[1]:
				AE = self.absolute_error(K, means)

			# keep the clustering that minimizes the absolute error
			if AE < min_AE:
				min_AE = AE
				min_means = means
				min_K = K

			# stop when nothing changes
			if prev_AE == AE:
				iter_flag = False
			else:
				prev_AE = AE

		return (min_K, min_means, min_AE)


	def getMedoid(self, cluster_elements):

		if len(cluster_elements) == 0:
			return self.empty_row

		N = len(cluster_elements[0])

		centroid = self.getCentroid( cluster_elements )

		# just a big number to start
		min_dist = self.big_number
		medoid = self.empty_row

		for element in cluster_elements:

			dist = Utils.euclidean_distance( centroid, element )

			if dist < min_dist:
				min_dist = dist
				medoid = element

		return medoid


	def getCentroid(self, cluster_elements ):

		if len(cluster_elements) == 0:
			return self.empty_row

		N = len(cluster_elements[0])

		centroid = []

		for i in range(N):
			centroid.append(0.0)

		for i in range(N):
			for x in cluster_elements:
				centroid[i] += x[i]

		for i in range(N):
			if centroid[i] != 0:
				centroid[i] = centroid[i] / len(cluster_elements)

		return centroid


	def absolute_error(self, clusters, means):

		ae = 0.0

		for cluster in clusters:
			
			sum_dissimilarities = 0

			for element in clusters[cluster]:
				sum_dissimilarities += Utils.euclidean_distance( element, means[cluster] )

			ae += sum_dissimilarities

		return ae


	def MSE(self, clusters, means):

		mse = 0.0

		for cluster in clusters:
			
			mse_c = 0.0

			for element in clusters[cluster]:
				mse_c += pow( Utils.euclidean_distance( element, means[cluster] ), 2 )

			if len(clusters[cluster]) > 0:
				mse_c = ( mse_c / len(clusters[cluster]) )

			mse += mse_c

		return (mse / len(clusters) )
	



