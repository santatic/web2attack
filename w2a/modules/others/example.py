#  modules/get_info.py
#
#  Copyright 2012 Kid :">

from w2a.core.templates import Templates

from socket import gethostbyname

class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Get Basic Meter Information By Reading Tables'
		self.detailed_description	= 'This module retreives some basic meter information and displays it in a human-readable way.'
		
		self.options.addString('HOST', 'domain/ip')

	def run(self, frmwk, args):
		print(gethostbyname(self.options['HOST']))
