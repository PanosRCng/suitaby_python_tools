try:
	import sys
	from IO import IO
	from Sizes import Sizes
	from People import People
	from SizeCatalog import SizeCatalog
	import MySQLdb
except ImportError:
	print '(!) module do not found'	
	exit()


#
# DBHelper module
#
# helps to construct a database schema and to make queries
#


class DBHelper():

	#constructor
	def __init__(self, databaseName, sizesFilename, peopleFilename, sizeCatalogFilename):

		self.databaseName = databaseName

		# (!) change this line to make it work
		# connect with database
		self.db = MySQLdb.connect(host="****", user="****", passwd="****", db=self.databaseName)

		self.io = IO()

		sizesDataLines = self.io.ReadFile(sizesFilename)
		peopleDataLines = self.io.ReadFile(peopleFilename)
		sizeCatalogDataLines = self.io.ReadFile(sizeCatalogFilename)

		self.sizes = Sizes(sizesDataLines)
		self.people = People(peopleDataLines)
		self.sizeCatalog = SizeCatalog(sizeCatalogDataLines)


	# constructs the db schema
	def constructDbSchema(self):

		self.createSizeCatalogTable("SIZE_CATALOG")	
		entriesDict = self.populateSizeCatalogTable("SIZE_CATALOG")

		self.createSizeTypesTables()
		self.createSizeTypesIndexes('left_limit')

		self.populateSizeTypesTables(entriesDict)	


	# populate size catalog table
	def populateSizeCatalogTable(self, tableName):

		entriesDict = {}

		for line in self.sizeCatalog.sizeCatalogDataLines:

			columns = line.split("\t")

			clothe_category = columns[0]
			label = columns[1]
			size_category = columns[2]
			size_type_projections = columns[3]
			brand = columns[4]
			parts = columns[5].split("\n")
			url = parts[0]

			value = '"' + clothe_category + '", "' + label + '", "' + size_category + '", "' + size_type_projections + '", "' + brand + '", "' + url + '"'

			entry_id = self.insertIntoSizeCatalogTable(tableName, value)

			key = clothe_category + " : " + label + " : " + size_category + " : " + brand + " : " + url 

			entriesDict[key] = entry_id

		return entriesDict


	# insert entry into size catalog entry
	def insertIntoSizeCatalogTable(self, tableName, value):

		cur = self.db.cursor() 

		query = self.getSizeCatalogInsertionQuery(tableName, value)

		cur.execute(query)

		for row in cur.fetchall():
		    	print row[0]

		entry_id = cur.lastrowid 

		self.db.commit()

		return entry_id


	# populate sizeTypes table
	def populateSizeTypesTables(self, entriesDict):

		sizeTypesList = self.sizes.getSizeTypesList()

		for sizeType in sizeTypesList:
	
			values = []

			for line in self.sizes.sizesDataLines:

				columns = line.split('\t')

				if columns[0].upper() == sizeType:

					limits = columns[1].split('-')
					sc = columns[6].split('\n')

					left_limit = limits[0]
					right_limit = limits[1]
					label = columns[2].upper()
					brand = columns[3].upper()
					url = columns[4]
					clothe_category = columns[5].upper()
					size_category = sc[0].upper()


					key = clothe_category + " : " + label + " : " + size_category + " : " + brand + " : " + url  

					value = left_limit + ', ' + right_limit + ', ' + str(entriesDict[key]) + ', "' + label + '", "' + brand + '", "' + url + '", "' + clothe_category + '", "' + size_category + '"'

					values.append(value)

			tableName = sizeType.replace(" ", "_")
		
			self.insertIntoTable(tableName, values)


	# insert entries into sizeType table
	def insertIntoTable(self, tableName, values):

		cur = self.db.cursor() 

		for value in values:
			
			query = self.getSizeTypeInsertionQuery(tableName, value)
		
			cur.execute(query)

			for row in cur.fetchall():
		    		print row[0]

		self.db.commit()


	# returns size catalog insertion query
	def getSizeCatalogInsertionQuery(self, tableName, value):

		query = 'insert into ' + tableName + ' (clothe_category, label, size_category, size_type_projection, brand, url) values('  + value +  ')'

		return query


	# returns a query for the insertion of a sizeType table
	def getSizeTypeInsertionQuery(self, tableName, value):

		query = 'insert into ' + tableName + ' (left_limit, right_limit, size_id, label, brand, url, clothe_category, size_category) values('  + value +  ')'

		return query


	# create sizeTypes tables
	def createSizeTypesTables(self):
	
		sizeTypesList = self.sizes.getSizeTypesList()

		for sizeType in sizeTypesList:

			tableName = sizeType.replace(" ", "_")

			self.createSizeTypeTable(tableName)


	def createSizeTypeTable(self, tableName):

		cur = self.db.cursor() 

		query = self.getSizeTypeCreationQuery(tableName)

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()


	# create size catalog table
	def createSizeCatalogTable(self, tableName):

		cur = self.db.cursor() 

		query = self.getSizeCatalogCreationQuery(tableName)

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()


	# creates an index to a specific column, for all sizeType tables
	def createSizeTypesIndexes(self, columnName):

		sizeTypesList = self.sizes.getSizeTypesList()

		for sizeType in sizeTypesList:

			tableName = sizeType.replace(" ", "_")

			self.createIndex(tableName, columnName)


	# creates an index for a table to a specific column
	def createIndex(self, tableName, columnName):

		cur = self.db.cursor() 	

		query = 'alter table ' + tableName + ' add index (' + columnName +')'	

		cur.execute(query)

		self.db.commit()


	# drops an index to a specific column, for all sizeType tables
	def dropSizeTypesIndexes(self, columnName):

		sizeTypesList = self.sizes.getSizeTypesList()

		for sizeType in sizeTypesList:

			tableName = sizeType.replace(" ", "_")

			self.dropIndex(tableName, columnName)


	# drops an index for a table to a specific column
	def dropIndex(self, tableName, columnName):

		cur = self.db.cursor() 	

		query = 'drop index ' + columnName + ' on ' + tableName	

		try:
			cur.execute(query)
		except:
			pass

		self.db.commit()


	# returns a query for the creation of a sizeType table
	def getSizeTypeCreationQuery(self, tableName):

		query = "create table " + tableName + " (id int auto_increment primary key," + " left_limit float," + " right_limit float," + " size_id int," + " label text(20)," + " brand text(30)," + " url text(256)," + " clothe_category text(50)," + " size_category text(50)" + " )"

		return query


	# returns a query for the creation of a sizeCatalog table
	def getSizeCatalogCreationQuery(self, tableName):

		query = "create table " + tableName + " (id int auto_increment primary key," + " clothe_category text(50)," + " label text(20)," + " size_category text(50)," + " size_type_projection text(256)," + " brand text(30)," + " url text(256)" + " )"

		return query


	# returns a "find a specific clothe_category" query
	def getClotheCategoryQuery(self, clotheCategory, sizes, personSizes):

		tableName = ""

		parts = sizes[0].split(' ')
		tableName = parts[0]

		for i in range(len(parts)):
			if i != 0:
				tableName = tableName + '_' +  parts[i]

		query = 'select brand, url from ' + tableName + ' where (' + personSizes[sizes[0]] + ' between left_limit and right_limit) and (clothe_category="' + clotheCategory + '")'

		if len(sizes) > 1:

			query = '(' + query + ')'

			for i in range(2,len(sizes)):

				tableName = ""

				parts = sizes[i].split(' ')
				tableName = parts[0]

				for i in range(len(parts)):
					if i != 0:
						tableName = tableName + '_' +  parts[i]

				query += ' union '

				query += '(select brand, url from ' + tableName + ' where (' + personSizes[sizes[i]] + ' between left_limit and right_limit) and (clothe_category="' + clotheCategory + '"))'

		return query	


	# returns a "match any clothe" query
	def getMatchClotheQuery(self, sizes, personSizes):

		query = 'select clothe_category, label, size_category, brand, url from SIZE_CATALOG '
		query += 'where (SIZE_CATALOG.id, SIZE_CATALOG.size_type_projection) IN '

		# construct the fits_user table on the fly  
		query += '( select size_id, group_concat(size_type ORDER BY size_type ASC) from ( '


		tableName = sizes[0].replace(" ", "_")

		query += '(select size_id, "' + tableName + '" as size_type from ' + tableName + ' where (' + personSizes[sizes[0]] + ' between left_limit and right_limit))'

		if len(sizes) > 1:

		#	query = '(' + query + ')'

			for i in range(2,len(sizes)):

				tableName = sizes[i-1].replace(" ", "_")

				query += ' union '

				query += '(select size_id, "' + tableName + '" as size_type from ' + tableName + ' where (' + personSizes[sizes[i-1]] + ' between left_limit and right_limit))'

		
		query += ' ) fits_user GROUP BY size_id'

		query += ' )'

		return query


	# submit a query to database
	def queryDB(self, query):

	#	print query + "\n"

		cur = self.db.cursor() 

		cur.execute(query)

	#	for row in cur.fetchall():
	#	    	print row

	#	print "\n\n"

		self.db.commit()


