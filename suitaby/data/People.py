try:
	from FormatChecker import FormatChecker
except ImportError:
	print '(!) module do not found'	
	exit()


#
# People module
#
# helps to extract specific stats about a people dataset
#


class People():

	#constructor 
	def __init__(self, dataLines):

		self.peopleDataLines = []

		formatChecker = FormatChecker()

		if not formatChecker.checkPeopleFormat(dataLines):
			print '(!) please format these lines, and try again \n'		

		else:
			self.peopleDataLines = dataLines

