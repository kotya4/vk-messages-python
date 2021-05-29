from vk.defaults import *


def params ( p ) :
	return '&'.join ( [ '{}={}'.format ( key, p [ key ] ) for key in p ] )


def oauth ( username, password ) :
	return 'https://oauth.vk.com/token?' + params ( {
		'grant_type'    : 'password',
		'username'      : username,
		'password'      : password,
		'v'             : DEFAULT_V,
		'scope'         : DEFAULT_SCOPE,
		'client_id'     : DEFAULT_CLIENT_ID,
		'client_secret' : DEFAULT_CLIENT_SECRET,
	} )


def method ( token, name, args ) :
	return 'https://api.vk.com/method/' + name \
		+ '?' + params ( args )                \
		+ '&access_token=' + token             \
		+ '&v=' + DEFAULT_V


def longpoll ( server, key, ts ) :
	return 'https://{}?act=a_check&key={}&ts={}&wait=25&mode={}&version={}'.format \
		( server, key, ts, DEFAULT_LONGPOLL_MODE, DEFAULT_LONGPOLL_VERSION )
