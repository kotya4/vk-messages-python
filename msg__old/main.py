import sys
import msg


if __name__ == "__main__" :
	if len ( sys.argv ) == 1 :
		# Program runs w\o arguments and
		# I'll show help message.
		print ( 'Hi there! To use this program you must provide some arguments.' )
		print ( 'First of all, you can type your actual login and password and ' )
		print ( 'I`ll try to get access token by myself.                       ' )
		print ( 'To do this set your login with key "-l" and password with key ' )
		print ( '"-p".                                                         ' )
		print ()
		print ( 'Or you can use your own access token setting it with key "-t".' )
		print ( 'If you want me to remember access token, I`ll put it in the   ' )
		print ( 'file next to me naming it "token", but I must ask you help me:' )
		print ()
		print ( 'So, you need to come up with a PASSWORD wich I`ll use to      ' )
		print ( 'encrypt your token with Vigenere cipher. This is NOT the      ' )
		print ( 'symmetric encryption or smth, so be careful                   ' )
		print ( 'with that file, do not store it anythere except your computer!' )
		print ( 'I only need it because I do not want to store your token as   ' )
		print ( 'raw text wich any human can read. I recomend you not to       ' )
		print ( 'store access token at all, but for convinience I cannot       ' )
		print ( 'forbid you from doing this. So, to save your token provide    ' )
		print ( 'your PASSWORD with key "-s". To use stored token just run this' )
		print ( 'program with key "-k". To print fast manual type "-h".        ' )
	elif len ( sys.argv ) == 2 and sys.argv [ 1 ] == '-h' :
		print ( 'Usage:' )
		print ( '-l [login] -p [password]' )
		print ( '-t [token]' )
		print ( '-l [login] -p [password] OR -t [token] WITH -s [vigenere key]' )
		print ( '-k [vigenere key]' )
		print ( '-h' )
	else :
		login         = None
		password      = None
		token         = None
		vigenere_save = None
		vigenere_load = None
		for i in range ( ( len ( sys.argv ) - 1 ) >> 1 ) :
			key   = sys.argv [ 1 + ( i << 1 ) + 0 ]
			value = sys.argv [ 1 + ( i << 1 ) + 1 ]
			if   key == '-l' : login         = value
			elif key == '-p' : password      = value
			elif key == '-t' : token         = value
			elif key == '-s' : vigenere_save = value
			elif key == '-k' : vigenere_load = value
		msg.run ( login, password, token, vigenere_save, vigenere_load )
