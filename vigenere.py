"""
	DO NOT USE THIS EXCEPT FOR ACCESS TOKEN DUMPING,
	OR MAKE YOUR OWN TABLE FUNCTIONS
"""


def tableNum () :
	return [ chr ( i ) for i in range ( ord ( '0' ), 1 + ord ( '9' ) ) ] \
	     + [ chr ( i ) for i in range ( ord ( 'a' ), 1 + ord ( 'z' ) ) ]


def tableChr () :
	return { c : i for ( i, c ) in enumerate ( tableNum () ) }


def forward ( key, data ) :
	tn = tableNum ()
	tc = tableChr ()
	s = ''
	for i in range ( len ( data ) ) :
		k = ord ( key [ i % len ( key ) ] )
		s += tn [ ( tc [ data [ i ] ] + k + len ( tn ) ) % len ( tn ) ]
	return s


def backward ( key, data ) :
	tn = tableNum ()
	tc = tableChr ()
	s = ''
	for i in range ( len ( data ) ) :
		k = ord ( key [ i % len ( key ) ] )
		s += tn [ ( tc [ data [ i ] ] - k + len ( tn ) ) % len ( tn ) ]
	return s
