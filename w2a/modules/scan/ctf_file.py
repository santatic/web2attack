#  modules/get_info.py
#
#  Copyright 2012 Kid :">

from w2a.core.templates import Templates
# from w2a.lib.net.http import HTTP
from w2a.config import CONFIG
from w2a.lib.file import full_path, read_from_file
from w2a.lib.thread import Thread

from copy import deepcopy
from re import search
from threading import Lock
class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Automatic check file exist'
		self.detailed_description	= 'This module retreives check file exist'
		
		self.options.add_string('URL', 'Path scan')
		self.options.add_string('EXTENSION', 'Extension of filescan(support : ext1,ext2...)', default = 'php')
		self.options.add_string('TYPE', 'Type of checker', default = 'location', complete = ['location', 'status', 'lenght', 'auto'])
		self.options.add_integer('THREADS', 'Multithreading', default = 10)
		self.options.add_boolean('STOP', 'Stop if found', default = False)
		self.options.add_path('DIRLIST', 'File containing directory list', False, default = CONFIG.DATA_PATH + '/dict/vuln.dir')
		self.options.add_path('FILELIST', 'File containing file list', default = CONFIG.DATA_PATH + '/dict/vuln.file')

		self.advanced_options.add_boolean('INTO', 'Continue scan file into dir if found status != 403', default = True)
		self.advanced_options.add_integer('OFFSET', 'Offset different of type lenght', default = 100)
		self.advanced_options.add_integer('TIMEOUT', 'Time out request', default = CONFIG.TIME_OUT)
		self.advanced_options.add_string('COOKIE', 'Cookie', False)
	
	def run(self, frmwk, args):
		self.frmwk		= frmwk
		self.dirs		= read_from_file(full_path(self.options['DIRLIST'])) if self.options['DIRLIST'] else []
		self.files		= read_from_file(full_path(self.options['FILELIST'])) if self.options['FILELIST'] else []
		self.url		= self.options['URL'] if self.options['URL'].endswith('/') else self.options['URL'] + '/'
		self.type		= self.options['TYPE']
		self.thread		= self.options['THREADS']
		self.stop		= self.options['STOP']
		self.extension 	= self.options['EXTENSION'].split(',')
		self.timeout	= self.advanced_options['TIMEOUT']
		self.into		= self.advanced_options['INTO']

		self.victim		= HTTP(self.url, timeout = self.timeout)
		self.victim.headers.update({'Cookie': self.advanced_options['COOKIE']} if self.advanced_options['COOKIE'] else {})
		
		self.success		= []
		self.tmp_dirs		= self.dirs + []
		self.current_dir	= ''
		self.locker			= Lock()

		if self.type in ['lenght', 'auto']:
			victim				= deepcopy(self.victim)
			victim.redirect		= False
			self.frmwk.print_status('Init not found infomation')
			victim.Request(self.url + 'ASDASdadhkjlhjfasdfawefa/', 'GET')

			if self.type == 'auto':
				# if victim.response.status == 404:
				# 	self.type	= 'status'
				# 	self.frmwk.print_success('auto get type: error')
				# el
				if victim.response.status == 200:
					self.type	= 'lenght'
					self.frmwk.print_success('auto get type: lenght')
				else:
					self.type				= 'location'
					self.frmwk.print_success('auto get type: location')

			if self.type == 'lenght':
				self.notfounddir	= len(victim.result)
			if self.type in ['lenght', 'location']:
				self.notfoundfile	= len(victim.Request(self.url + 'adfasdaszxcvzdczxfasASasda.' + self.extension[0], 'GET'))
				self.offset			= self.advanced_options['OFFSET']
			del victim

		if self.type == 'location':
			self.victim.redirect	= False

		self.frmwk.print_status('Starting scanner')
		########check file in current path######
		try:
			if self.url.endswith('/'):
				self.url	= self.url[:-1]
			self.filechecker(self.url)
			if not self.url.endswith('/'):
				self.url	= self.url + '/'
			########################################
			threads	= []
			for i in range(self.thread):
				t	= Thread(target = self.worker)
				threads.append(t)
				t.start()
			for t in threads:
				t.join()
		except KeyboardInterrupt:
			for t in threads:
				if t.isAlive():
					t.terminate()
			pass
		if len(self.success) > 0:
			self.frmwk.print_success('Found list:\n-----------')
			for link in self.success:
				self.frmwk.print_success(link)
		else:
			self.frmwk.print_error('---------\nNot Found!\n---------')
	def worker(self):
		victim		= deepcopy(self.victim)
		while len(self.tmp_dirs) > 0:
			if self.stop and len(self.success) > 0:
				return
			try:
				self.locker.acquire()
				self.current_dir	= self.tmp_dirs.pop(0)
				dirpath	= self.url + self.current_dir
				self.locker.release()
			except IndexError:
				pass
				return

			if self.checker(victim, dirpath, 'dir'):
				self.locker.acquire()
				self.success.append('DIR:  ' + dirpath)
				self.frmwk.print_success('FOUND DIR: %s' % dirpath)
				if self.type == 'location': # location status move page,redirect to check
					victim.redirect = True
					self.checker(victim, dirpath, 'dir')
					victim.redirect = False
				if victim.response.status == 403 or self.into:
					self.filechecker(dirpath)
				self.locker.release()
				if self.stop:
					return
			else:
				self.frmwk.print_error('NOT FOUND: %s' % dirpath)

	def filechecker(self, dirpath):
		self.tmp_files	= self.files + []
		threads	= []
		for i in range(self.thread):
			t	= Thread(target = self.checkfile, args = (dirpath,))
			threads.append(t)
			t.start()
		try:
			for t in threads:
				t.join()
		except KeyboardInterrupt:
			for t in threads:
				if t.isAlive():
					t.terminate()
			pass

	def checkfile(self, dirpath):
		victim			= deepcopy(self.victim)
		if self.type == 'location':
			victim.redirect	= True
		while len(self.tmp_files) > 0:
			for ext in self.extension:
				if len(self.tmp_files) == 0:
					return
				filepath	= dirpath + '/' + self.tmp_files.pop(0).format(ext = ext)
				if self.checker(victim, filepath):
					self.success.append('FILE: ' + filepath)
					self.frmwk.print_success('FOUND FILE: %s' % filepath)
					if self.stop:
						self.tmp_files	= []
						return
				else:
					self.frmwk.print_error('NOT FOUND: %s' % filepath)

	def checker(self, victim, path, check = 'file'):
		method = 'GET' if self.type == 'lenght' else 'HEAD'
		victim.Request(path, method)

		if self.type == 'location':
			if check == 'dir':
				if victim.response.getheader('location') and victim.response.getheader('location').strip().endswith('/'):
					return True
				return False
			else:
				if victim.response.status == 404:
					return False
				else:
					return True
		elif self.type == 'status':
			if victim.response.status == 404:
				return False
			else:
				return True
		elif self.type == 'lenght':
			lenght	= self.notfounddir if check == 'dir' else self.notfoundfile
			if abs(len(victim.result) - lenght) < self.offset:
				return True
			else:
				return False
