try:
	import os
except ImportError:
	print 'io -- (!) module do not found'	
	exit()


#
# io module
#
# by default reads and writes data in the './data' folder
#


# open file, read it as lines to memory, close file, return a list with the lines
def ReadFile(fileName):

	fullName = os.path.join('./data', fileName)

	f = open(fullName, 'rU')
	lines = f.readlines()
	f.close()

	# create an empty list to save the dataLines
	dataLines = []

	for line in lines:

		if line != '\n':
			# if line is a data line - does not start with '#'
			if( line[0] != '#' ):

				dataLines.append( line.replace('\n', '') )			

	if len(dataLines) == 0:
		print 'io -- (!) the file is empty, no lines found in'
	
	return dataLines


# open file, write the list with the lines, close file
def WriteFile(filename, lines, flag):

	if len(lines)<0:
		print 'io -- (!) no data to write'
		return

	fullname = os.path.join('./data', filename)

	f = open(fullname, flag)

	for line in lines:
		f.write(line)
		f.write('\n')

	f.close


# write the sizes catalog header
def WriteSizeCatalogHeader(filename):

	fullname = os.path.join('./data', filename)

	f = open(fullname, 'w')
	f.write('#clothe_category	label	size_category	size_type_projections	brand	url\n'+'#\n')
	f.close


# write the sizes header
def WriteSizesHeader(filename):

	fullname = os.path.join('./data', filename)

	f = open(fullname, 'w')
	f.write('#size_type	size	label	brand	url	clothe_category	size_category\n'+'#\n')
	f.close


# just write the people header
def WritePeopleHeader(filename, sizeTypesList):

	fullname = os.path.join('./data', filename)

	line = "#people_id"

	for sizeType in sizeTypesList:

		line += '\t' + sizeType

	line += '\n#\n'

	f = open(fullname, 'w')
	f.write(line)
	f.close


