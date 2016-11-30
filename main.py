try:
	import sys

	from suitaby.data import io
	from suitaby.data.Dataset import Dataset
	from suitaby.data import checker
	from suitaby.data import preprocessor
	from suitaby.data.SizeCatalog import SizeCatalog
	from suitaby.data.SizesDataset import SizesDataset

	from suitaby.data.DBHelper import DBHelper

#	from suitaby.data.Sizes import Sizes
except ImportError:
	print 'main -- (!) module do not found '	
	exit()


def main():

	inSizesFile = "new_sizes.txt"
	sizeCatalogFile = "producedData/sizeCatalog.txt"
	preprocessOutFile = "producedData/preprocessedSizes.txt"


### from unprocessed sizes data to database - as one shot run ###
#
# preprocessing
# size catalog construction
# database construction and bulk load  


	# load file as list of string datalines
	sizesDataLines = io.ReadFile(inSizesFile)

	# do a consistency check
	dataset = Dataset( sizesDataLines )
	checker.checkDataset(dataset)

	# preprocess dataLines
	preprocessedDataLines = preprocessor.preprocess(sizesDataLines)

	# write processed dataLines to file
	io.WriteHeader(preprocessOutFile, Dataset.columns)
	io.WriteFile(preprocessOutFile, preprocessedDataLines, 'a')

	# construct the size catalog
	sizesDataset = SizesDataset( preprocessedDataLines )
	projections = sizesDataset.getSizeTypesProjections()
	sizeCatalog = sizesDataset.constructSizeCatalog(projections)

	# write the sizes catalog to file
	io.WriteHeader(sizeCatalogFile, SizeCatalog.columns)
	io.WriteFile(sizeCatalogFile, sizeCatalog, 'a')

	# create a dbHelper object, connect to database, and construct the db schema
	dbHelper = DBHelper("betaDB", preprocessOutFile, sizeCatalogFile)
	dbHelper.constructDbSchema()
	
	print 'all ok'


if __name__ == "__main__":
	main()
