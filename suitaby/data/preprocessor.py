try:
	import formatChecker
	from SizesDataset import SizesDataset
	from Brand import Brand
except ImportError:
	print 'preprocessor -- (!) module do not found'	
	exit()


#
# preprocessor module
#
# prepares the sizes data lines for the database, by making a series of operations
#


# preforms a series of preprocessing operations
# takes as input a list of lines as strings
# returns a list of lines as strings
def preprocess(dataLines):

	if not formatChecker.checkSizeFormat(dataLines):
		print formatChecker.errorMessage

	upperCaseLines = doUpperCase(dataLines)
	changedUrlsLines = changeURLs(upperCaseLines)
	mergedDataLines = mergeSynonymousSizeTypes(changedUrlsLines)
	fixedSizesLines = getFixedSizesLines(mergedDataLines)

	return fixedSizesLines




# makes all column data upperCase (exceptions are the url and size columns)
def doUpperCase(dataLines):
		
	upperCaseLines = []

	for line in dataLines:

		# split line to columns using 'tab' 
		columns = line.split('\t')

		size_type = columns[0]
		size = columns[1]
		label = columns[2]
		brand = columns[3]
		url = columns[4]
		clothe_category = columns[5]
		parts = columns[6].split('\n')
		size_category = parts[0] 

		upperLine = size_type.upper() + '\t' + size + '\t' + label.upper() + '\t' + brand.upper() + '\t' + url + '\t' + clothe_category.upper() + '\t' + size_category.upper()

		upperCaseLines.append(upperLine)

	return upperCaseLines


# sets the correct brands' urls
def changeURLs(dataLines):

	changedUrlsLines = []

	for line in dataLines:

		# split line to columns using 'tab' 
		columns = line.split('\t')

		size_type = columns[0]
		size = columns[1]
		label = columns[2]
		brand = columns[3]
		url = columns[4]
		clothe_category = columns[5]
		parts = columns[6].split('\n')
		size_category = parts[0] 

		url = Brand.brandsUrls[ brand ]

		changedUrlLine = size_type + '\t' + size + '\t' + label + '\t' + brand + '\t' + url + '\t' + clothe_category + '\t' + size_category

		changedUrlsLines.append(changedUrlLine)

	return changedUrlsLines


# merge synonymous sizeTypes
# { hip -> hips, sleeve - sleeve length, back -> back_length }
def mergeSynonymousSizeTypes(dataLines):
		
	mergedDataLines = []

	for line in dataLines:

		# split line to columns using 'tab' 
		columns = line.split('\t')

		size_type = columns[0]
		size = columns[1]
		label = columns[2]
		brand = columns[3]
		url = columns[4]
		clothe_category = columns[5]
		parts = columns[6].split('\n')
		size_category = parts[0] 

		if (size_type == "HIP"):
			size_type = "HIPS"
		elif (size_type == "SLEEVE"):
			size_type = "SLEEVE LENGTH"
		elif (size_type == "BACK"):
			size_type = "BACK LENGTH"

		mergedLine = size_type + '\t' + size + '\t' + label + '\t' + brand + '\t' + url + '\t' + clothe_category + '\t' + size_category

		mergedDataLines.append(mergedLine)

	return mergedDataLines


# get the lines with the sizes fixed
def getFixedSizesLines(dataLines):

	outLines = []

	sizesDataset = SizesDataset(dataLines)

	brands = sizesDataset.getBrands()
	catSizeTypes = sizesDataset.getSizeTypes()
	catSizeCategories = sizesDataset.getSizeCats()

	for brand in brands:		
		for clotheCat in catSizeTypes:
			sizeTypes = catSizeTypes[clotheCat]
			sizeCats = catSizeCategories[clotheCat]

			for sizeCat in sizeCats:
				for sizeType in sizeTypes:

					fixedLines = fixSizes(brand, clotheCat, sizeCat, sizeType, dataLines)

					for fixedLine in fixedLines:
						outLines.append(fixedLine)

	return outLines



def fixSizes(brand, clotheCat, sizeCat, sizeType, dataLines):

	outLines = []
	sizes = []
	labels = {}
	labelsList = []
	linesCounter = 0

	for line in dataLines:

		columns = line.split('\t')

		# just split the next line character
		terms = columns[6].split('\n')		

		if (brand == columns[3]) and (clotheCat == columns[5]) and (sizeCat == terms[0]) and (sizeType == columns[0]):

			# fix XX,XX to XX.XX
			columns[1] = columns[1].replace(",", ".")

			sizes.append(columns[1])

			tt = columns[1].split('-')

			labelsList.append( columns[2] )

			labels[str(float(tt[0]))] = columns[2]

			url = columns[4]

			linesCounter+=1


	if linesCounter > 0:

		if len(set(sizes)) > 1:

			outSizes = []

			for i in range(len(sizes)):

				ss = sizes[i].split('-')

				if len(ss) == 1:

					if i+1 < len(sizes):

						ss2 = sizes[i+1].split('-')

						if float(sizes[i]) < float(ss2[0])-0.1: 

							outSizes.append( str(float(sizes[i])) + '-' + str(float(ss2[0])-0.1) )
						else:
							outSizes.append( str(float(sizes[i])) + '-' + str(float(sizes[i])) )
					else:
						outSizes.append( str(float(sizes[i])) + '-' + str(float(sizes[i])) )
				else:
					outSizes.append( sizes[i] )

			for outSize in outSizes:

				tt = outSize.split('-')

				outLines.append(sizeType + '\t' + outSize + '\t' + labels[str(float(tt[0]))] + '\t' + brand +
								 '\t' + url + '\t' + clotheCat + '\t' + sizeCat)

		elif len(set(sizes)) == 1:

			for label in labelsList:

				outSize = sizes[0] + '-' + sizes[0]

				outLines.append(sizeType + '\t' + outSize + '\t' + label + '\t' + brand +
							 '\t' + url + '\t' + clotheCat + '\t' + sizeCat)		
		
	return outLines


