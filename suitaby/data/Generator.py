try:
	import sys
	import random
	from IO import IO
	from Sizes import Sizes
except ImportError:
	print '(!) module do not found'	
	exit()


#
# Generator module
#
#
# generates more brands and people data from a given size dataset
#


class Generator():


	#constructor 
	def __init__(self, sizesFilename):

		self.io = IO()

		dataLines = self.io.ReadFile(sizesFilename)

		self.sizes = Sizes(dataLines)


	# generates more brands data
	def GenerateBrands(self, number, outFilename):

		clotheSizeCategories = self.sizes.getSizeCats()
		clotheSizeTypes = self.sizes.getSizeTypes()

		self.io.WriteSizesHeader(outFilename)

		for i in range(number):

			brand = 'brand_'+ str(i)
			url = 'url_' + str(i)

			offset = round(random.random(), 2)

			brandLines = self.PopulateBrand(brand, url, clotheSizeTypes, clotheSizeCategories, offset)

			self.io.WriteFile(outFilename, brandLines, 'a')



	# generates more people data
	def GeneratePeople(self, numPeople, outFilename):

		peopleLines = self.PopulatePeople(numPeople)

		sizeTypesList = self.sizes.getSizeTypesList()

		self.io.WritePeopleHeader(outFilename, sizeTypesList)

		self.io.WriteFile(outFilename, peopleLines, 'a')


	def PopulatePeople(self, numPeople):

		lines = []

		sizesBounds = self.sizes.getSizesBounds()

		for i in range(numPeople):

			line = ""

			line = str(i)

			for size in sizesBounds:

				line += '\t' + str( random.uniform(sizesBounds[size][0], sizesBounds[size][1]) )		

			lines.append(line)

		return lines


	def PopulateBrand(self, brand, url, catSizeTypes, catSizeCategories, offset):

		outLines = []
		
		for clotheCat in catSizeTypes:

			sizeTypes = catSizeTypes[clotheCat]
			sizeCats = catSizeCategories[clotheCat]

			for sizeCat in sizeCats:

				for sizeType in sizeTypes:

					sizesList = self.sizes.getSizes(clotheCat, sizeCat, sizeType)

					for size in sizesList:

						ss = size.split('-')

						newSize = str( float(ss[0])+float(offset) ) + '-' + str( float(ss[1])+float(offset) )

						outLines.append( sizeType + '\t' + newSize + '\t' + '-' + '\t' + brand 
									+ '\t' + url + '\t' + clotheCat + '\t' + sizeCat )
					
		return outLines


