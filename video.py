import vk.vk as vk
import vk.url as url
import requests



def run ( username, password, token, vigenerekey ) :

	# take token from oauth
	if username and password :
		( token, ) = vk.parse ( vk.get ( url.oauth ( username, password ) ), [ 'access_token' ] )

	# save token to file
	if token and vigenerekey :
		with open ( 'token', 'w' ) as f :
			encoded = vigenere.forward ( vigenerekey, token )
			f.write ( encoded )

	# load token from file
	if not token and vigenerekey :
		try:
			with open ( 'token', 'r' ) as f :
				encoded = f.read ()
				token = vigenere.backward ( vigenerekey, encoded )
		except FileNotFoundError :
			vk.error ( 'FileNotFoundError raised, no token vigenered yet' )

	# still have no token
	if not token:
		vk.error ( 'Still have no token, terminating self :(' )
		exit ( 2 )

	# ok
	vk.debug ( 'Token', token )

	( response ) = vk.parse ( vk.get ( url.method ( token, 'video.get', {
		"videos" : "231061039_456240524"
	} ) ), [ 'response' ] )






# run ( '89196442026', 'nastyarizhik2', None, None )



r = requests.get ( 'https://vk.com/video_ext.php?oid=231061039&id=456240524&hash=d75c52dc819b1ce4&__ref=vk.windows&api_hash=1620474238790e1fa9eec248fdbb_GE4TMNRXGAZDIOA', headers=vk.DEFAULT_HEADERS )

with open ( 'outp.txt', mode='w', encoding="utf-8" ) as f:
	f.write(r.text)

# print (r.text)