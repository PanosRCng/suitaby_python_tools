#
#
#	!!!  outdated  !!!
#

try:
	from suitaby.data.Sizes import Sizes
except ImportError:
	print '(!) module do not found'	
	exit()


#
# Dataset module
#
# helps to extract datasets from the sizes data
#


class Dataset():


	#constructor 
	#
	# - dataLines, list, preprocessed size data
	def __init__(self, dataLines):

		if not len(dataLines) > 0:
			print '(!) dataLines list is empty'

		self.sizes = Sizes(dataLines)

		self.dataLines = []

		self.features = []


	# creates a dataset line for every size catalog entry
	# returns a dictionary dataset[size_catalog_entry] = "[(sizeType_1:value), (sizeType_2:value),]" 
	def getDataset(self, features):

		self.features = features

		sizeTypes = self.sizes.getSizeTypesList()
		for feature in features:
			if feature not in sizeTypes:
				print '(!) feature ' + feature + ' is not a proper sizeType'
				return
		
		groupDict = {}

		# for every line
		for line_i in self.sizes.sizesDataLines:
		
			# split line to columns using 'tab' 
			columns = line_i.split('\t')

			size_type_i = columns[0]
			size_i = columns[1]
			label_i = columns[2]
			brand_i = columns[3]
			url_i = columns[4]
			clothe_category_i = columns[5]
			parts = columns[6].split('\n')
			size_category_i = parts[0] 

			# for every line again
			for line_j in self.sizes.sizesDataLines:
		
				# split line to columns using 'tab' 
				columns = line_j.split('\t')

				size_type_j = columns[0]
				size_j = columns[1]
				label_j = columns[2]
				brand_j = columns[3]
				url_j = columns[4]
				clothe_category_j = columns[5]
				parts_j = columns[6].split('\n')
				size_category_j = parts[0] 

				if (brand_i == brand_j) and (url_i == url_j) and (clothe_category_i == clothe_category_j) and (size_category_i == size_category_j) and (label_i == label_j):

					key = brand_i + " : " + clothe_category_i + " : " + label_i + " : " + size_category_i

					if key in groupDict:
						groupDict[key].append((size_type_i,size_i))
					else:
						sizeList = []
						sizeList.append((size_type_i,size_i))
						groupDict[key] = sizeList

		fixedLines = {}

		for key in list(groupDict.keys()):

			featureList =  list(set(groupDict[key]))

			id_counter = 0
			tempDict = {}
			doubles = []

			for feature in featureList:
				if feature[0] not in tempDict:
					tempDict[feature[0]] = feature[1]
				else:
					doubles.append(feature[0])

			tempFeatureList = []

			for feature in featureList:
				if feature[0] not in doubles:
					tempFeatureList.append(feature)

			if len(featureList) == len(tempFeatureList):
				fixedLines[key] = featureList
			else:
				for feature in featureList:
					if feature[0] in doubles:

						key_new = key + " : " + str(id_counter)
						id_counter += 1

						featureList_new = list(tempFeatureList)
						featureList_new.append(feature)

						fixedLines[key_new] = featureList_new

		ext_dataset = {}
		id_counter = 0

		for key in list(fixedLines.keys()):

			features1 = []
			features2 = []

			for feature in fixedLines[key]:

				parts = feature[1].split('-')

				features1.append( (feature[0], parts[0]) )
				features2.append( (feature[0], parts[1]) )				

			ext_dataset[id_counter] = features1
			id_counter += 1
			ext_dataset[id_counter] = features2
			id_counter += 1

		dataset = {}
		id_counter = 0

		feature_vector = {}
		for feature in features:
			feature_vector[feature] = 0

		for key in ext_dataset:

			new_feature_vector = dict(feature_vector)

			for feature in ext_dataset[key]:
				new_feature_vector[feature[0]] = feature[1]

			dataset[id_counter] = new_feature_vector
			id_counter += 1

		dataLines = []

		for key in dataset.keys():

			dataLine = []

			for feature in self.features:
				dataLine.append( float(dataset[key][feature]) )

			self.dataLines.append(dataLine)

		return self.dataLines


	def getStats(self):

		featuresStats = {}
		patternDict = {}

		for feature in self.features:
			featuresStats[feature] = 0

		for data in self.dataLines:

			row = ''

			for i in range(len(self.features)):		
				if data[i] != 0:
					featuresStats[self.features[i]] += 1
					row += self.features[i] + ' + '

			if row in patternDict.keys():
				patternDict[row] += 1
			else:
				patternDict[row] = 1	

		return (featuresStats, patternDict)





