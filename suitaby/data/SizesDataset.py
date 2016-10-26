try:
	from Dataset import Dataset
	from ClotheCategory import ClotheCategory
except ImportError:
	print 'SizesDataset -- (!) module do not found'	
	exit()


#
# SizesDataset class
#
# 
#

class SizesDataset(Dataset, object):

	#constructor 
	def __init__(self, dataLines):
		super(SizesDataset, self).__init__(dataLines)


	# returns a dictionary with the urls for the brands in the brands list
	def getUrls(self, brands):

		# create a dictionary to keep the urls for the brands
		urls = {}

		# for every brand
		for brand in brands:

			# find the url for the brand in dataLines
			for line in self.dataLines:

				# split line to columns using 'tab' 
				columns = line.split('\t')

				# find a line with the brand
				if brand == columns[3]:

					# get the url, and save it to dictionary
					urls[brand] = columns[4]
					break

		return urls


	# get the unique size types for every clothe category
	def getSizeTypes(self):

		# create an empty dictionary to keep the clothe_category stats
		clotheCatStats = {}

		clotheCats = self.clothe_categories()

		# create an empty dictionary to keep the size_type stats
		clotheSizeTypeStats = {}

		for clotheCat in clotheCats:
	
			# a list to keep the size types used for this clothe category 
			sizeTypes = []

			for line in self.dataLines:
		
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

		clotheCats = self.clothe_categories()

		# create an empty dictionary to keep the size_category stats
		clotheSizeCatsStats = {}

		for clotheCat in clotheCats:

			# a list to keep the size categories used for this clothe category 
			sizeCats = []

			for line in self.dataLines:
		
				columns = line.split('\t')

				if clotheCat == columns[5].upper():

					# just split the next line character
					terms = columns[6].split('\n')

					sizeCats.append( terms[0].upper() )

			uniqueSizeCats = set(sizeCats)

			clotheCatStats[clotheCat] = uniqueSizeCats

		return clotheCatStats


	# finds the size type projections for every size catalog entry
	# returns a dictionary projections[size_catalog_entry] = "[sizeType_1, sizeType_2,]" 
	def getSizeTypesProjections(self):
		
		groupDict = {}

		# for every line
		for line_i in self.dataLines:
		
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
			for line_j in self.dataLines:
		
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

			if clothe_category not in ClotheCategory.invertedIndex.keys():

				ps = clothe_category.split(" ")

				p_exists = False
				uknown = []

				for p in ps:
					if p in ClotheCategory.invertedIndex.keys():
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


	# get the list with all the unique size types
	def getSizeTypesList(self):

		sizeTypesSet = []

		catSizeTypes = self.getSizeTypes()

		for i in catSizeTypes:
		
			sizeTypes = catSizeTypes[i]

			for sizeType in sizeTypes:
			
				sizeTypesSet.append(sizeType)

	
		return list(set(sizeTypesSet))


