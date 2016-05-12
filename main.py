try:
	import sys
	from suitaby.data.IO import IO
	from suitaby.data.Sizes import Sizes
	from suitaby.data.Generator import Generator
	from suitaby.data.DBHelper import DBHelper
	from suitaby.data.Tester import Tester
except ImportError:
	print '(!) module do not found '	
	exit()


def main():

	inSizesFile = "sizes.txt"
	upperOutFileName = "upperCaseSizes.txt"
	changedUrlsOutFileName = "changedUrlsSizes.txt"
	mergedOutFileName = "mergedSynonymousSizeTypes_sizes.txt"
	outFileName = "fixedSizes.txt"
	fixedSizesOutFile = "fixedSizes.txt"
	outPeopleFile = "generatedPeople.txt"
	outBrandsFile = "generatedBrands.txt"
	sizeCatalogFile = "sizeCatalog.txt"




########################
#    usage examples    #
########################



### get useful stats from size data ###
#
#	# load file as list of string datalines
#	io = IO()
#	sizesDataLines = io.ReadFile(inSizesFile)
#
#	# create Sizes object
#	sizes = Sizes(sizesDataLines)	
#
#	# get the unique brands
#	brands = sizes.getBrands()
#
#	# get the unique clothe categories
#	clotheCategories = sizes.getClotheCategories()
#
#	# get the unique size types for every clothe category
#	clotheSizeTypes = sizes.getSizeTypes()
#
#	# get a list with all the unique size types
#	sizeTypes = sizes.getSizeTypesList()
#
#	# get the unique size categories for every clothe category
#	clotheSizeCategories = sizes.getSizeCats()		
#


### get size lines with merged synonymous SizeTypes ###
#
#	# load file as list of string datalines
#	io = IO()
#	sizesDataLines = io.ReadFile(inSizesFile)
#
#	# create Sizes object
#	sizes = Sizes(sizesDataLines)
#
#	# merge synonymous sizeTypes
#	mergedSynonymousSizeTypesLines = sizes.mergeSynonymousSizeTypes()
#
#	# write mergedSynonymousSizeTypes lines to file
#	io.WriteSizesHeader(mergedOutFileName)
#	io.WriteFile(mergedOutFileName, mergedSynonymousSizeTypesLines, 'a')	


### get fixed size lines ###
#
#	# load file as list of string datalines
#	io = IO()
#	sizesDataLines = io.ReadFile(inSizesFile)
#
#	# create Sizes object
#	sizes = Sizes(sizesDataLines)	
#
#	# get fixed lines as list of string datalines
#	fixedLines = sizes.getFixedLines()
#
#	# write fixed lines to file
#	io.WriteSizesHeader(fixedSizesOutFile)
#	io.WriteFile(fixedSizesOutFile, fixedLines, 'a')



### get the size bounds (min, max) for every sizeType ###
#
#	# load file as list of string datalines
#	io = IO()
#	sizesDataLines = io.ReadFile(inSizesFile)
#
#	# create Sizes object
#	sizes = Sizes(sizesDataLines)	
#
#	# get fixed lines as list of string datalines
#	fixedLines = sizes.getFixedLines()
#
#	# create new Sizes object using the fixed sizes dataLines
#	fixedSizes = Sizes(fixedLines)
#
#	# get the size bounds (min, max) for every sizeType as dictionary
#	# (!) works for size data lines with fixed sizes
#	sizeBounds = fixedSizes.getSizesBounds()



### construct the size catalog ###
#
#	# load file as list of string datalines
#	io = IO()
#	sizesDataLines = io.ReadFile(inSizesFile)
#	
#	# create Sizes object
#	sizes = Sizes(sizesDataLines)
#
#	mergedSynonymousSizeTypesLines = sizes.mergeSynonymousSizeTypes()
#
#	# create new Sizes object using the merged sizes dataLines
#	mergedSizes = Sizes(mergedSynonymousSizeTypesLines)
#
#	# get fixed lines as list of string datalines
#	fixedLines = mergedSizes.getFixedLines()
#
#	# create new Sizes object using the fixed sizes dataLines
#	fixedSizes = Sizes(fixedLines)	
#
#	# get the size type projections for every size catalog entry
#	sizeTypesProjections = fixedSizes.getSizeTypesProjections()
#
#	# get the size catalog as list of string datalines
#	sizeCatalog = fixedSizes.constructSizeCatalog(sizeTypesProjections)
#
#	# write size catalog to file
#	io.WriteSizeCatalogHeader(sizeCatalogFile)
#	io.WriteFile(sizeCatalogFile, sizeCatalog, 'a')



### generate virtual people ###
#
#	# load file as list of string datalines
#	io = IO()
#	sizesDataLines = io.ReadFile(inSizesFile)
#
#	# create Sizes object
#	sizes = Sizes(sizesDataLines)	
#
#	mergedSynonymousSizeTypesLines = sizes.mergeSynonymousSizeTypes()
#
#	# create new Sizes object using the merged sizes dataLines
#	mergedSizes = Sizes(mergedSynonymousSizeTypesLines)
#
#	# get fixed lines as list of string datalines
#	fixedLines = mergedSizes.getFixedLines()
#
#	# write fixed lines to file
#	io.WriteSizesHeader(fixedSizesOutFile)
#	io.WriteFile(fixedSizesOutFile, fixedLines, 'a')
#
#	generator = Generator(fixedSizesOutFile)
#	generator.GeneratePeople(10, outPeopleFile)



### from unprocessed sizes data to database - as one shot run ###
#
# preprocessing
# size catalog construction
# generate virtual people
# database construction and bulk load  


	# load file as list of string datalines
	io = IO()
	sizesDataLines = io.ReadFile(inSizesFile)

	# create Sizes object
	sizes = Sizes(sizesDataLines)	


	### starts preprocessing ###

	# make all column data upperCase (exceptions are the url and size columns), and write them to file
	upperDataLines = sizes.doUpperCase()
	io.WriteSizesHeader(upperOutFileName)
	io.WriteFile(upperOutFileName, upperDataLines, 'a')

	# create new Sizes object using the upperCase sizes dataLines
	upperSizes = Sizes(upperDataLines)

	#change brands' URLs (from sizes source url to the brand url), and write them to file
	changedURLsDataLines = upperSizes.changeURLs()
	io.WriteSizesHeader(changedUrlsOutFileName)
	io.WriteFile(changedUrlsOutFileName, changedURLsDataLines, 'a')

	# create new Sizes object using the changedUrls sizes dataLines
	changedUrlsSizes = Sizes(changedURLsDataLines)

	# merge synonymous sizeTypes, and write them to file
	mergedSynonymousSizeTypesLines = changedUrlsSizes.mergeSynonymousSizeTypes()
	io.WriteSizesHeader(mergedOutFileName)
	io.WriteFile(mergedOutFileName, mergedSynonymousSizeTypesLines, 'a')

	# create new Sizes object using the merged sizes dataLines
	mergedSizes = Sizes(mergedSynonymousSizeTypesLines)

	# get fixed lines as list of string datalines, and write them to file
	fixedLines = mergedSizes.getFixedLines()
	io.WriteSizesHeader(fixedSizesOutFile)
	io.WriteFile(fixedSizesOutFile, fixedLines, 'a')

	### ends preprocessing ###


	# create new Sizes object using the fixed sizes dataLines
	fixedSizes = Sizes(fixedLines)	

	# get the size type projections for every size catalog entry
	sizeTypesProjections = fixedSizes.getSizeTypesProjections()

	# get the size catalog as list of string datalines, and write it to file
	sizeCatalog = fixedSizes.constructSizeCatalog(sizeTypesProjections)
	io.WriteSizeCatalogHeader(sizeCatalogFile)
	io.WriteFile(sizeCatalogFile, sizeCatalog, 'a')

	# generate virtual people, and write them to file
	#generator = Generator(fixedSizesOutFile)
	#generator.GeneratePeople(10, outPeopleFile)

	# create a dbHelper object, connect to database, and construct the db schema
	dbHelper = DBHelper("betaDB", fixedSizesOutFile, sizeCatalogFile)
	dbHelper.constructDbSchema()
	
	print 'all ok'


if __name__ == "__main__":
	main()
