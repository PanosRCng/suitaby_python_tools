try:
	import sys

	from suitaby.data import io
	from suitaby.data.Dataset import Dataset
except ImportError:
	print 'main -- (!) module do not found '	
	exit()


def main():

	inSizesFile = "sizes.txt"
	newSizesFile = "new_sizes.txt"



	# load file as list of string datalines
	sizesDataLines = io.ReadFile(inSizesFile)

	# do a consistency check
	dataset = Dataset( sizesDataLines )


	new_columns = [
		   'size_type',
		   'size',
		   'label',
          	   'brand',
		   'url',
		   'clothe_category',
		   'size_category',
		   'gender'
		   ]

	new_lines = []

	for line in dataset.dataLines:
		
		columns = dataset.getColumns(line)

		columns['gender'] = 'M'

		new_line = ""

		for i in range(len(new_columns)):
			new_line += columns[ new_columns[i] ] + '\t'

		new_lines.append( new_line[:-1] )


	io.WriteHeader(newSizesFile, new_columns)
	io.WriteFile(newSizesFile, new_lines, 'a')
	

	
	print 'all ok'


if __name__ == "__main__":
	main()
