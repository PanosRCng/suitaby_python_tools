
#
# formatChecker module
#
# checks if a list of dataLines follows a specific format
#

errorMessage = '(!) please format these lines, and try again \n'

# checks if sizes data lines are formatted well
def checkSizeFormat(dataLines):

	ok = True

	for line in dataLines:

		# split line to columns using 'tab' 
		columns = line.split('\t')
		
		if len(columns) != 7:
			print 'please fix this line: ' + line + '  (!) length:' + str(len(columns))
			ok = False

	return ok	


# checks if size catalog data lines are formatted well
def checkSizeCatalogFormat(dataLines):

	ok = True

	for line in dataLines:

		# split line to columns using 'tab' 
		columns = line.split('\t')
		
		if len(columns) != 6:
			print 'please fix this line: ' + line + '  (!) length:' + str(len(columns))
			ok = False

	return ok


# checks if people data lines are formatted well
def checkPeopleFormat(dataLines):

	ok = True

	for line in dataLines:

		# split line to columns using 'tab' 
		columns = line.split('\t')
		
		if len(columns) != 16:
			print 'please fix this line: ' + line + '  (!) length:' + str(len(columns))
			ok = False

	return ok


