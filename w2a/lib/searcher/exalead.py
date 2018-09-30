# -*- coding: utf-8 -*-

from w2a.lib.searcher.search_engine import SearchEngine

class exalead(SearchEngine):
	"""docstring for exalead"""

	def __init__(self, keyworld, limit, delay):
		super().__init__('http://www.exalead.com/', keyworld, limit, delay)
		self.name	= 'www.exalead.com'
	def uriCreater(self):
		return "http://www.exalead.com/search/web/results/?q=" + self.keyworld + "&start_index=" + str(self.count)
	
	def Getdata(self, data):
		#print(data)
		return data.split('id="results"', 1)[1][22:].split('</ol>', 1)[0].strip().split('</li>')[:-1]

	def Spliter(self, info):
		s	= {}
		s['url']	= info.split('href="', 1)[1].split('"', 1)[0]
		s['data']	= info.split('</h3>', 1)[1].split('<span class="bookmarkLinks">', 1)[0].strip().replace('<b>', '').replace('</b>', '').replace('<br>', '').replace('\n', '')
		return s

	def Has_Next(self, data):
		if data.find("Go to the next page") == -1:
			return False
		return True