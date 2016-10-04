try:
	import formatChecker
except ImportError:
	print 'SizeCatalog -- (!) module do not found'	
	exit()


#
# SizeCatalog module
#
# helps to extract specific stats about a size catalog dataset
#


class SizeCatalog():


	#constructor 
	def __init__(self, dataLines):

		self.dataLines = []

		if not formatChecker.checkSizeCatalogFormat(dataLines):
			print '(!) please format these lines, and try again \n'		

		else:
			self.dataLines = dataLines
