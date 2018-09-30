#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from w2a.core.templates import Templates
# from w2a.config import CONFIG
from w2a.lib.file import full_path, read_from_file, write_to_file

class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		############################
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Sort data in file or directory'
		self.detailed_description	= 'This module retreives sort and remove duplicate lines'
		############################
		self.options.add_path('INPUT', 'file hash info', False)
		self.options.add_path('CRACKED', 'file cracked info', False)
		self.options.add_path('OUTPUT', 'output to sort', False)
		############################

	def run(self, frmwk, args):
		self.input 		= self.options['INPUT']
		self.cracked 	= self.options['CRACKED']
		self.output 	= self.options['OUTPUT']

		# f = open(self.output , "w+")
		f = open(self.output , encoding='utf-8', mode='w+')

		# User name:           Administrator
		# User principal name: Administrator@free.com
		# Administrator:$NT$50d45644293044783ffce8b109fb6ed2:::
		case 		= 0
		write_line 	= ''
		for line in read_from_file(full_path(write_to_file.input)):
			if case == 0:
				if line.startswith('User name:'):
					write_line 	= line.split(':')[1].strip()
					case 		= 1
			elif case == 1:
				if line.startswith('User principal name:'):
					case 		= 2
					clear_pass 	= self.find_pass(write_line)
					write_line 	+= ':'+ line.split(':')[1].strip()
					if not clear_pass:
						continue
					write_line 	+= ':' + clear_pass
					case 		= 0
					f.write(write_line + '\n')
				else:
					self.frmwk.print_error('error while find User principal name!')
					return None
			elif case == 2:
				if line.startswith('SAM Account name:'):
					case 		= 0
					clear_pass 	= self.find_pass(line.split(':')[1].strip())
					if not clear_pass:
						continue
					write_line 	+= ':' + clear_pass
					f.write(write_line + '\n')
				else:
					self.frmwk.print_error('error while find User principal name!')
					return None

		f.close()

	def find_pass(self, user):
		for line in read_from_file(full_path(write_to_file.cracked)):
			if line.startswith(user):
				return line.split(':', 2)[1]
		return None