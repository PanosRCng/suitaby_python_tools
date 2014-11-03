try:
	from FormatChecker import FormatChecker
except ImportError:
	print '(!) module do not found'	
	exit()


#
# Size Catalog module
#
# helps to extract specific stats about a size catalog dataset
#


class SizeCatalog():


	#constructor 
	def __init__(self, dataLines):

		self.sizeCatalogDataLines = []

		formatChecker = FormatChecker()

		if not formatChecker.checkSizeCatalogFormat(dataLines):
			print '(!) please format these lines, and try again \n'		

		else:
			self.sizeCatalogDataLines = dataLines
