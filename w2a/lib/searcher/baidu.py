# -*- coding: utf-8 -*-

from w2a.lib.searcher.Searcher import Searcher

from urllib.parse import unquote

class baidu(Searcher):
	"""docstring for google"""
	def __init__(self, keyworld, limit, delay):
		super().__init__('http://www.baidu.com/', keyworld, limit, delay)
		self.name	= 'www.baidu.com'
	def uriCreater(self):
		return "http://www.baidu.com/s?wd=" + self.keyworld + "&ie=utf-8&pn=" + str(self.count)
	
	def Getdata(self, data):
		return data.split('<td class=f><h3 class="t">', 1)[1].rsplit('</font></td></tr></table><br>', 1)[0].split('</font></td></tr></table><br>')

	def Spliter(self, info):
		s	= {}
		s['url']	= unquote(info.split('href="', 1)[1].split('"', 1)[0].strip())
		s['data']	= info.split('target="_blank"', 1)[1].split('</span>', 1)[0].replace('<font color=#CC0000>', '').replace('</font>', '').replace('<br>  ', '').replace('\n', '').strip()
		return s
	
	def Has_Next(self, data):
		if data.find(">下一页") == -1:
			return False
		return True