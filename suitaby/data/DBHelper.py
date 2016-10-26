try:
	import sys
	import MySQLdb

	import io
	from ClotheCategory import ClotheCategory
	from Brand import Brand
	from SizesDataset import SizesDataset
	from SizeType import SizeType
	from SizeCatalog import SizeCatalog

#	from People import People
except ImportError:
	print 'DBHelpder -- (!) module do not found'	
	exit()


#
# DBHelper class
#
# helps to construct a database schema and to make queries
#


class DBHelper():

	#constructor
	def __init__(self, databaseName, sizesFilename, sizeCatalogFilename):

		self.databaseName = databaseName

		# (!) change this line to make it work
		# connect with database
		self.db = MySQLdb.connect(host="localhost", user="root", passwd="root", db=self.databaseName, charset='utf8')

		sizesDataLines = io.ReadFile(sizesFilename)
		sizeCatalogDataLines = io.ReadFile(sizeCatalogFilename)

		self.sizesDataset = SizesDataset( sizesDataLines )

		self.sizeCatalog = SizeCatalog(sizeCatalogDataLines)


	# constructs the db schema
	def constructDbSchema(self):

		self.createUserTable()
		self.createSizeTable()
		self.createPredictedSizeTable()
		self.createSizeConfidenceTable()
		self.createBrandTable()
		self.createUrlTable()
		self.createLabelTable()
		self.createClotheCategoryTable()
		self.createParentClotheCategoryTable()
		self.createClotheCategoryToParentTable()
		self.createSizeCatalogEntryTable()
		self.createSizeCatalogEntryToClotheCategoryTable()
		self.createSizeTypesTables()
		self.createUsersLogsTable()
		self.createPostsTable()
		self.createPostsCategoriesRelationshipTable()
	
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

		for clotheCategory in ClotheCategory.invertedIndex.keys():

			if clotheCategory in clotheCategories_ids.keys():
				clothe_category_id = clotheCategories_ids[clotheCategory]

				for parent in ClotheCategory.invertedIndex[clotheCategory]:

					if parent in parentClotheCategories_ids.keys():
						parent_clothe_category_id = parentClotheCategories_ids[parent]

						self.insertIntoClotheCategoryToParentTable(clothe_category_id, parent_clothe_category_id)

		return clotheCategories_ids

	# populates the parent_clothe_category table
	def populateParentClotheCategoriesTable(self):

		parentClotheCategories_ids = {}

		for parentClotheCategory in ClotheCategory.parentClotheCategories:
			
			clotheCategory_entry_id = self.insertIntoParentClotheCategoryTable(parentClotheCategory)

			parentClotheCategories_ids[parentClotheCategory] = clotheCategory_entry_id

		return parentClotheCategories_ids		


	# populates the clothe_category table
	def populateClotheCategoriesTable(self):
		
		clotheCategories_ids = {}

		for clotheCategory in ClotheCategory.clotheCategories:
			
			clotheCategory_entry_id = self.insertIntoClotheCategoryTable(clotheCategory)

			clotheCategories_ids[clotheCategory] = clotheCategory_entry_id

		return clotheCategories_ids


	# populates the label table
	def populateLabels(self):

		label_ids = {}

		labels = self.sizesDataset.labels( )

		for label in labels:

			label_entry_id = self.insertIntoLabelTable(label)
			
			label_ids[label] = label_entry_id

		return label_ids


	# populates the brand and url table
	def populateBrands(self):

		brand_ids = {}

		urls = Brand.brandsUrls

		for brand in urls.keys():

			brand_ids[brand] = self.insertIntoBrandTable(brand)

			self.insertIntoUrlTable(urls[brand], brand_ids[brand])

		return brand_ids


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


	# creates the predicted size table
	def createPredictedSizeTable(self):

		cur = self.db.cursor() 

		query = self.getPredictedSizeCreationQuery()

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()


	# creates the predicted size table
	def createSizeConfidenceTable(self):

		cur = self.db.cursor() 

		query = self.getSizeConfidenceCreationQuery()

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()


	# creates the blog posts table
	def createPostsTable(self):

		cur = self.db.cursor() 

		query = self.getPostsCreationQuery()

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()


	# creates the blog post category table
	def createPostsCategoriesRelationshipTable(self):

		cur = self.db.cursor() 

		query = self.getPostsCategoriesRelationshipCreationQuery()

		cur.execute(query)

		for row in cur.fetchall() :
		    print row[0]

		self.db.commit()		


	# creates the users_logs table
	def createUsersLogsTable(self):

		cur = self.db.cursor() 

		query = self.getUsersLogsCreationQuery()

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

		for line in self.sizeCatalog.dataLines:

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

			

			for clotheCategory in self.sizesDataset.splitClotheCategory(clothe_category_column):

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

		for sizeType in SizeType.sizeTypes:
	
			values = []

			for line in self.sizesDataset.dataLines:

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

		for sizeType in SizeType.sizeTypes:

			tableName = sizeType.replace(" ", "_")

			self.createSizeTypeTable(tableName)


	def createSizeTypeTable(self, tableName):

		cur = self.db.cursor() 

		query = self.getSizeTypeCreationQuery(tableName)

		print query

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

		for sizeType in SizeType.sizeTypes:

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

		for sizeType in SizeType.sizeTypes:

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

		query = ("create table parent_clothe_category ("
			 "id int(10) unsigned not null primary key auto_increment,"
			 "name varchar(255) not null"
			 ")")

		return query


	# returns a query for the creation of the size_catalog_entry_to_clothe_category table
	def getSizeCatalogEntryToClotheCategoryCreationQuery(self):

		query = ("create table size_catalog_entry_to_clothe_category ("
			 "size_catalog_entry_id int(10) unsigned not null,"
			 "clothe_category_id int(10) unsigned not null,"
			 "foreign key (size_catalog_entry_id) references size_catalog_entry(id),"
			 "foreign key (clothe_category_id) references  clothe_category(id),"
			 "primary key (size_catalog_entry_id, clothe_category_id)"
			 ")")

		return query


	# returns a query for the creation of the clothe_category_to_parent table
	def getClotheCategoryToParentCreationQuery(self):

		query = ("create table clothe_category_to_parent ("
			 "clothe_category_id int(10) unsigned not null,"
			 "parent_clothe_category_id int(10) unsigned not null,"
			 "foreign key (clothe_category_id) references clothe_category(id),"
			 "foreign key (parent_clothe_category_id) references parent_clothe_category(id),"
			 "primary key (clothe_category_id, parent_clothe_category_id)"
			 ")")

		return query


	# returns a query for the creation of the clothe_category table
	def getClotheCategoryCreationQuery(self):

		query = ("create table clothe_category ("
			 "id int(10) unsigned not null primary key auto_increment,"
			 "name varchar(255) not null"
			 ")")

		return query


	# returns a query for the creation of the label table
	def getLabelCreationQuery(self):

		query = ("create table label ("
			 "id int(10) unsigned not null primary key auto_increment,"
			 "name varchar(255) not null"
			 ")")

		return query


	# returns a query for the creation of the user table
	def getUserCreationQuery(self):

		query = ("create table users ("
			 "id int(10) unsigned not null primary key auto_increment,"
			 "username varchar(255) not null,"
			 "email varchar(255) not null unique,"
			 "password varchar(60) not null,"
			 "dob date,"
			 "gender varchar(10) not null,"
			 "created_at timestamp not null default '0000-00-00 00:00:00',"
			 "updated_at timestamp not null default '0000-00-00 00:00:00',"
			 "remember_token varchar(100)"
			 ")")

		return query


	# returns a query for the creation of the size table
	def getSizeCreationQuery(self):

		query = ("create table sizes ("
			 "id int(10) unsigned not null primary key auto_increment,"
			 "user_id int(10) unsigned not null unique, ")

		for sizeType in SizeType.sizeTypes:

			sizeType = sizeType.replace(" ", "_")
			sizeType = sizeType.lower()

			query += sizeType + " float, "

		query += "foreign key (user_id) references users(id) )"

		return query


	# returns a query for the creation of the predicted size table
	def getPredictedSizeCreationQuery(self):

		query = ("create table predicted_sizes ("
			 "id int(10) unsigned not null primary key auto_increment,"
			 "user_id int(10) unsigned not null unique, ")

		for sizeType in SizeType.sizeTypes:

			sizeType = sizeType.replace(" ", "_")
			sizeType = sizeType.lower()

			query += sizeType + " float, "

		query += "foreign key (user_id) references users(id) )"

		return query


	# returns a query for the creation of the size confidence table
	def getSizeConfidenceCreationQuery(self):

		query = ("create table sizes_confidence ("
			 "id int(10) unsigned not null primary key auto_increment,"
			 "user_id int(10) unsigned not null unique, ")

		for sizeType in SizeType.sizeTypes:

			sizeType = sizeType.replace(" ", "_")
			sizeType = sizeType.lower()

			query += sizeType + " float, "

		query += "foreign key (user_id) references users(id) )"

		return query


	# returns a query for the creation of the brand table
	def getBrandCreationQuery(self):

		query = ("create table brand ("
			 "id int(10) unsigned not null primary key auto_increment,"
			 "name varchar(255) not null"
			 ")")

		return query


	# returns a query for the creation of the posts table
	def getPostsCreationQuery(self):

		query = ("create table posts ("
			 "id int(10) unsigned not null primary key auto_increment,"
			 "post_title varchar(255) not null,"
			 "post_body text not null,"
			 "author varchar(255) not null,"
			 "author_id int(10) unsigned not null,"
			 "created_at timestamp not null default '0000-00-00 00:00:00',"
			 "updated_at timestamp not null default '0000-00-00 00:00:00'"
			 ")")

		return query	


	# returns a query for the creation of the post category table
	def getPostsCategoriesRelationshipCreationQuery(self):

		query = ("create table posts_categories_relationship ("
			 "post_id int(10) unsigned not null,"
			 "category_id int(10) unsigned not null,"
			 "created_at timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',"
			 "updated_at timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',"
			 "foreign key (post_id) references posts(id),"
			 "foreign key (category_id) references  parent_clothe_category(id),"
			 "primary key (post_id, category_id)"
			 ")")


		return query


	# returns a query for the creation of the users_logs table
	def getUsersLogsCreationQuery(self):

		query = ("create table users_logs ("
			 "id int(10) unsigned not null primary key auto_increment,"
			 "user_id int(10) unsigned not null,"
			 "time timestamp not null default '0000-00-00 00:00:00',"
			 "action varchar(30) not null,"
			 "details varchar(511),"
		         "foreign key (user_id) references users(id)"
			 ")")

		return query


	# returns a query for the creation of the url table
	def getUrlCreationQuery(self):

		query = ("create table url ("
			 "id int(10) unsigned not null primary key auto_increment,"
			 "brand_id int(10) unsigned not null unique,"
			 "link varchar(511),"
		         "foreign key (brand_id) references brand(id)"
			 ")")

		return query


	# returns a query for the creation of a sizeType table
	def getSizeTypeCreationQuery(self, tableName):

		query = ("create table " + tableName + " ("
			 "id int(10) unsigned not null primary key auto_increment,"
			 "size_catalog_entry_id int(10) unsigned not null,"
			 "left_limit float not null,"
			 "right_limit float not null,"
			 "foreign key (size_catalog_entry_id) references size_catalog_entry(id)"
			 ")")

		return query


	# returns a query for the creation of a size_catalog_entry table
	def getSizeCatalogEntryCreationQuery(self):

		query = ("create table size_catalog_entry ("
			 "id int(10) unsigned not null primary key auto_increment,"
			 "size_type_projection varchar(255) not null,"
			 "size_category varchar(255) not null,"
			 "brand_id int(10) unsigned not null,"
			 "label_id int(10) unsigned not null, "
			 "foreign key (brand_id) references brand(id),"
			 "foreign key (label_id) references label(id)"
			 ")")

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


