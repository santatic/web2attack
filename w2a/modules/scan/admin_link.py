#  modules/get_info.py
#
#  Copyright 2012 Kid :">

from w2a.core.templates import Templates
from w2a.config import CONFIG

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
		self.options.add_boolean('STOP', 'Stop if found', default = True)
		self.options.add_path('DIRLIST', 'File containing directory list', False,default = CONFIG.DATA_PATH + '/dict/admin.dir')
		self.options.add_path('FILELIST', 'File containing file list', default = CONFIG.DATA_PATH + '/dict/admin.file')

		self.advanced_options.add_boolean('INTO', 'Continue scan file into dir if found status != 403', default = False)
		self.advanced_options.add_integer('OFFSET', 'Offset different of type lenght', default = 100)
		self.advanced_options.add_integer('TIMEOUT', 'Time out request', default = CONFIG.TIME_OUT)
		self.advanced_options.add_string('COOKIE', 'Cookie', False)
	
	def run(self, frmwk, args):
		module_name	= 'scan/vuln_file'
		scanner		= frmwk.modules[module_name]
		scanner.options.add_string('URL', 'Path ', default = self.options['URL'])
		scanner.options.add_string('EXTENSION', 'Extension', default = self.options['EXTENSION'])
		scanner.options.add_string('TYPE', 'Type of checker', default = self.options['TYPE'])
		scanner.options.add_integer('THREADS', 'Multithreading', default = self.options['THREADS'])
		scanner.options.add_boolean('STOP', 'Stop if found', default = self.options['STOP'])
		scanner.options.add_path('DIRLIST', 'directory list', default = self.options['DIRLIST'])
		scanner.options.add_path('FILELIST', 'file list', default = self.options['FILELIST'])
		scanner.advanced_options.add_boolean('INTO', 'scan into', default = self.advanced_options['INTO'])
		scanner.advanced_options.add_integer('OFFSET', 'Offset', default = self.advanced_options['OFFSET'])
		scanner.advanced_options.add_integer('TIMEOUT', 'Time out', default = self.advanced_options['TIMEOUT'])
		scanner.advanced_options.add_string('COOKIE', 'Cookie', default = self.advanced_options['COOKIE'])
		scanner.run(frmwk, None)
		frmwk.reload_module(module_name)