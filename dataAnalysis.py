try:
	import sys
	from suitaby.data.IO import IO
	from suitaby.data.Sizes import Sizes
	from suitaby.data.Clustering import CL_Unsupervised
	from suitaby.data.Model import KNNModel
	from suitaby.data.Dataset import Dataset
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

	preprocess()
	io = IO()
	dataLines = io.ReadFile(preprocessOutFile)

	knnModel = KNNModel(dataLines, ['BACK LENGTH', 'SHOULDER WIDTH', 'CHEST', 'SLEEVE LENGTH', 'NECK'], 'NECK')
	knnModel.measure()

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
