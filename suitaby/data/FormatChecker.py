

#
# FormatChecker module
#
# checks if a dataFile follows a specific format
#

class FormatChecker():


	#constructor
	def __init__(self):

		pass


	# checks if sizes data lines are formatted well
	def checkSizeFormat(self, dataLines):

		ok = True

		for line in dataLines:

			# split line to columns using 'tab' 
			columns = line.split('\t')
		
			if len(columns) != 7:
				print 'please fix this line: ' + line + '  (!) length:' + str(len(columns))
				ok = False

		return ok	


	# checks if size catalog data lines are formatted well
	def checkSizeCatalogFormat(self, dataLines):

		ok = True

		for line in dataLines:

			# split line to columns using 'tab' 
			columns = line.split('\t')
		
			if len(columns) != 6:
				print 'please fix this line: ' + line + '  (!) length:' + str(len(columns))
				ok = False

		return ok


	# checks if people data lines are formatted well
	def checkPeopleFormat(self, dataLines):

		ok = True

		for line in dataLines:

			# split line to columns using 'tab' 
			columns = line.split('\t')
		
			if len(columns) != 16:
				print 'please fix this line: ' + line + '  (!) length:' + str(len(columns))
				ok = False

		return ok


