#
# checker module
#
#
# - checks if a list of dataLines follows a specific format
#
# - checks if a list of dataLines is consistent with Brand.py, SizeType.py
#   or there new things that must be added  
#



try:
	from Brand import Brand
	from SizeType import SizeType
except ImportError:
	print 'consistencyChecker -- (!) module do not found'	
	exit()



formatErrorMessage = '(!) please format these lines, and try again \n'
newcomersWarningMessage = '(!) new things: '
extinctWarningMessage = '(!) extinct things: '


# checks if a list of dataLines follows a specific format
def formatCheck(dataLines, num_of_columns):

	ok = True

	for line in dataLines:

		# split line to columns using 'tab' 
		columns = line.split('\t')
		
		if len(columns) != num_of_columns:
			print 'please fix this line: ' + line + '  (!) number of columns:' + str(len(columns))
			ok = False

	return ok



# checks data consistency in a dataset
def checkDataset(dataset):

	ok = True

	checkBrands(dataset)
	checkSizeTypes(dataset)

	return ok


def checkBrands(dataset):

	extinct = [brand for brand in Brand.brandsUrls if brand not in dataset.brands()]
	newcomers = [newBrand for newBrand in dataset.brands() if newBrand not in Brand.brandsUrls]

	if len(extinct) > 0:
		print extinctWarningMessage + 'brands'
		print extinct
		print '\n\n'

	if len(newcomers) > 0:
		print newcomersWarningMessage + 'brands'
		print newcomers
		print '\n\n'


def checkSizeTypes(dataset):

	extinct = [sizeType for sizeType in SizeType.sizeTypes if sizeType not in dataset.size_types()]
	newcomers = [newSizeType for newSizeType in dataset.size_types() if newSizeType not in SizeType.sizeTypes]

	if len(extinct) > 0:
		print extinctWarningMessage + 'sizeTypes'
		print extinct
		print '\n\n'

	if len(newcomers) > 0:
		print newcomersWarningMessage + 'sizeTypes'
		print newcomers
		print '\n\n'





