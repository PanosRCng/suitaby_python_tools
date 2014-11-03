try:
	from FormatChecker import FormatChecker
except ImportError:
	print '(!) module do not found'	
	exit()


#
# Sizes module
#
# helps to extract specific stats about a sizes dataset
#


class Sizes():


	#constructor 
	def __init__(self, dataLines):

		self.sizesDataLines = []

		formatChecker = FormatChecker()

		if not formatChecker.checkSizeFormat(dataLines):
			print '(!) please format these lines, and try again \n'		

		else:
			self.sizesDataLines = dataLines


	# constructs the size catalog
	def constructSizeCatalog(self, sizeTypesProjections):

		sizeCatalog = []

		for key in list(sizeTypesProjections.keys()):
			columns = key.split(" : ")

			brand = columns[0]
			clothe_category = columns[1]
			label = columns[2]
			size_category = columns[3]
			url = columns[4]

			size_types_projection = sizeTypesProjections[key]
			
			dataLine = clothe_category + "\t" + label + "\t" + size_category + "\t" + size_types_projection + "\t" + brand + "\t" + url

			sizeCatalog.append(dataLine)

		return sizeCatalog


	# merge synonymous sizeTypes
	# { hips -> hip, sleeve - sleeve length }
	def mergeSynonymousSizeTypes(self):
		
		mergedDataLines = []

		for line in self.sizesDataLines:

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

			if (size_type.upper() == "HIPS"):
				size_type = "HIP"
			elif (size_type.upper() == "SLEEVE"):
				size_type = "SLEEVE LENGTH"

			mergedLine = size_type + '\t' + size + '\t' + label + '\t' + brand + '\t' + url + '\t' + clothe_category + '\t' + size_category

			mergedDataLines.append(mergedLine)

		return mergedDataLines


	# finds the size type projections for every size catalog entry
	# returns a dictionary projections[size_catalog_entry] = "sizeType_1, sizeType_2," 
	def getSizeTypesProjections(self):
		
		groupDict = {}

		# for every line
		for line_i in self.sizesDataLines:
		
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
			for line_j in self.sizesDataLines:
		
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

					key = brand_i + " : " + clothe_category_i + " : " + label_i + " : " + size_category_i + " : " + url_i

					if key in groupDict:
						groupDict[key].append(size_type_i)
					else:
						sizeList = []
						sizeList.append(size_type_i)
						groupDict[key] = sizeList

		projections = {}

		for key in list(groupDict.keys()):

			sizeTypes =  list(set(groupDict[key]))

			sizeTypes.sort()

			sizeTypes_str = ""

			for sizeType in sizeTypes:
				sizeTypes_str += sizeType.replace(" ", "_") + ","

			projections[key] = sizeTypes_str[:-1]


		return projections



	# get the unique brands
	def getBrands(self):

		# create an empty list to keep the brands
		brands = []

		# for every line
		for line in self.sizesDataLines:

			# split line to columns using 'tab' 
			columns = line.split('\t')

			# upperCase brand columns (uniqueness)
			columns[3] = columns[3].upper()

			# save brand to brands list
			brands.append(columns[3])

		uniqueBrands = set(brands)

		return uniqueBrands


	# get the unique clothe categories
	def getClotheCategories(self):

		# create an empty list to keep the clothe categories
		clothes = []

		# for every line
		for line in self.sizesDataLines:

			# split line to columns using 'tab' 
			columns = line.split('\t')

			# upperCase colthe category columns (uniqueness)
			columns[5] = columns[5].upper()

			# save clothe category to clothes list
			clothes.append(columns[5])

		uniqueClothes = set(clothes)

		return uniqueClothes


	# get the unique size types for every clothe category
	def getSizeTypes(self):

		# create an empty dictionary to keep the clothe_category stats
		clotheCatStats = {}

		clotheCats = self.getClotheCategories()

		# create an empty dictionary to keep the size_type stats
		clotheSizeTypeStats = {}

		for clotheCat in clotheCats:
	
			# a list to keep the size types used for this clothe category 
			sizeTypes = []

			for line in self.sizesDataLines:
		
				columns = line.split('\t')

				if clotheCat == columns[5].upper():

					sizeTypes.append( columns[0].upper() )

			uniqueSizeTypes = set(sizeTypes)

			clotheCatStats[clotheCat] = uniqueSizeTypes

		return clotheCatStats


	# get the unique size categories for every clothe category
	def getSizeCats(self):

		# create an empty dictionary to keep the clothe_category stats
		clotheCatStats = {}

		clotheCats = self.getClotheCategories()

		# create an empty dictionary to keep the size_category stats
		clotheSizeCatsStats = {}

		for clotheCat in clotheCats:

			# a list to keep the size categories used for this clothe category 
			sizeCats = []

			for line in self.sizesDataLines:
		
				columns = line.split('\t')

				if clotheCat == columns[5].upper():

					# just split the next line character
					terms = columns[6].split('\n')

					sizeCats.append( terms[0].upper() )

			uniqueSizeCats = set(sizeCats)

			clotheCatStats[clotheCat] = uniqueSizeCats

		return clotheCatStats


	# get the lines with the sizes fixed
	def getFixedLines(self):

		outLines = []

		brands = self.getBrands()
		catSizeTypes = self.getSizeTypes()
		catSizeCategories = self.getSizeCats()

		for brand in brands:		

			for clotheCat in catSizeTypes:

				sizeTypes = catSizeTypes[clotheCat]
				sizeCats = catSizeCategories[clotheCat]

				for sizeCat in sizeCats:

					for sizeType in sizeTypes:

						fixedLines = self.fixSizes(brand, clotheCat, sizeCat, sizeType)

						for fixedLine in fixedLines:
							outLines.append(fixedLine)

		return outLines


	def fixSizes(self, brand, clotheCat, sizeCat, sizeType):

		outLines = []
		sizes = []
		labels = {}
		labelsList = []
		linesCounter = 0

		for line in self.sizesDataLines:

			columns = line.split('\t')

			# just split the next line character
			terms = columns[6].split('\n')		

			if (brand == columns[3].upper()) and (clotheCat == columns[5].upper()) and (sizeCat == terms[0].upper()) and (sizeType == columns[0]):

				sizes.append(columns[1])

				tt = columns[1].split('-')

				labelsList.append( columns[2].upper() )

				labels[str(float(tt[0]))] = columns[2].upper()

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


	# get the sizes for a specific set [ clotheCategory, sizeCategory, sizeType ] 
	def getSizes(self, clotheCat_i, sizeCat_i, sizeType_i):

		sizes = []

		for line in self.sizesDataLines:

			columns = line.split('\t')

			# just split the next line character
			terms = columns[6].split('\n')		

			if (clotheCat_i == columns[5].upper()) and (sizeCat_i == terms[0].upper()) and (sizeType_i == columns[0]):
						
				sizes.append(columns[1])

		return sizes


	# get the list with all the unique size types
	def getSizeTypesList(self):

		sizeTypesSet = []

		catSizeTypes = self.getSizeTypes()

		for i in catSizeTypes:
		
			sizeTypes = catSizeTypes[i]

			for sizeType in sizeTypes:
			
				sizeTypesSet.append(sizeType)

	
		return list(set(sizeTypesSet))


	# get the size bounds (min, max) for every sizeType as dictionary
	# (!) works for size data lines with fixed sizes, see getFixedLines
	def getSizesBounds(self):

		sizesBounds = {}

		sizeTypesList = self.getSizeTypesList()
		
		for sizeType in sizeTypesList:

			bounds = self.getSizeBounds(sizeType)

			sizesBounds[sizeType] = bounds
					
		return sizesBounds


	# get the size bounds (min, max) for a specific sizeType
	# (!) works for size data lines with fixed sizes, see getFixedLines
	def getSizeBounds(self, sizeType):

		sizes = []
		bounds = []

		for line in self.sizesDataLines:

			columns = line.split('\t')

			# just split the next line character
			terms = columns[6].split('\n')		

			if sizeType == columns[0]:
						
				strSizes = columns[1].split('-')

				sizes.append(float(strSizes[0]))
				sizes.append(float(strSizes[1]))

		bounds.append(min(sizes))
		bounds.append(max(sizes))

		return bounds


