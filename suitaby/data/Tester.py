#
#
#	!!!  outdated  !!!
#

try:
	import sys
	import time
	from DBHelper import DBHelper
except ImportError:
	print '(!) module do not found'	
	exit()


#
# Tester module
#
# makes some query tests to database
#


class Tester():

	#constructor 
	def __init__(self, databaseName, sizesFilename, peopleFilename, sizeCatalogFile):

		self.dbHelper = DBHelper(databaseName, sizesFilename, peopleFilename, sizeCatalogFile)

		#self.doClotheCategoryTest()
		self.doMatchClotheTest()


	# (!!!) (fix this)
	# does the "clothe category" test 
	def doClotheCategoryTest(self):

		peoples = self.dbHelper.people.peopleDataLines

		clotheCategories = self.dbHelper.sizes.getClotheCategories()

		catSizeTypes = self.dbHelper.sizes.getSizeTypes()

		# create the people size map 
		peopleSizeMap = {}

		sizeTypesList = self.dbHelper.sizes.getSizeTypesList()

		for i in range(len(sizeTypesList)):
			peopleSizeMap[sizeTypesList[i]] = i+1
		

		# test start time
		start_time = time.time()

		for people in peoples:

			parts = people.split('\t')

			for clotheCategory in clotheCategories:

				personSizes = {}
				sizesList = []
	
				sizes = catSizeTypes[clotheCategory]

				for size in sizes:
	
					personSizes[size.upper()] = parts[peopleSizeMap[size]]
					sizesList.append(size.upper())

				query = self.dbHelper.getClotheCategoryQuery(clotheCategory, sizesList, personSizes)

				self.dbHelper.queryDB(query)

		# elapsed time
		elapsed_time = time.time() - start_time

		print 'clothe category test lasted: ' + str(elapsed_time)


	# does the "match clothe" test
	def doMatchClotheTest(self):

		peoples = self.dbHelper.people.peopleDataLines

		# create the people size map 
		peopleSizeMap = {}

		sizeTypesList = self.dbHelper.sizes.getSizeTypesList()

		for i in range(len(sizeTypesList)):
			peopleSizeMap[sizeTypesList[i]] = i+1

		# test start time
		start_time = time.time()

		for people in peoples:

			parts = people.split('\t')

			personSizes = {}

			for sizeType in sizeTypesList:
	
				personSizes[sizeType.upper()] = parts[peopleSizeMap[sizeType]]

			query = self.dbHelper.getMatchClotheQuery(sizeTypesList, personSizes)

			self.dbHelper.queryDB(query)

		# elapsed time
		elapsed_time = time.time() - start_time

		print 'match clothe test lasted: ' + str(elapsed_time)



