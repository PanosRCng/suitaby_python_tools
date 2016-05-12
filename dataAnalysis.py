try:
	import sys
	from suitaby.data.IO import IO
	from suitaby.data.Sizes import Sizes
	from suitaby.data.Clustering import CL_Unsupervised
	from suitaby.data.Model import KNNModel
	from suitaby.data.Utils import Utils
except ImportError:
	print '(!) main - module do not found'	
	exit()

inSizesFile = "sizes.txt"
preprocessOutFile = "producedData/fixedSizes.txt"


def preprocess():

	# load file as list of string datalines
	io = IO()
	sizesDataLines = io.ReadFile(inSizesFile)

	# create Sizes object
	sizes = Sizes(sizesDataLines)	


	### starts preprocessing ###

	# make all column data upperCase (exceptions are the url and size columns)
	upperDataLines = sizes.doUpperCase()

	# create new Sizes object using the upperCase sizes dataLines
	upperSizes = Sizes(upperDataLines)

	#change brands' URLs (from sizes source url to the brand url)
	changedURLsDataLines = upperSizes.changeURLs()

	# create new Sizes object using the changedUrls sizes dataLines
	changedUrlsSizes = Sizes(changedURLsDataLines)

	# merge synonymous sizeTypes
	mergedSynonymousSizeTypesLines = changedUrlsSizes.mergeSynonymousSizeTypes()

	# create new Sizes object using the merged sizes dataLines
	mergedSizes = Sizes(mergedSynonymousSizeTypesLines)

	# get fixed lines as list of string datalines, and write them to file
	fixedLines = mergedSizes.getFixedLines()
	io.WriteSizesHeader(preprocessOutFile)
	io.WriteFile(preprocessOutFile, fixedLines, 'a')



def main():

#	preprocess()
	io = IO()
	dataLines = io.ReadFile(preprocessOutFile)

	sizes = Sizes(dataLines)	
	bounds = sizes.getSizesBounds()

	for bound in bounds:
		print bound, bounds[bound]


#	Utils.scatterPlot(dataLines, 'WAIST', 'HIPS')

#	knnModel = KNNModel(dataLines, ['WAIST', 'HIPS'], 'HIPS')
#	print knnModel.predict([84.3], 5)


#	knnModel = KNNModel(dataLines, ['WAIST', 'HIPS', 'LOWER WAIST'], 'LOWER WAIST')
#
#	data_str = ''
#	labels_str = ''
#
#	for id in knnModel.data:
#		line = str(id) + ' => ' +  str(knnModel.data[id]) + ', '
#		data_str += line
#
#	print '\n\n'
#
#	for id in knnModel.labels:
#		line = str(id) + ' => ' +  str(knnModel.labels[id]) + ', '
#		labels_str += line
#
#	print data_str
#	print labels_str


#	knnModel = KNNModel(dataLines, ['BACK LENGTH', 'SHOULDER WIDTH', 'CHEST', 'SLEEVE LENGTH', 'NECK'], 'BACK LENGTH')
#	knnModel = KNNModel(dataLines, ['SHOULDER WIDTH', 'CHEST', 'SLEEVE LENGTH'], 'SHOULDER WIDTH')
#	knnModel = KNNModel(dataLines, ['WAIST', 'HIPS', 'THIGH'], 'THIGH')
#	knnModel = KNNModel(dataLines, ['BACK LENGTH', 'SHOULDER WIDTH', 'CHEST', 'SLEEVE LENGTH'], 'BACK LENGTH')
#	knnModel = KNNModel(dataLines, ['INSIDE LEG', 'WAIST'], 'INSIDE LEG')
#	knnModel = KNNModel(dataLines, ['WAIST', 'FRONT RISE', 'BOTTOM LEG'], 'WAIST')
#	knnModel = KNNModel(dataLines, ['WAIST', 'CHEST', 'HIPS'], 'HIPS')
#	knnModel = KNNModel(dataLines, ['WAIST', 'HIPS'], 'HIPS')
#	knnModel = KNNModel(dataLines, ['BACK LENGTH', 'CHEST'], 'BACK LENGTH')
#	knnModel = KNNModel(dataLines, ['WAIST', 'HIPS', 'LOWER WAIST'], 'LOWER WAIST')
#	knnModel = KNNModel(dataLines, ['WAIST', 'BACK LENGTH'], 'BACK LENGTH')
#	knnModel = KNNModel(dataLines, ['CHEST', 'NECK'], 'NECK')
#	knnModel = KNNModel(dataLines, ['CHEST', 'SLEEVE LENGTH', 'NECK'], 'NECK')
#
#	knnModel.measure()


#	sizes = Sizes(dataLines)	
#	sizeTypes = sizes.getSizeTypesList()
#
#	dataset = Dataset(dataLines)
#	dataset.getDataset(sizeTypes)
#	featuresStats, patternDict = dataset.getStats()
	
	
#	clustering = CL_Unsupervised()
#	clusters, centroids = clustering.KMeans(datasetFixed, 5, 'medoids')
#
#	for cluster in clusters:
#		for element in clusters[cluster]:
#
#			labels[id_counter] = centroids[cluster][predict_index]
#			data[id_counter] = [ element[i] for i in data_indices ]
#			id_counter += 1
#
#	for cluster in clusters:
#		for i in range(len(sizeTypes)):
#			print sizeTypes[i], centroids[cluster][i]
#		print '\n\n'


if __name__ == "__main__":
	main()
