import winsound
import time
import datetime
import vk.vk as vk
import vk.url as url
import vigenere


def timestampToReadable ( ts ) :
	return datetime.datetime.fromtimestamp( int ( ts ) ).strftime ( '%H:%M:%S' )


def astral ( s ) :
	""" Converts all wierd unicode to hex """
	s = list ( s )
	for i in range ( len ( s ) ) :
		c = ord ( s [ i ] )
		# Miscellaneous Symbols Block from U+2600 to U+26FF
		if c > 0xFFFF or 0x2600 <= c and c <= 0x26FF :
			s [ i ] = '[U+{:X}]'.format ( c )
	return ''.join ( s )


def encodeMessage ( text ) :
	return astral ( str ( text ) ) if text else ''


def parseAttachment ( a ) :
	type = a [ 'type' ]
	if type == 'photo' :
		sizes = a [ 'photo' ] [ 'sizes' ]
		url   = sizes [ -1 ] [ 'url' ]
		return '[{}]'.format ( type )
	elif type == 'video' :
		title         = a [ 'video' ] [ 'title' ]
		image         = a [ 'video' ] [ 'image' ]
		firstFrame    = a [ 'video' ] [ 'first_frame' ]
		firstFrameUrl = firstFrame [ -1 ] [ 'url' ]
		return '[{} {}]'.format ( type, title )
	elif type == 'doc' :
		title = a [ 'doc' ] [ 'title' ]
		url   = a [ 'doc' ] [ 'url' ]
		return '[{} {}]'.format ( type, title )
	elif type == 'audio' :
		title  = a [ 'audio' ] [ 'title' ]
		artist = a [ 'audio' ] [ 'artist' ]
		url    = a [ 'audio' ] [ 'url' ]
		return '[{} {} - {}]'.format ( type, artist, title )
	else :
		return '[{}]'.format ( type )


def parse ( update ) :
	# message was recieved
	if update [0] == 4 :
		messageId  = update [ 1 ]
		flags      = update [ 2 ]
		peerId     = update [ 3 ]
		timestamp  = update [ 4 ]
		text       = update [ 5 ]
		isOutbox   = bool ( int ( flags ) & 2 )
		if not isOutbox :
			print ( 'MSG @ {} FROM {} >\n\r\t{}'.format (
				timestampToReadable ( timestamp ),
				peerId,
				encodeMessage ( text ),
			) )
			winsound.PlaySound ( 'poop.wav', winsound.SND_FILENAME )


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


	# take longpoll
	( server, key, ts, pts ) = vk.parse ( vk.get ( url.method ( token, 'messages.getLongPollServer', {
		'need_pts'   : 1,
		'lp_version' : vk.DEFAULT_LONGPOLL_VERSION,
	} ) ), [ 'response', 'server' ], [ 'response', 'key' ], [ 'response', 'ts' ], [ 'response', 'pts' ] )

	# ok
	vk.debug ( 'LongPoll', server, key, ts, pts )


	# take conversations
	( count, items, unreadCount ) = vk.parse ( vk.get ( url.method ( token, 'messages.getConversations', {

	} ) ), [ 'response', 'count' ], [ 'response', 'items' ], [ 'response', 'unread_count' ] )

	# ok
	vk.debug ( 'Conversations', count, unreadCount )

	# "unreadCount" can be None i.e. response.unread_count does not exist

	# print unread

	print ( 'YOU HAVE {} CONVERSATIONS, {} OF THEM UNREAD'.format (
		count,
		unreadCount,
	) )

	for item in items :
		if not 'unread_count' in item [ 'conversation' ] :
			continue
		if not item [ 'conversation' ] [ 'unread_count' ] > 0 :
			continue

		unread = item [ 'conversation' ] [ 'unread_count' ]
		peerId = item [ 'conversation' ] [ 'peer' ] [ 'id' ]

		print ( '\t{} MESSAGES FROM {}'.format (
			unread,
			peerId,
		) )

		# take history of that conversation
		( historyCount, historyItems ) = vk.parse ( vk.get ( url.method ( token, 'messages.getHistory', {
			'peer_id' : peerId,
			'count'   : unread,
		} ) ), [ 'response', 'count' ], [ 'response', 'items' ] )

		for item in reversed ( historyItems ) :

			date        = item [ 'date' ]
			text        = item [ 'text' ]
			attachments = item [ 'attachments' ]

			print ( '\t\t@ {} >\t{}'.format (
				timestampToReadable ( date ),
				encodeMessage ( text ) + ' '.join ( [ parseAttachment ( a ) for a in attachments ] ),
			) )

	print ( 'Listening for updates ...' )

	while True :

		# listen longpoll
		( updates, ts ) = vk.parse ( vk.get ( url.longpoll ( server, key, ts ) ), [ 'updates' ], [ 'ts' ] )

		if updates == None :
			vk.error ( 'update is not iterable, maybe keyerror raised' )
			exit ()


		# parse updates
		for u in updates :
			parse ( u )

		# sleep
		time.sleep ( vk.DEFAULT_LONGPOLL_DELAY_SECS )
