#
# Dataset class
#
# 
#



try:
	import checker
except ImportError:
	print 'Dataset -- (!) module do not found'	
	exit()



class Dataset():

	columns = [
		   'size_type',
		   'size',
		   'label',
          	   'brand',
		   'url',
		   'clothe_category',
		   'size_category',
		   'gender'
		   ]

	#constructor 
	def __init__(self, dataLines):

		self.dataLines = []

		if not checker.formatCheck(dataLines, len(self.columns)):
			print checker.formatErrorMessage
		else:
			self.dataLines = dataLines


	# returns a list with the unique entries in this dataset
	def __getEntries(self, column):

		# create an empty list to keep the entries
		entries = []

		# for every line
		for line in self.dataLines:

			# split line to columns using 'tab' 
			columns = line.split('\t')

			# save entrie to entries list
			entries.append(columns[column])

		# get the unique entries list
		uniqueEntries = set(entries)

		return list(uniqueEntries)


	# returns a list with the unique size_types in this dataset
	def size_types(self):
		return self.__getEntries(0)


	# returns a list with the unique sizes in this dataset
	def sizes(self):
		return self.__getEntries(1)


	# returns a list with the unique labels in this dataset
	def labels(self):
		return self.__getEntries(2)


	# returns a list with the unique brands in this dataset
	def brands(self):
		return self.__getEntries(3)


	# returns a list with the unique urls in this dataset
	def urls(self):
		return self.__getEntries(4)


	# returns a list with the unique clothe_categories in this dataset
	def clothe_categories(self):
		return self.__getEntries(5)


	# returns a list with the unique size_categories in this dataset
	def size_categories(self):
		return self.__getEntries(6)


	# returns a list with the unique genders in this dataset
	def genders(self):
		return self.__getEntries(7)


	# returns a dictionary with the columns of the given line
	def getColumns(self, line):

		columns = {}

		parts = line.split('\t')

		for i in range(len(self.columns)):
			columns[ self.columns[i] ] = parts[i]

		return columns


	# returns a line from the given columns
	def getLine(self, columns):

		line = ""

		for i in range(len(self.columns)):
			line += columns[ self.columns[i] ] + '\t'

		return line[:-1]
	

	# checks if two lines have the same column values of the given columns_list
	def matchLines(self, line_i, line_j, columns_list = None):

		if columns_list is None:
			columns_list = self.columns

		columns_i = self.getColumns(line_i)
		columns_j = self.getColumns(line_j)

		for column in columns_list:
			if columns_i[column] != columns_j[column]:
				return False

		return True


		


