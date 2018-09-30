# -*- coding: utf-8 -*-

from w2a.lib.searcher.search_engine import SearchEngine

class bing(SearchEngine):
	"""docstring for bing"""

	def __init__(self, keyworld, limit, delay):
		super().__init__('http://www.bing.com/', keyworld, limit, delay)
		self.name	= 'www.bing.com'
	
	def uriCreater(self):
		return "http://www.bing.com/search?form=MOZSBR&pc=MOZI&q=" + self.keyworld + "&web.count=50&first=" + str(self.count)
	
	def Getdata(self, data):
		return data.split('<li class="sa_wr">', 1)[1].rsplit('</p> </div>  </div></li>', 1)[0].split('</p> </div>  </div></li><li class="sa_wr">')

	def Spliter(self, info):
		s	= {}
		s['url']	= info.split('<h3><a href="', 1)[1].split('"', 1)[0]
		s['data']	= info.split('<h3><a href="', 1)[1].split('">', 1)[1].replace('<strong>', '').replace('</strong>', '').replace('\n', '').strip()
		return s

	def Has_Next(self, data):
		if data.find(">Next</a>") == -1:
			return False
		return True