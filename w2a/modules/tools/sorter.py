#  modules/harvester.py
#
#  Copyright 2012 Kid :">

from w2a.core.templates import Templates
from w2a.config import CONFIG
from w2a.lib.file import full_path, read_from_file, write_to_file, list_dir

class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		############################
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Sort data in file or directory'
		self.detailed_description	= 'This module retreives sort and remove duplicate lines'
		############################
		self.options.add_path('FILE', 'file to sort', False)
		self.options.add_path('DIRECTORY', 'dir to sort', default = CONFIG.TMP_PATH)
		############################

	def run(self, frmwk, args):
		listfile	= []
		listdir		= []
		if self.options['FILE']:
			listfile.append(full_path(self.options['FILE']))
		else:
			files	= list_dir(self.options['DIRECTORY'])
			if f in files:
				listfile.append(full_path(self.options['DIRECTORY'] + '/' + f))
		
		for f in listfile:
			frmwk.print_status('sorting : %s' % f)
			write_to_file(f,sorted(list(set(read_from_file(f)))))
