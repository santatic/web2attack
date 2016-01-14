# -*- coding: utf-8 -*-
import socket
from w2a.lib.net import socks
from w2a.config import CONFIG
from .core.printer import print_error

if CONFIG.SOCKS != None:
	if CONFIG.SOCKS[0] == 'socks5':
		stype	= socks.PROXY_TYPE_SOCKS5
	elif CONFIG.SOCKS[0] == 'socks4':
		stype	= socks.PROXY_TYPE_SOCKS4
	elif CONFIG.SOCKS[0] == 'http':
		stype	= socks.PROXY_TYPE_HTTP
	else:
		print_error('Unknown Proxy Type')
		stype	= None
	if stype:
		socks.setdefaultproxy(stype, CONFIG.SOCKS[1], CONFIG.SOCKS[2])
		socket.socket 	= socks.socksocket