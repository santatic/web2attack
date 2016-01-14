#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, abspath, isdir, basename
from w2a.core.printer import print_error

def FullPath(f, strip = True):
	if strip:
		f = f.strip()
	return abspath(f)

def ReadFromFile(filename, strip = True):
	if isfile(filename):
		# result = []
		with open(filename, encoding='utf-8', mode='r') as f:
			try:
				for line in f:
					if strip:
						# result.append(line.strip())
						yield line.strip()
					else:
						# result.append(line)
						yield line
			except Exception as ex:
				print_error("Cann't read file : %s \nError: %s" % (filename, ex))
			finally:
				f.close()
				# return result;
	else:
		print_error("File %s do not exist!\n" % filename)

def WriteToFile(filename , data =[], strip = True):
	try:
		f = open(filename , encoding='utf-8', mode='w+')
	except Exception as e:
		print_error("Cann't open to write file : %s \n" % filename)
		return
	try:
		for line in data:
			if strip:
				f.write(line.strip() + '\n')
			else:
				f.write(line + '\n')
	except Exception as ex:
		print_error("Cann't write file : %s\nError: %s" % (filename, ex))
	finally:
		f.close()

def AppendFile(filename , data =[], strip = True):
	try:
		f = open(filename , "a+")
	except Exception as e:
		print_error("Cann't open to append file : %s \n" % filename)
		return
	
	try:
		for line in data:
			if strip:
				f.write(line.strip() + '\n')
			else:
				f.write(line + '\n')
	except Exception as ex:
		print_error("Cann't append file : %s\nError: %s" % (filename, ex))
	finally:
		f.close()

def ListDir(basepath = ''):
	files	= []
	dirs	= []
	path	= ''
	if basepath != '':
		basepath = basepath + '/'
	while True:
		if isdir(FullPath(basepath + path)):
			lfs = listdir(FullPath(basepath + path))
			for f in lfs:
				if not basename(f).startswith('__'):
					f = path + f
					if isdir(basepath + f):
						dirs.append(f + '/')
					else:
						files.append(f)
		else:
			print_error('No search directory: ' + path)
		if len(dirs) < 1:
			break
		path = dirs.pop(0)
	return files
