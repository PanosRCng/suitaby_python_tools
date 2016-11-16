#try:
#	
#except ImportError:
#	print 'SizeType -- (!) module do not found'	
#	exit()


#
# SizeType class
#
#

class SizeType:

	sizeTypes = [
			'LOWER_WAIST',
			'INSIDE_LEG',
			'WAIST',
			'BACK_LENGTH',
			'FRONT_RISE',
			'SHOULDER_WIDTH',
			'HEIGHT',
			'CHEST',
			'THIGH',
			'SLEEVE_LENGTH',
			'SLEEVE_LENGTH_LONG',
			'HALF_CHEST',
			'FOOT_LENGTH',
			'HIPS',
			'NECK'
		     ]


	mergedSizeTypes = {
				'HIP' : 'HIPS',
				'SLEEVE' : 'SLEEVE_LENGTH',
				'BACK' : 'BACK_LENGTH'
			  }	



