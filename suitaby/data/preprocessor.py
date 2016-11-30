try:
	import checker
	from Dataset import Dataset
	from SizesDataset import SizesDataset
	from Brand import Brand
	from SizeType import SizeType
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

	if not checker.formatCheck(dataLines, len(Dataset.columns)):
		print checker.formatErrorMessage

	upperCaseLines = doUpperCase(dataLines)
	changedUrlsLines = changeURLs(upperCaseLines)
	fixedSizeTypesLines = fixSizeTypes(changedUrlsLines)
	mergedDataLines = mergeSynonymousSizeTypes(fixedSizeTypesLines)
	fixedSizesLines = getFixedSizesLines(mergedDataLines)

	return fixedSizesLines




# makes all column data upperCase (exceptions are the url and size columns)
def doUpperCase(dataLines):
		
	upperCaseLines = []

	dataset = Dataset(dataLines)

	for line in dataset.dataLines:

		columns = dataset.getColumns(line)

		columns['size_type'] = columns['size_type'].upper()
		columns['label'] = columns['label'].upper()
		columns['brand'] = columns['brand'].upper()
		columns['clothe_category'] = columns['clothe_category'].upper()
		columns['size_category'] = columns['size_category'].upper()
		columns['gender'] = columns['gender'].upper()

		upperCaseLines.append( dataset.getLine(columns) )

	return upperCaseLines


# sets the correct brands' urls
def changeURLs(dataLines):

	changedUrlsLines = []

	dataset = Dataset(dataLines)

	for line in dataset.dataLines:

		columns = dataset.getColumns(line)
		columns['url'] = Brand.brandsUrls[ columns['brand'] ]
		changedUrlsLines.append( dataset.getLine(columns) )

	return changedUrlsLines


# fix sizeTypes names
# { INSIDE LEG -> INSIDE_LEG, BACK LENGTH -> BACK_LENGTH, etc. }
def fixSizeTypes(dataLines):
		
	fixedDataLines = []

	dataset = Dataset(dataLines)

	for line in dataset.dataLines:

		columns = dataset.getColumns(line)
		columns['size_type'] = columns['size_type'].replace(" ", "_")
		fixedDataLines.append( dataset.getLine(columns) )

	return fixedDataLines


# merge synonymous sizeTypes
# { hip -> hips, sleeve - sleeve length, back -> back_length }
def mergeSynonymousSizeTypes(dataLines):
		
	mergedDataLines = []

	dataset = Dataset(dataLines)

	for line in dataset.dataLines:

		columns = dataset.getColumns(line)

		if columns['size_type'] in SizeType.mergedSizeTypes:
			columns['size_type'] = SizeType.mergedSizeTypes[ columns['size_type'] ]

		mergedDataLines.append( dataset.getLine(columns) )

	return mergedDataLines


# get the lines with the sizes fixed
def getFixedSizesLines(dataLines):

	outLines = []

	sizesDataset = SizesDataset(dataLines)

	brands = sizesDataset.brands()
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

		if (brand == columns[3]) and (clotheCat == columns[5]) and (sizeCat == columns[6]) and (sizeType == columns[0]):

			# fix XX,XX to XX.XX
			columns[1] = columns[1].replace(",", ".")

			sizes.append(columns[1])

			tt = columns[1].split('-')

			labelsList.append( columns[2] )

			labels[str(float(tt[0]))] = columns[2]

			url = columns[4]
			gender = columns[7]

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
								 '\t' + url + '\t' + clotheCat + '\t' + sizeCat + '\t' + gender)

		elif len(set(sizes)) == 1:

			for label in labelsList:

				outSize = sizes[0] + '-' + sizes[0]

				outLines.append(sizeType + '\t' + outSize + '\t' + label + '\t' + brand +
							 '\t' + url + '\t' + clotheCat + '\t' + sizeCat + '\t' + gender)		
		
	return outLines


