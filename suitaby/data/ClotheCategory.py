#try:
#	
#except ImportError:
#	print 'ClotheCategory -- (!) module do not found'	
#	exit()


#
# ClotheCategory class
#
#

class ClotheCategory:
	
	parentClotheCategories = [
			    'KNITWEAR',
			    'UNDERWEAR',
			    'SHOES',
			    'JACKETS & COATS',
			    'ACCESSORIES',
			    'SUITS',
			    'T-SHIRTS',
		            'TROUSERS',
			    'APPAREL',
			    'SPORTSWEAR',
			    'SHIRTS'
			   ]
	
	clotheCategories = [    'POLOS', 
				'SPORT SHIRTS',
				'SUITS', 
				'COATS',
				'POLO',
				'TAILORED JACKETS',
				'SPORTSWEAR',
				"MEN'S SHORTS",
				'PULLOVERS',
				"MEN'S TOPS",
				'SHEP SHIRTS',
				'SUIT',
				'SHIRT',
				'BUSINESS SUITS',
				'SHORTS',
				'BOXERS',
				"MEN'S BOTTOMS",
				'TEES',
				'PANTS',
				'FLEECE',
				'CHINOS',
				'SWIMWEAR',
				'SOCKS',
				'BLAZERS',
				'JACKETS',
				'TOPS',
				'TRACK PANTS',
				'SHIRTS',
				'APPAREL',
				'MERINO',
				'CASUAL',
				'APPAREL (POLO)',
				'DRESS SHIRTS',
				'CARDIGANS',
				'OUTERWEAR',
				'SWEATSHIRTS',
				'SUITS TROUSERS',
				'T-SHIRTS',
				'SWEATERS',
				'JUMPERS',
				'KNITWEAR',
				'UNDERWEAR',
				'RUGBY',
				'BUSINESS SHIRTS',
				'BELTS',
				'ELASTICATED WAIST TROUSERS',
				'TROUSERS',
				'RUGBYS',
				'SHOES',
				'DENIM',
				'JEANS',
				"MEN'S PANTS",
				'BOTTOMS'	]


	# inverted index of clothe category to parent categories list
	invertedIndex = { 
					"POLOS" : ["T-SHIRTS"],
					"RUGBYS" : ["T-SHIRTS"],
					"TOPS" : ["T-SHIRTS"],
					"POLO" : ["T-SHIRTS"],
					"SWEATSHIRTS" : ["T-SHIRTS"],
					"T-SHIRTS" : ["T-SHIRTS"],
					"RUGBY" : ["T-SHIRTS"],
					"MEN'S TOPS" : ["T-SHIRTS", "JACKETS & COATS", "SHIRTS", "KNITWEAR"],
					"SHEP SHIRTS" : ["T-SHIRTS"],
					"TEES" : ["T-SHIRTS"],
					"BUSINESS SUITS" : ["SUITS"],
					"SUITS TROUSERS" : ["SUITS"],
					"SUIT" : ["SUITS"],
					"SUITS" : ["SUITS"],
					"TAILORED JACKETS"  : ["SUITS"],
					"COATS" : ["JACKETS & COATS"],
					"OUTERWEAR" : ["JACKETS & COATS"],
					"BLAZERS" : ["JACKETS & COATS"],
					"JACKETS" : ["JACKETS & COATS"],
					"SPORTSWEAR" : ["SPORTSWEAR"],
					"ELASTICATED WAIST TROUSERS" : ["SPORTSWEAR"],
					"SPORT SHIRTS" : ["SPORTSWEAR"],
					"SWIMWEAR" : ["SPORTSWEAR"],
					"TRACK PANTS" : ["SPORTSWEAR"],
					"SHIRTS" : ["SHIRTS"],
					"BUSINESS SHIRTS" : ["SHIRTS"],
					"CASUAL" : ["SHIRTS"],
					"SHIRT" : ["SHIRTS"],
					"DRESS SHIRTS" : ["SHIRTS"],
					"APPAREL (POLO)" : ["APPAREL"],
					"APPAREL" : ["APPAREL"],
					"MERINO" : ["KNITWEAR"],
					"CARDIGANS" : ["KNITWEAR"],
					"PULLOVERS" : ["KNITWEAR"],
					"JUMPERS" : ["KNITWEAR"],
					"KNITWEAR" : ["KNITWEAR"],
					"FLEECE" : ["KNITWEAR"],
					"SWEATERS" : ["KNITWEAR"],
					"BOTTOMS" : ["TROUSERS"],
					"SHORTS" : ["TROUSERS"],
					"MEN'S SHORTS" : ["TROUSERS"],
					"MEN'S BOTTOMS" : ["TROUSERS"],
					"PANTS" : ["TROUSERS"],
					"MEN'S PANTS" : ["TROUSERS"],
					"CHINOS" : ["TROUSERS"],
					"DENIM" : ["TROUSERS"],
					"JEANS" : ["TROUSERS"],
					"TROUSERS" : ["TROUSERS"],
					"BELTS" : ["ACCESSORIES"],
					"SOCKS" : ["ACCESSORIES"],
					"UNDERWEAR" : ["UNDERWEAR"],
					"BOXERS" : ["UNDERWEAR"],
					"SHOES" : ["SHOES"]
				      }



