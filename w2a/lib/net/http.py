# http lib update 1/4/2013
#		+ add yield to send and revc big file 

from w2a.lib.user_agent import User_Agent, Bot_User_Agent
from w2a.config import CONFIG
from w2a.core.printer import print_error

from gzip import GzipFile
from io import BytesIO
from urllib import request, parse
from http.client import HTTPConnection, HTTPSConnection
from socket import setdefaulttimeout, timeout
from base64 import b64encode
from re import search

class HTTP:
	def __init__(self, host, timeout = CONFIG.TIME_OUT, proxy = CONFIG.PROXY, user_agents_type = ''):
		self.timeout 		= timeout
		self.proxy			= proxy
		
		self.store_cookie	= False
		self.redirect		= True				#flag redirect when check found Location in header
		self.rand_useragent	= True				#random useragents flag

		if user_agents_type == 'bot':
			self.user_agents 	= Bot_User_Agent()
		else:
			self.user_agents 	= User_Agent()

		self.user_agent	= self.user_agents.user_agent

		HTTPConnection.debuglevel 	= 10
		######################################
		self.url 		= ''
		self.method		= 'GET'
		self.headers	= {
				'User-Agent': self.user_agent,
				'Accept-Encoding': 'gzip, deflate',
				'Connection': 'close'
			}
		######################################
		https	= False
		if self.proxy != None:
			host	= proxy
		if host.startswith('http'):
			parser		= parse.urlparse(host)
			self.host	= parser.hostname
			self.port 	= parser.port
			if self.port == None:
				if parser.scheme == 'https':
					self.port	= 443
				else:
					self.port	= 80
			if parser.scheme == 'https':
				https	= True
			
			_user 	= parser.username if parser.username else ''
			_pass	= parser.password if parser.password else ''
			_login	= str(_user) + ':' + str(_pass)
		else:
			spliter		= host.split(':')
			self.host 	= spliter[0]
			if len(spliter) < 2:
				self.port	= 80

		if len(_login) > 1:
			self.headers.update({'Authorization': "Basic " + b64encode(_login.encode('ascii')).decode('utf-8')})

		if https:
			self.request 	= HTTPSConnection(self.host,self.port, timeout = self.timeout)
		else:
			self.request 	= HTTPConnection(self.host,self.port, timeout = self.timeout)

	def init(self, url, method , header = {}):
		try:
			if method:
				self.method 	= method
			# proxy setting
			if not self.proxy and url.startswith('http'):
				url = url.split('/', 3)
				if len(url) > 3:
					self.url 	= '/' + url[3]
			else:
				self.url 	= url

			#random user agent
			if self.rand_useragent:
				self.user_agent 	= self.user_agents.getRandomUserAgent()
				self.headers.update({'User-Agent': self.user_agent})
			
			#update header for POST method
			if self.method == 'POST':
				self.headers.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
			elif 'Content-Type' in self.headers:
				del self.headers['Content-Type']

			# update header
			if len(header) > 0:
				self.headers.update(header)

			# put all paramater request
			self.request.putrequest(self.method, self.url)

			# put all request header
			for hk, hv in self.headers.items():
				self.request.putheader(hk, hv)

			# add \r\n\r\n end of header
			self.request.endheaders()

			# set timeout request
			self.request.sock.settimeout(self.timeout)
		except Exception as e:
			raise

	def send(self, data =b''):
		if data:
			self.request.send(data)

	def recv(self, chunk = 0):
		### get response header
		self.response	= self.request.getresponse()

		### store cookie
		if self.store_cookie and self.response.getheader('set-cookie'):
			cookies = dict()
			cook 	= self.request.getheader['cookie'] + '; ' + self.response.getheader('set-cookie')
			for c in cook.split(';'):
				tmp	= c.trim().split('=', 1)
				if len(tmp) == 2:
					cookies.update({tmp[0],tmp[1]})
			self.request.putheader('cookie', '; '.join(k +'='+ v for k,v in cookies.items()))

		### yield all data
		if chunk > 0:
			while not self.response.closed:
				yield self.response.read(chunk)
		else:
			result 	= self.response.read()
			print(self.response.getheaders())

			### extract gzip file, this method not support for send chunk data
			if self.response.getheader('content-encoding') == 'gzip':
				result = GzipFile(fileobj=BytesIO(result)).read()

			### auto redirect, this method not support for send chunk data
			if self.redirect:
				refresh	= search(b'http-equiv=.refresh(.*?)content=("|\')(.*?)url=(.*?)\2', result[:1000].lower())
				if(self.response.getheader('location') or refresh):
					self.refresh 	= True
					if self.response.getheader('location'):
						self.url 	= self.response.getheader('location')
					else:
						self.url 	= refresh.group(4)
					self.params		= ''
					self.method 	= 'GET'
					if 'Content-Type' in self.headers:
						del self.headers['Content-Type']
			### yield all content
			yield result
			
		self.request.close()

	def Request(self, url, method = 'GET', params = b'', header = {}):
		self.refresh	= False
		self.params 	= params
		if type(self.params) == type(""):
			self.params = self.params.encode()
		if method.upper() == "POST":
			header.update({"Content-Length": len(self.params)})
			
		while True:
			self.init(url, method, header)
			self.send(self.params)
			self.result 	= b''
			for data in self.recv():
				self.result	+= data
			if not self.refresh:
				# print(self.result)
				return self.result
			else:
				self.refresh	= False

	# def Request(self, url, method = 'GET', params = None, header = {}, chunk = 0):
	# 	# print("data : %s \nparams : %s" % (url,params))
	# 	if self.rand_useragent:
	# 		self.user_agent 	= self.user_agents.getRandomUserAgent()
	# 		self.headers.update({'User-Agent': self.user_agent})
		
	# 	if params:
	# 		self.headers.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
	# 	elif 'Content-Type' in self.headers:
	# 		del self.headers['Content-Type']

	# 	if len(header) > 0:
	# 		self.headers.update(header)

	# 	while True:
	# 		if not self.proxy:
	# 			if url.startswith('http'):
	# 				url = url.split('/', 3)
	# 				if len(url) > 3:
	# 					url 	= '/' + url[3]
	# 		if params:
	# 			self.request.request(method, url, params, headers = self.headers)
	# 		else:
	# 			self.request.request(method, url, headers = self.headers)
			
	# 		self.request.sock.settimeout(self.timeout)
	# 		self.response	= self.request.getresponse()
	# 		######## store cookie ###########
	# 		if self.storecookie and self.response.getheader('set-cookie'):
	# 			cookies = []
	# 			for c in self.response.getheader('set-cookie').split(','):
	# 				cookies.append(c.split(';', 1)[0])

	# 			cookie 	= self.headers['Cookie'] + ';' if 'Cookie' in self.headers else ''
	# 			cookies = cookie + '; '.join(cookies)
				
	# 			result	= {}
	# 			for c in cookies.split(';'):
	# 				tmp	= c.strip().split('=', 1)
	# 				if len(tmp) == 2:
	# 					result[tmp[0]] = tmp[1]
	# 			self.cookie	= '; '.join(k +'='+ v for k,v in result.items())
	# 			self.headers.update({'Cookie': self.cookie})
	# 		###
	# 		if chunk > 0:
	# 			break

	# 		self.result = self.response.read()
	# 		if self.response.getheader('content-encoding') == 'gzip':
	# 			self.result = GzipFile(fileobj=BytesIO(self.result)).read()
	# 		# self.result	= self.result.decode('utf-8', 'replace')
	# 		###
	# 		refresh	= search(b'http-equiv=.refresh(.*?)content=("|\')(.*?)url=(.*?)\2',self.result[:1000].lower())
	# 		if (self.response.getheader('location') or refresh) and self.redirect:
	# 			if self.response.getheader('location'):
	# 				url 	= self.response.getheader('location')
	# 			else:
	# 				url = refresh.group(4)
	# 			params	= None
	# 			method	= 'GET'
	# 			if 'Content-Type' in self.headers:
	# 				del self.headers['Content-Type']
	# 		else:
	# 			break
	# 	#########################
	# 	if chunk > 0:
	# 		while not self.response.closed:
	# 			yield self.response.read(chunk)
	# 		self.request.close()
	# 	else:	
	# 		self.request.close()
	# 		yield self.result