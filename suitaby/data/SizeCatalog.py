try:
	import checker
except ImportError:
	print 'SizeCatalog -- (!) module do not found'	
	exit()


#
# SizeCatalog class
#
# helps to extract specific stats about a size catalog dataset
#


class SizeCatalog():


	columns = [
		   'clothe_category',
		   'label',
		   'size_category',
          	   'size_type_projections',
		   'brand',
		   'url',
		   'gender'
		   ]

	#constructor 
	def __init__(self, dataLines):

		self.dataLines = []

		if not checker.formatCheck(dataLines, len(self.columns)):
			print checker.formatErrorMessage	

		else:
			self.dataLines = dataLines



	# returns a dictionary with the columns of the given line
	def getColumns(self, line):

		columns = {}

		parts = line.split('\t')

		for i in range(len(self.columns)):
			columns[ self.columns[i] ] = parts[i]

		return columns



