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

		# inverted index of clothe category to parent categories list
		self.clotheCategoriesInvertedIndex = { 
						"POLOS" : ["T-SHIRTS"],
						"RUGBYS" : ["T-SHIRTS"],
						"TOPS" : ["T-SHIRTS"],
						"POLO" : ["T-SHIRTS"],
						"SWEATSHIRTS" : ["T-SHIRTS"],
						"T-SHIRTS" : ["T-SHIRTS"],
						"RUGBY" : ["T-SHIRTS"],
						"MEN'S TOPS" : ["T-SHIRTS", "JACKETS & COATS", "SHIRTS", "KNITWEAR"],
						"SHEP SHIRTS" : ["T-SHIRTS"],
						"TEES" : ["T-SHIRTS"],
						"BUSINESS SUITS" : ["SUITS"],
						"SUITS TROUSERS" : ["SUITS"],
						"SUIT" : ["SUITS"],
						"SUITS" : ["SUITS"],
						"TAILORED JACKETS"  : ["SUITS"],
						"COATS" : ["JACKETS & COATS"],
						"OUTERWEAR" : ["JACKETS & COATS"],
						"BLAZERS" : ["JACKETS & COATS"],
						"JACKETS" : ["JACKETS & COATS"],
						"SPORTSWEAR" : ["SPORTSWEAR"],
						"ELASTICATED WAIST TROUSERS" : ["SPORTSWEAR"],
						"SPORT SHIRTS" : ["SPORTSWEAR"],
						"SWIMWEAR" : ["SPORTSWEAR"],
						"TRACK PANTS" : ["SPORTSWEAR"],
						"SHIRTS" : ["SHIRTS"],
						"BUSINESS SHIRTS" : ["SHIRTS"],
						"CASUAL" : ["SHIRTS"],
						"SHIRT" : ["SHIRTS"],
						"DRESS SHIRTS" : ["SHIRTS"],
						"APPAREL (POLO)" : ["APPAREL"],
						"APPAREL" : ["APPAREL"],
						"MERINO" : ["KNITWEAR"],
						"CARDIGANS" : ["KNITWEAR"],
						"PULLOVERS" : ["KNITWEAR"],
						"JUMPERS" : ["KNITWEAR"],
						"KNITWEAR" : ["KNITWEAR"],
						"FLEECE" : ["KNITWEAR"],
						"SWEATERS" : ["KNITWEAR"],
						"BOTTOMS" : ["TROUSERS"],
						"SHORTS" : ["TROUSERS"],
						"MEN'S SHORTS" : ["TROUSERS"],
						"MEN'S BOTTOMS" : ["TROUSERS"],
						"PANTS" : ["TROUSERS"],
						"MEN'S PANTS" : ["TROUSERS"],
						"CHINOS" : ["TROUSERS"],
						"DENIM" : ["TROUSERS"],
						"JEANS" : ["TROUSERS"],
						"TROUSERS" : ["TROUSERS"],
						"BELTS" : ["ACCESSORIES"],
						"SOCKS" : ["ACCESSORIES"],
						"UNDERWEAR" : ["UNDERWEAR"],
						"BOXERS" : ["UNDERWEAR"],
						"SHOES" : ["SHOES"]
					      }

		self.sizesDataLines = []

		formatChecker = FormatChecker()

		if not formatChecker.checkSizeFormat(dataLines):
			print '(!) please format these lines, and try again \n'		

		else:
			self.sizesDataLines = dataLines


	# returns the unique parent clothe categories list from a clothe category column
	def extractParentClotheCategories(self, column):

		parent_clothe_categories = []

		clotheCategories = self.splitClotheCategory(column)

		for clotheCategory in clotheCategories:
			for parent in self.clotheCategoriesInvertedIndex[clotheCategory]:
				parent_clothe_categories.append(parent)

		return set(parent_clothe_categories)


	# returns the unique parent clothe categories
	def getParentClotheCategories(self):

		parent_clothe_categories = []

		for clotheCategory in self.clotheCategoriesInvertedIndex.keys():
			for parent in self.clotheCategoriesInvertedIndex[clotheCategory]:
				parent_clothe_categories.append(parent)

		return set(parent_clothe_categories)

	
	# returns a list with the child clothe categories for a parent_clothe_category
	def getChildClotheCategories(self, parent_clothe_category):	

		child_clothe_categories = []

		if parent_clothe_category not in self.getParentClotheCategories():
			print '(!) the given argument is not a parent clothe category'
			return child_clothe_categories

		for clotheCategory in self.getClotheCategoriesList():
			if parent_clothe_category in  self.clotheCategoriesInvertedIndex[clotheCategory]:
				child_clothe_categories.append( clotheCategory )

		return child_clothe_categories


	# make all column data upperCase (exceptions are the url and size columns)
	def doUpperCase(self):
		
		upperDataLines = []

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

			upperLine = size_type.upper() + '\t' + size + '\t' + label.upper() + '\t' + brand.upper() + '\t' + url + '\t' + clothe_category.upper() + '\t' + size_category.upper()

			upperDataLines.append(upperLine)

		return upperDataLines


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


	# returns a clothe categories list from the clothe category column
	def splitClotheCategory(self, column):

		clotheCategoriesList = []
		
		column = column.replace(",", "_")
		column = column.replace("&", "_")

		parts = column.split("_")

		for part in parts:

			clothe_category = part.strip()

			if clothe_category not in self.clotheCategoriesInvertedIndex.keys():

				ps = clothe_category.split(" ")

				p_exists = False
				uknown = []

				for p in ps:
					if p in self.clotheCategoriesInvertedIndex.keys():
						p_exists = True
						clotheCategoriesList.append(p)
					else:
						uknown.append(p)

				if p_exists:
					for u in uknown:
						print "can not find group for this: " + u + " -> " + clothe_category
				else:
					print "can not find group fo this: " + clothe_category

			else:

				clotheCategoriesList.append(clothe_category)

		return set(clotheCategoriesList)

	
	#
	def changeURLs(self):

		self.brandsUrls = { "MARLBORO" : "http://www.marlborooriginals.co.za/",
				    "TOMMY HILFIGER" : "http://eu.tommy.com/",
				    "TIMBERLAND" : "http://shop.timberland.com/",
				    "REPLAY" : "http://shop.replay.it/",
				    "VANS" : "http://collection.vans.eu/",
				    "BROOKS BROTHERS" : "http://www.brooksbrothers.com/",
				    "MAGEE1866" : "http://www.magee1866.com/",
				    "NAUTICA" : "http://www.nautica.com/",
				    "GANT" : "http://www.gant.co.uk/",
				    "NIKE" : "http://www.nike.com/",
				    "LEE" : "http://www.lee.com/",
				    "WIERD FISH" : "http://www.weirdfish.co.uk/",
				    "LEVI'S" : "http://www.levi.com/",
				    "JOE BROWNS" : "http://www.joebrowns.co.uk/",
				    "DOCKERS" : "http://www.dockers.com/",
				    "BARKERS" : "http://www.barkersonline.co.nz/",
				    "HARRIS TWEED" : "http://harristweedco.co.uk/",
				    "CHATHAM" : "http://www.chatham.co.uk/",
				    "MEYER" : "http://www.meyer-hosen.com/",
				    "VINEYARD VINES" : "http://www.vineyardvines.com/",
				    "JOHN SMEDLEY" : "http://www.johnsmedley.com/",
				    "ITALIAN CLASSICS" : "http://www.highandmighty.co.uk/",
				    "D555" : "http://www.dukeclothing.com/",
				    "POLO" : "-",
				    "BOSS" : "-" }

		changedUrlsDataLines = []

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

			url = self.brandsUrls[ brand ]

			changedUrlLine = size_type + '\t' + size + '\t' + label + '\t' + brand + '\t' + url + '\t' + clothe_category + '\t' + size_category

			changedUrlsDataLines.append(changedUrlLine)

		return changedUrlsDataLines	


	# merge synonymous sizeTypes
	# { hip -> hips, sleeve - sleeve length, back -> back_length }
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

			if (size_type == "HIP"):
				size_type = "HIPS"
			elif (size_type == "SLEEVE"):
				size_type = "SLEEVE LENGTH"
			elif (size_type == "BACK"):
				size_type = "BACK LENGTH"

			mergedLine = size_type + '\t' + size + '\t' + label + '\t' + brand + '\t' + url + '\t' + clothe_category + '\t' + size_category

			mergedDataLines.append(mergedLine)

		return mergedDataLines


	# finds the size type projections for every size catalog entry
	# returns a dictionary projections[size_catalog_entry] = "[sizeType_1, sizeType_2,]" 
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

			# save brand to brands list
			brands.append(columns[3])

		# get the unique brands list
		uniqueBrands = set(brands)

		return uniqueBrands


	# get a dictionary with the urls for the brands in the brands list
	def getUrls(self, brands):

		# create a dictionary to keep the urls for the brands
		urls = {}

		# for every brand
		for brand in brands:

			# find the url for the brand in dataLines
			for line in self.sizesDataLines:

				# split line to columns using 'tab' 
				columns = line.split('\t')

				# find a line with the brand
				if brand == columns[3]:

					# get the url, and save it to dictionary
					urls[brand] = columns[4]
					break

		return urls


	# get the unique labels
	def getLabels(self):

		# create an empty list to keep the labels
		labels = []

		# for every line
		for line in self.sizesDataLines:

			# split line to columns using 'tab' 
			columns = line.split('\t')

			# save label to labels list
			labels.append(columns[2])

		# get the unique labels list
		uniqueLabels = set(labels)

		return uniqueLabels


	# get the clothe categories
	def getClotheCategories(self):

		# create an empty list to keep the clothe categories
		clothes = []

		# for every line
		for line in self.sizesDataLines:

			# split line to columns using 'tab' 
			columns = line.split('\t')

			# save clothe category to clothes list
			clothes.append(columns[5])

		uniqueClothes = set(clothes)

		return uniqueClothes


	# get the unique clothe categories
	def getClotheCategoriesList(self):
		
		clotheCategoriesList = []

		clotheCategoriesColumns = self.getClotheCategories()

		for column in clotheCategoriesColumns:
		
			column = column.replace(",", "_")
			column = column.replace("&", "_")

			parts = column.split("_")

			for part in parts:

				clothe_category = part.strip()

				if clothe_category not in self.clotheCategoriesInvertedIndex.keys():

					ps = clothe_category.split(" ")

					p_exists = False
					uknown = []

					for p in ps:
						if p in self.clotheCategoriesInvertedIndex.keys():
							p_exists = True
							clotheCategoriesList.append(p)
						else:
							uknown.append(p)

					if p_exists:
						for u in uknown:
							print "can not find group for this: " + u + " -> " + clothe_category
					else:
						print "can not find group fo this: " + clothe_category

				else:

					clotheCategoriesList.append(clothe_category)

		uniqueClotheCategoriesList = set(clotheCategoriesList)

		return uniqueClotheCategoriesList


	# get the unique size types for a parent clothe category
	def getSizeTypesParent(self, parentClotheCategory):

		sizeTypes = []

		if parentClotheCategory not in self.getParentClotheCategories():
			print '(!) the given argument is not a parent clothe category'
			return sizeTypes

		sizeTypesDict = self.getSizeTypes()

		for child_clothe_category in self.getChildClotheCategories(parentClotheCategory):
			for key in sizeTypesDict.keys():
				if child_clothe_category in key:
					for sizeType in sizeTypesDict[key]:
						sizeTypes.append(sizeType)

		return list(set(sizeTypes))


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


