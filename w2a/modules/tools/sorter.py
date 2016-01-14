#  modules/harvester.py
#
#  Copyright 2012 Kid :">

from w2a.core.templates import Templates
from w2a.config import CONFIG
from w2a.lib.file import FullPath, ReadFromFile, WriteToFile, ListDir

class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		############################
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Sort data in file or directory'
		self.detailed_description	= 'This module retreives sort and remove duplicate lines'
		############################
		self.options.addPath('FILE', 'file to sort', False)
		self.options.addPath('DIRECTORY', 'dir to sort', default = CONFIG.TMP_PATH)
		############################

	def run(self, frmwk, args):
		listfile	= []
		listdir		= []
		if self.options['FILE']:
			listfile.append(FullPath(self.options['FILE']))
		else:
			files	= ListDir(self.options['DIRECTORY'])
			if f in files:
				listfile.append(FullPath(self.options['DIRECTORY'] + '/' + f))
		
		for f in listfile:
			frmwk.print_status('sorting : %s' % f)
			WriteToFile(f,sorted(list(set(ReadFromFile(f)))))
