import requests
import json
import time
from vk.defaults import *


Debug = '\nYielded debug messages:\n'


def stringify ( v ) :
	return ' '.join ( str ( s ) for s in v )


def debug ( *v ) :
	if DEFAULT_DEBUG :
		print ( *v )
	else :
		global Debug
		Debug += '\n' + stringify ( v )


def error ( *v ) :
	if DEFAULT_ERROR :
		if not DEFAULT_DEBUG :
			global Debug
			print ( Debug )
			Debug = '\nYielded debug messages:\n'
			print ( '\nNow error message:\n' )
		print ( *v )


def get ( url ) :
	debug ( 'Get', url )
	for i in range ( DEFAULT_RECONNECT_TRIES + 1 ) :
		try :
			return requests.get ( url, headers=DEFAULT_HEADERS )
		except requests.exceptions.ConnectionError :
			debug ( 'ConnectionError raised, tries left', DEFAULT_RECONNECT_TRIES - i )
			time.sleep ( DEFAULT_WAIT_BEFORE_RECONNECT )
	error ( 'Max reconnection tries' )
	return None


def destruct ( result, fields ) :
	values = []
	for keys in fields :
		value = result
		for key in keys :
			try :
				value = value [ key ]
			except KeyError as e :
				debug ( 'KeyError raised on destruct, missing', str ( e ) )
				# TODO: mate default value for inconsistent keys,
				#       do not debug them.
				value = None
				break
		values += [ value ]
	return values


def parse ( response, *fields ) :
	try :
		result = json.loads ( response.text )
		dump = json.dumps ( result, indent=2, sort_keys=True )
		if len ( dump ) > DEFAULT_DEBUG_DUMP_LEN :
			dump = dump [ :DEFAULT_DEBUG_DUMP_LEN ] + ' ...'
		debug ( 'Response', dump )
		return destruct ( result, fields )
	except ValueError :
		error ( 'ValueError raised, response saved in "response.txt"' )
		with open ( 'response.txt', 'w', encoding='utf-8' ) as f :
			f.write ( response.text )
	except AttributeError as e :
		error ( 'AttributeError raised on parse', str ( e ) )
	return []


