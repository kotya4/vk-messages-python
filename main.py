import sys
import msg2


if __name__ == "__main__" :
	if len ( sys.argv ) == 1 :
		print ( 'Usage:' )
		print ( '-l [username] -p [password]' )
		print ( '-t [token]' )
		print ( '-l [username] -p [password] OR -t [token] WITH -v [key]' )
		print ( '-v [key]' )
	else :
		username    = None
		password    = None
		token       = None
		vigenerekey = None
		for i in range ( ( len ( sys.argv ) - 1 ) >> 1 ) :
			key   = sys.argv [ 1 + ( i << 1 ) + 0 ]
			value = sys.argv [ 1 + ( i << 1 ) + 1 ]
			if   key == '-l' : username    = value
			elif key == '-p' : password    = value
			elif key == '-t' : token       = value
			elif key == '-v' : vigenerekey = value
		# err check
		if bool ( username ) ^ bool ( password ) :
			print ( 'You need to provide username AND password' )
			exit ( 1 )
		elif ( username or password ) and token :
			print ( 'You need to provide username and password OR token' )
			exit ( 1 )
		elif not ( username or password ) and not token and not vigenerekey :
			print ( 'You need to provide username and password OR token OR key' )
			exit ( 1 )
		# ok
		else :
			try :
				msg2.run ( username, password, token, vigenerekey )
			except KeyboardInterrupt :
				print ( 'Terminated on KeyboardInterrupt' )
			except ValueError as e :
				print ( 'Terminated on ValueError,', e )
				print ( 'Why?' )
				print ( 'Maybe "vk.parse" returned an empty list.' )
				print ( 'Maybe "print" cannot encode a character.' )
