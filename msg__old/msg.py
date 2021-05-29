import requests
import json
import time


SCOPE_MESSAGES = 4096

DEFAULT_V = '5.130'

DEFAULT_SCOPE = 0 | SCOPE_MESSAGES

# Offitial windows app credentials from
# https://github.com/negezor/vk-io/blob/master/packages/authorization/src/constants.ts

DEFAULT_CLIENT_ID = '3697615'

DEFAULT_CLIENT_SECRET = 'AlVXZFMUqyrnABp8ncuU'

DEFAULT_HEADERS = {
	# Firefox browser
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
}

DEFAULT_LONGPOLL_VERSION = 3

DEFAULT_LONGPOLL_MODE = 0

DEFAULT_LONGPOLL_DELAY_SECS = 5

DEFAULT_WAIT_BEFORE_RECONNECT = 30

DEFAULT_RECONNECT_TRIES = 3


def URLParams ( params ) :
	return '&'.join ( [ '{}={}'.format ( key, params [ key ] ) for key in params ] )


def URLOauth ( username, password ) :
	return 'https://oauth.vk.com/token?' + URLParams ( {
		'grant_type'    : 'password',
		'username'      : username,
		'password'      : password,
		'v'             : DEFAULT_V,
		'scope'         : DEFAULT_SCOPE,
		'client_id'     : DEFAULT_CLIENT_ID,
		'client_secret' : DEFAULT_CLIENT_SECRET,
	} )


def URLMethod ( method, params, token ) :
	return 'https://api.vk.com/method/' + method \
		+ '?' + URLParams ( params )             \
		+ '&access_token=' + token               \
		+ '&v=' + DEFAULT_V


def URLLongPoll ( server, key, ts ) :
	return 'https://{}?act=a_check&key={}&ts={}&wait=25&mode={}&version={}'.format \
		( server, key, ts, DEFAULT_LONGPOLL_MODE, DEFAULT_LONGPOLL_VERSION )


def get ( url ) :
	return requests.get ( url, headers=DEFAULT_HEADERS )


def parseLongPoll ( update ) :
	# Добавление нового сообщения.
	if update [0] == 4 :
		message_id   = update [1]
		flags        = update [2]
		minor_id     = update [3]
		extra_fields = update [4]
		print ( 'KTO TO NAPISAL SOOBCHENIE', message_id )


def withReconnect ( f ) :
	tries = 0
	while True :
		try:
			return f ()
		except requests.exceptions.ConnectionError as e:
			print ( 'ConnectionError raised' )
			if DEFAULT_RECONNECT_TRIES >= 0 and tries > DEFAULT_RECONNECT_TRIES :
				print ( 'Max reconnection tries', tries )
				raise e
			time.sleep ( DEFAULT_WAIT_BEFORE_RECONNECT )
			tries += 1


def run ( login=None, password=None, token=None, vigenere_save=None, vigenere_load=None ) :

	try:

		response = None

		if vigenere_load :
			# load token from file
			pass

		elif login and password :
			# load token from oauth
			def fromOAuth () :
				url = URLOauth ( login, password )
				print ( 'GET : ' + url )
				response = requests.get ( url, headers=DEFAULT_HEADERS )
				r = json.loads ( response.text )
				print ( 'ANSWER : ', json.dumps ( r, indent=2, sort_keys=True ) )
				return r [ 'access_token' ]
			token = withReconnect ( fromOAuth )

		if vigenere_save :
			# save token to file
			pass

		# get longpoll

		def getLongPoll () :
			url = URLMethod ( 'messages.getLongPollServer', {
				'need_pts'   : 0,
				'lp_version' : DEFAULT_LONGPOLL_VERSION,
			}, token )
			print ( 'GET : ' + url )
			response = requests.get ( url, headers=DEFAULT_HEADERS )
			r = json.loads ( response.text )
			print ( 'ANSWER : ', json.dumps ( r, indent=2, sort_keys=True ) )
			return (
				r [ 'response' ][ 'server' ],
				r [ 'response' ][ 'key' ],
				r [ 'response' ][ 'ts' ]
			)
		( server, key, ts ) = withReconnect ( getLongPoll )

		# listen longpoll

		def listenLongPoll () :
			url = URLLongPoll ( server, key, ts )
			print ( 'GET : ' + url )
			response = requests.get ( url, headers=DEFAULT_HEADERS )
			r = json.loads ( response.text )
			print ( 'ANSWER : ', json.dumps ( r, indent=2, sort_keys=True ) )
			return (
				r [ 'updates' ],
				r [ 'ts' ]
			)

		while ( True ) :
			( updates, ts ) = withReconnect ( listenLongPoll )

			for update in updates :
				parseLongPoll ( update )

			time.sleep ( DEFAULT_LONGPOLL_DELAY_SECS )

		# done

		print ( 'Ok.' )

	except ValueError :

		with open ( 'response.txt', 'w', encoding='utf-8' ) as f :

			f.write ( response.text )

		print ( 'ValueError raised, response text saved in "response.txt"' )
