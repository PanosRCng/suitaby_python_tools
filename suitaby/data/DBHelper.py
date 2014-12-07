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
		self.db = MySQLdb.connect(host="localhost", user="root", passwd="root", db=self.databaseName)

		self.io = IO()

		sizesDataLines = self.io.ReadFile(sizesFilename)
		peopleDataLines = self.io.ReadFile(peopleFilename)
		sizeCatalogDataLines = self.io.ReadFile(sizeCatalogFilename)

		self.sizes = Sizes(sizesDataLines)
		self.people = People(peopleDataLines)
		self.sizeCatalog = SizeCatalog(sizeCatalogDataLines)


	# constructs the db schema
	def constructDbSchema(self):

		self.createUserTable()
		self.createSizeTable()
		self.createBrandTable()
		self.createUrlTable()
		self.createLabelTable()
		self.createClotheCategoryTable()
		self.createParentClotheCategoryTable()
		self.createClotheCategoryToParentTable()
		self.createSizeCatalogEntryTable()
		self.createSizeCatalogEntryToClotheCategoryTable()
		self.createSizeTypesTables()

		self.populateUsers()
		brand_ids = self.populateBrands()
		label_ids = self.populateLabels()
		clotheCategories_ids = self.populateClotheCategories()
		entriesDict = self.populateSizeCatalogEntryTable(brand_ids, label_ids, clotheCategories_ids)
		self.populateSizeTypesTables(entriesDict)	

		self.createSizeTypesIndexes('left_limit')



	# populates the clothe_category_to_parent table
	def populateClotheCategories(self):

		parentClotheCategories_ids = self.populateParentClotheCategoriesTable()
		clotheCategories_ids = self.populateClotheCategoriesTable()

		for clotheCategory in self.sizes.clotheCategoriesInvertedIndex.keys():

			if clotheCategory in clotheCategories_ids.keys():
				clothe_category_id = clotheCategories_ids[clotheCategory]

				for parent in self.sizes.clotheCategoriesInvertedIndex[clotheCategory]:

					if parent in parentClotheCategories_ids.keys():
						parent_clothe_category_id = parentClotheCategories_ids[parent]

						self.insertIntoClotheCategoryToParentTable(clothe_category_id, parent_clothe_category_id)

		return clotheCategories_ids

	# populates the parent_clothe_category table
	def populateParentClotheCategoriesTable(self):

		parentClotheCategories_ids = {}

		for parentClotheCategory in self.sizes.getParentClotheCategories():
			
			clotheCategory_entry_id = self.insertIntoParentClotheCategoryTable(parentClotheCategory)

			parentClotheCategories_ids[parentClotheCategory] = clotheCategory_entry_id

		return parentClotheCategories_ids		


	# populates the clothe_category table
	def populateClotheCategoriesTable(self):
		
		clotheCategories_ids = {}

		clotheCategories = self.sizes.getClotheCategoriesList()

		for clotheCategory in clotheCategories:
			
			clotheCategory_entry_id = self.insertIntoClotheCategoryTable(clotheCategory)

			clotheCategories_ids[clotheCategory] = clotheCategory_entry_id

		return clotheCategories_ids


	# populates the label table
	def populateLabels(self):

		label_ids = {}

		labels = self.sizes.getLabels( )

		for label in labels:

			label_entry_id = self.insertIntoLabelTable(label)
			
			label_ids[label] = label_entry_id

		return label_ids


	# populates the brand and url table
	def populateBrands(self):

		brand_ids = {}

		urls = self.sizes.getUrls( self.sizes.getBrands() )

		for brand in urls.keys():

			brand_entry_id = self.insertIntoBrandTable(brand)

			brand_ids[brand] = brand_entry_id

			self.insertIntoUrlTable(urls[brand], brand_entry_id)

		return brand_ids


	# popoluates user and size table
	def populateUsers(self):

		sizeTypesList = self.sizes.getSizeTypesList()

		for line in self.people.peopleDataLines:

			columns = line.split("\t")	

			username = "user_" + columns[0]
			password = "password_" + columns[0] 

			user_entry_id = self.insertIntoUserTable(username, password)

			self.insertIntoSizeTable(user_entry_id, columns[1:], sizeTypesList)


	# insert entry into size_catalog_entry_to_clothe_category table
	def insertIntoSizeCatalogEntryToClotheCategoryTable(self, size_catalog_entry_id, clothe_category_id):

		cur = self.db.cursor() 

		query = self.getSizeCatalogEntryToClotheCategoryInsertionQuery(size_catalog_entry_id, clothe_category_id)

		cur.execute(query)

		for row in cur.fetchall():
		    	print row[0]

		entry_id = cur.lastrowid 

		self.db.commit()

		return entry_id


	# insert entry into clothe_category_to_parent table
	def insertIntoClotheCategoryToParentTable(self, clothe_category_id, parent_clothe_category_id):

		cur = self.db.cursor() 

		query = self.getClotheCategoryToParentInsertionQuery(clothe_category_id, parent_clothe_category_id)

		cur.execute(query)

		for row in cur.fetchall():
		    	print row[0]

		entry_id = cur.lastrowid 

		self.db.commit()

		return entry_id


	# insert entry into parent_clothe_category table
	def insertIntoParentClotheCategoryTable(self, parentClotheCategory):

		cur = self.db.cursor() 

		query = self.getParentClotheCategoryInsertionQuery(parentClotheCategory)

		cur.execute(query)

		for row in cur.fetchall():
		    	print row[0]

		entry_id = cur.lastrowid 

		self.db.commit()

		return entry_id


	# insert entry into clothe_category table
	def insertIntoClotheCategoryTable(self, clotheCategory):

		cur = self.db.cursor() 

		query = self.getClotheCategoryInsertionQuery(clotheCategory)

		cur.execute(query)

		for row in cur.fetchall():
		    	print row[0]

		entry_id = cur.lastrowid 

		self.db.commit()

		return entry_id


	# insert entry into label table
	def insertIntoLabelTable(self, label):

		cur = self.db.cursor() 

		query = self.getLabelInsertionQuery(label)

		cur.execute(query)

		for row in cur.fetchall():
		    	print row[0]

		entry_id = cur.lastrowid 

		self.db.commit()

		return entry_id


	# insert entry into brand table
	def insertIntoBrandTable(self, brand):

		cur = self.db.cursor() 

		query = self.getBrandInsertionQuery(brand)

		cur.execute(query)

		for row in cur.fetchall():
		    	print row[0]

		entry_id = cur.lastrowid 

		self.db.commit()

		return entry_id


	# returns a brand insertion query
	def getBrandInsertionQuery(self, brand):

		value = '"' + brand + '"'

		query = 'insert into brand (name) values('  + value +  ')'

		return query


	# returns a label insertion query
	def getLabelInsertionQuery(self, label):

		value = '"' + label + '"'

		query = 'insert into label (name) values('  + value +  ')'

		return query


	# returns a size_catalog_entry_to_clothe_category insertion query
	def getSizeCatalogEntryToClotheCategoryInsertionQuery(self, size_catalog_entry_id, clothe_category_id):

		value = str(size_catalog_entry_id) + ", " + str(clothe_category_id)

		query = 'insert into size_catalog_entry_to_clothe_category (size_catalog_entry_id, clothe_category_id) values('  + value +  ')'

		return query


	# returns a clothe_category_to_parent insertion query
	def getClotheCategoryToParentInsertionQuery(self, clothe_category_id, parent_clothe_category_id):

		value = str(clothe_category_id) + ", " + str(parent_clothe_category_id)

		query = 'insert into clothe_category_to_parent (clothe_category_id, parent_clothe_category_id) values('  + value +  ')'

		return query


	# returns a parent_clothe_category insertion query
	def getParentClotheCategoryInsertionQuery(self, parentClotheCategory):

		value = '"' + parentClotheCategory + '"'

		query = 'insert into parent_clothe_category (name) values('  + value +  ')'

		return query


	# returns a clothe_category insertion query
	def getClotheCategoryInsertionQuery(self, clotheCategory):

		value = '"' + clotheCategory + '"'

		query = 'insert into clothe_category (name) values('  + value +  ')'

		return query


	# insert entry into url table
	def insertIntoUrlTable(self, url, brand_id):

		cur = self.db.cursor() 

		query = self.getUrlInsertionQuery(url, brand_id)

		cur.execute(query)

		for row in cur.fetchall():
		    	print row[0]

		self.db.commit()


	# returns a url insertion query
	def getUrlInsertionQuery(self, url, brand_id):

		value = '"' + url + '", ' + str(brand_id)

		query = 'insert into url (link, brand_id) values('  + value +  ')'

		return query


	# insert entry into size table
	def insertIntoSizeTable(self, user_id, sizes, sizeTypesList):

		cur = self.db.cursor() 

		query = self.getSizeInsertionQuery(user_id, sizes, sizeTypesList)

		cur.execute(query)

		for row in cur.fetchall():
		    	print row[0]

		self.db.commit()


	# returns a size insertion query
	def getSizeInsertionQuery(self, user_id, sizes, sizeTypesList):

		value = str(user_id) + ', '

		for size in sizes:
			value += str(size) + ', ' 		

		query = 'insert into size (user_id, '

		for sizeType in sizeTypesList:

			sizeType = sizeType.replace(" ", "_")

			query += sizeType + "_point,"

		query = query[:-1]

		query += ') values('  + value[:-2] +  ')'

		return query


	# insert entry into user table
	def insertIntoUserTable(self, username, password):

		cur = self.db.cursor() 

		query = self.getUserInsertionQuery(username, password)

		cur.execute(query)

		for row in cur.fetchall():
		    	print row[0]

		entry_id = cur.lastrowid 

		self.db.commit()

		return entry_id


	# returns a user insertion query
	def getUserInsertionQuery(self, username, password):

		value = '"' + username + '", "' + password + '"'

		query = 'insert into user (username, password) values('  + value +  ')'

		return query


	# creates the patent_clothe_category table
	def createParentClotheCategoryTable(self):

		cur = self.db.cursor() 

		query = self.getParentClotheCategoryCreationQuery()

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()


	# creates the clothe_category_to_parent table
	def createClotheCategoryToParentTable(self):

		cur = self.db.cursor() 

		query = self.getClotheCategoryToParentCreationQuery()

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()


	# creates the size_catalog_entry_to_clothe_category table
	def createSizeCatalogEntryToClotheCategoryTable(self):

		cur = self.db.cursor() 

		query = self.getSizeCatalogEntryToClotheCategoryCreationQuery()

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()


	# creates the clothe_category table
	def createClotheCategoryTable(self):

		cur = self.db.cursor() 

		query = self.getClotheCategoryCreationQuery()

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()


	# creates the label table
	def createLabelTable(self):

		cur = self.db.cursor() 

		query = self.getLabelCreationQuery()

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()


	# creates the user table
	def createUserTable(self):

		cur = self.db.cursor() 

		query = self.getUserCreationQuery()

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()


	# creates the size table
	def createSizeTable(self):

		cur = self.db.cursor() 

		query = self.getSizeCreationQuery()

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()


	# creates the brand table
	def createBrandTable(self):

		cur = self.db.cursor() 

		query = self.getBrandCreationQuery()

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()


	# creates the url table
	def createUrlTable(self):

		cur = self.db.cursor() 

		query = self.getUrlCreationQuery()

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()


	# populates the size_catalog_entry table
	def populateSizeCatalogEntryTable(self, brand_ids, label_ids, clotheCategories_ids):

		entriesDict = {}

		for line in self.sizeCatalog.sizeCatalogDataLines:

			columns = line.split("\t")

			clothe_category_column = columns[0]
			label = columns[1]
			size_category = columns[2]
			size_type_projection = columns[3]
			brand = columns[4]
			parts = columns[5].split("\n")
			url = parts[0]

			value = '"' + size_type_projection + '", "' + size_category + '", ' + str(brand_ids[brand]) + ', ' + str(label_ids[label])

			entry_id = self.insertIntoSizeCatalogEntryTable(value)

			key = clothe_category_column + " : " + label + " : " + size_category + " : " + brand + " : " + url 

			entriesDict[key] = entry_id

			

			for clotheCategory in self.sizes.splitClotheCategory(clothe_category_column):

				self.insertIntoSizeCatalogEntryToClotheCategoryTable(entry_id, clotheCategories_ids[clotheCategory])

		return entriesDict


	# insert entry into size_catalog_entry table
	def insertIntoSizeCatalogEntryTable(self, value):

		cur = self.db.cursor() 

		query = self.getSizeCatalogEntryInsertionQuery(value)

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

				if columns[0] == sizeType:

					limits = columns[1].split('-')
					sc = columns[6].split('\n')

					left_limit = limits[0]
					right_limit = limits[1]
					label = columns[2]
					brand = columns[3]
					url = columns[4]
					clothe_category = columns[5]
					size_category = sc[0]


					key = clothe_category + " : " + label + " : " + size_category + " : " + brand + " : " + url  

					value = str(entriesDict[key]) + ', ' + left_limit + ', ' + right_limit

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


	# returns a size_catalog_entry insertion query
	def getSizeCatalogEntryInsertionQuery(self, value):

		query = 'insert into size_catalog_entry (size_type_projection, size_category, brand_id, label_id) values('  + value +  ')'

		return query


	# returns a query for the insertion of a sizeType table
	def getSizeTypeInsertionQuery(self, tableName, value):

		query = 'insert into ' + tableName + ' (size_catalog_entry_id, left_limit, right_limit) values('  + value +  ')'

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


	# create size_catalog_entry table
	def createSizeCatalogEntryTable(self):

		cur = self.db.cursor() 

		query = self.getSizeCatalogEntryCreationQuery()

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


	# returns a query for the creation of the parent_clothe_category table
	def getParentClotheCategoryCreationQuery(self):

		query = "create table parent_clothe_category (id int not null auto_increment primary key," + " name text(256) not null" + " )"

		return query


	# returns a query for the creation of the size_catalog_entry_to_clothe_category table
	def getSizeCatalogEntryToClotheCategoryCreationQuery(self):

		query = "create table size_catalog_entry_to_clothe_category (size_catalog_entry_id int not null, clothe_category_id int not null, foreign key (size_catalog_entry_id) references size_catalog_entry(id), foreign key (clothe_category_id) references  clothe_category(id), primary key (size_catalog_entry_id, clothe_category_id) )"

		return query


	# returns a query for the creation of the clothe_category_to_parent table
	def getClotheCategoryToParentCreationQuery(self):

		query = "create table clothe_category_to_parent (clothe_category_id int not null, parent_clothe_category_id int not null, foreign key (clothe_category_id) references clothe_category(id), foreign key (parent_clothe_category_id) references parent_clothe_category(id), primary key (clothe_category_id, parent_clothe_category_id) )"

		return query


	# returns a query for the creation of the clothe_category table
	def getClotheCategoryCreationQuery(self):

		query = "create table clothe_category (id int not null auto_increment primary key," + " name text(256) not null" + " )"

		return query


	# returns a query for the creation of the label table
	def getLabelCreationQuery(self):

		query = "create table label (id int not null auto_increment primary key," + " name text(256) not null" + " )"

		return query


	# returns a query for the creation of the user table
	def getUserCreationQuery(self):

		query = "create table user (id int not null auto_increment primary key," + " username text(256) not null," + " password text(256) not null" + " )"

		return query


	# returns a query for the creation of the size table
	def getSizeCreationQuery(self):

		sizeTypesList = self.sizes.getSizeTypesList()

		query = "create table size (id int auto_increment not null primary key," + " user_id int not null, "

		for sizeType in sizeTypesList:

			sizeType = sizeType.replace(" ", "_")

			query += sizeType + "_point float, "

		query += "foreign key (user_id) references user(id) )"

		return query


	# returns a query for the creation of the brand table
	def getBrandCreationQuery(self):

		query = "create table brand (id int not null auto_increment primary key," + " name text(256) not null )"

		return query


	# returns a query for the creation of the url table
	def getUrlCreationQuery(self):

		query = "create table url (id int auto_increment not null primary key," + " brand_id int not null, " + " link text(512), "

		query += "foreign key (brand_id) references brand(id) )"

		return query


	# returns a query for the creation of a sizeType table
	def getSizeTypeCreationQuery(self, tableName):

		query = "create table " + tableName + " (id int auto_increment not null primary key, " + "size_catalog_entry_id int not null, " + "left_limit float not null, " + "right_limit float not null, " + "foreign key (size_catalog_entry_id) references size_catalog_entry(id)" + " )"

		return query


	# returns a query for the creation of a size_catalog_entry table
	def getSizeCatalogEntryCreationQuery(self):

		query = "create table size_catalog_entry (id int not null auto_increment primary key, " + "size_type_projection text(256) not null, " + "size_category text(256) not null, " + "brand_id int not null, " + "label_id int not null, " + "foreign key (brand_id) references brand(id), " + "foreign key (label_id) references label(id)" + " )"

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


