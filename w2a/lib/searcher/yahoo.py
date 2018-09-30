# -*- coding: utf-8 -*-

from w2a.lib.searcher.search_engine import SearchEngine

class yahoo(SearchEngine):
	"""docstring for yahoo"""
	def __init__(self, keyworld, limit, delay):
		super().__init__('http://search.yahoo.com/', keyworld, limit, delay)
		self.name	= 'search.yahoo.com'
		
	def uriCreater(self):
		return "http://search.yahoo.com/search?p=" + self.keyworld + "&ei=UTF-8&fr=moz35&n=100&pstart=1&b=" + str(self.count)
	
	def Getdata(self, data):
		return data.split('<li><div class="res"><div>', 1)[1].rsplit('</span><br/></div></li></ol></div>', 1)[0].split('</div></li><li><div class="res"><div>')

	def Spliter(self, info):
		s	= {}
		s['url']	= info.split('/**', 1)

		if len(s['url']) > 1:
			s['url']	= s['url'][1].split('"', 1)[0]
		else:
			s['url']	= info.split('&u=', 1)
			if len(s['url']) > 1:
				s['url']	= s['url'][1].split('&', 1)[0]
			else:
				s['url']	= info.split('href="', 1)[1].split('"', 1)[0]
		try:
			s['data']	= info.split('class="abstr"', 1)[1].split('</span>', 1)[0]
		except:
			s['data']	= info
		s['data']	= s['data'].replace('<b>', '').replace('</b>', '').replace('\n', '').strip()
		return s

	def Has_Next(self, data):
		if data.find(">Next &gt;</a>") == -1:
			return False
		return True