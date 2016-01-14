# -*- coding: utf-8 -*-
class CONFIG():
	"""docstring for CONFIG"""
	
	_VERSION_		= '1.0.0'
	_NAME_			= 'w2a'
	ROOT_PATH			= 'w2a/'
	DEBUG_FLAG		= True
	TIME_OUT		= 30
	DB_ACCESS		= True
	PROXY			= None #'http://127.0.0.1:8080/'
	SOCKS			= None
#	SOCKS			= ['socks5', '209.222.3.117', 17566]
#	SOCKS			= ['socks5', '185.29.8.36', 5041]
#	SOCKS 			= ['socks5', '185.29.8.14', 5041]
#	SOCKS			= ['socks5', '127.0.0.1', 9150]
	DATA_PATH		= ROOT_PATH + 'data'
	MODULES_PATH	= ROOT_PATH + 'modules'
	TMP_PATH		= ROOT_PATH + 'output'
	FILE_PATH		= DATA_PATH + '/file'

	EXTENSION		= ["pdf", "txt", "doc", "docx", "xls", "xlsx", "ppt", "pptx" , "odp", "ods"]

	COLOR_STATUS	= '1;34m'
	COLOR_SUCCESS	= '1;32m'
	COLOR_ERROR		= '1;31m'
	COLOR_CMD		= '1;33m'

	GMAIL_ACCOUNT	= ['unknow.checker@gmail.com','checker.']

	IP_WHITE_LIST	= ['8.8.8.8']

	QUOTES = [	'I\'ll be back.',
				'Phac !'
			]
