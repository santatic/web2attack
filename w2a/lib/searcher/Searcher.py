# -*- coding: utf-8 -*-

from w2a.lib.net.http import HTTP
from w2a.lib.thread import Thread
from w2a.config import CONFIG
from w2a.core import printer

from re import findall, search
from urllib.parse import quote_plus
from time import sleep


class Searcher(Thread):
	"""docstring for Searcher"""
	def __init__(self, host, keyworld, limit, delay):
		super().__init__()
		self.keyworld	= quote_plus(keyworld)
		self.limit		= limit
		self.delay		= delay
		self.request	= HTTP(host, CONFIG.TIME_OUT, user_agents_type = 'bot')
		self.count		= 0
		self.info		= []
		self.step		= 10

	def run(self):
		while True:
			printer.print_line('\t{0:<25} {1:d}'.format(self.name, self.count))
			uri	= self.uriCreater()
			if not self.Has_Next(self.do_search(uri)):
				break
			if self.count <= 1:
				break
			self.count	+= self.step
			if self.count >= self.limit:
				break
			sleep(self.delay)
	def do_search(self, uri):
		data	= self.request.Request(uri)
		#print("-----------data : %s" % data)
		if data != '':
			try:
				info	= self.Getdata(data)
			except Exception as e:
				printer.print_error('%s : Nothing to do !' % self.name)
				pass
				return ''
			self.do_split(info)
		return data
	
	def do_split(self, info):
		ifl	= []
		for i in info:
			try:
				ifl.append(self.Spliter(i.strip()))
			except Exception as e:
				printer.print_error('%s Error : %s\ncontent: %s' % (self.name, e, i))
				pass
		self.info	+= ifl
		self.step	= len(ifl)
