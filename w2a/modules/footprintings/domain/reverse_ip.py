#  modules/reverse_ip.py
#
#  Copyright 2012 VinaKid :">

from w2a.core.templates import Templates
# from w2a.lib.net.http import HTTP
from w2a.config import CONFIG
from w2a.lib.thread import Thread
from w2a.lib.dbconnect import IPInSerter, getDomain, getIP
from w2a.lib.file import full_path, read_from_file, append_file

from re import findall,search
from urllib.parse import urlencode
from socket import gethostbyname, timeout


class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		############################
		self.version		= 1
		self.author			= [ 'VinaKid' ]
		self.description 	= 'Get all domain in IP'
		self.detailed_description	= 	'Module dùng để reverse ip từ 1 domain/ip\n'+\
										'- Có thể set nhiều domain/ip ngăn cách bằng dấu phẩy\n'+\
										'- Option CHECK sẽ kiểm tra kết quả cùng ip với domain/ip nhập vào\n'+\
										'- Option THREADS là thread để dùng Option CHECK\n'+\
										'- Option RHOSTLIST là reverse ip từ file chứa list domain/ip\n'+\
										'nếu không set RHOST thì sẽ get domain/list tù RHOSTLIST\n'
		############################
		self.options.add_string('RHOST', 'IP/Domain to reverse(support : ip1,ip2...)', False)
		self.options.add_boolean('CHECK', 'check domain is in this IP ', default = True)
		self.options.add_integer('THREADS', 'thread check domain', default = 10)
		############################
		self.advanced_options.add_path('RHOSTLIST', 'Path to domain list', default = CONFIG.DATA_PATH + '/victim.lst')
		self.advanced_options.add_path('OUTPUT', 'Output directory', default = CONFIG.TMP_PATH + '/reverseip/')
		############################
		self.fmt_string	= "Site: {0:<30} {1}"
		self.SEARCHERS	= [
					{
						'SITE'	:	"My-ip-neighbors.com",
						'URL'	:	"http://www.my-ip-neighbors.com/?domain=%s",
						'REGEX'	:	r'<td class="action"\starget="\_blank"><a\shref="http\:\/\/whois\.domaintools\.com\/(.*?)"\starget="\_blank"\sclass="external">Whois<\/a><\/td>',
					},
					{
						'SITE'	:	"Yougetsignal.com",
						'DATA'	:	'remoteAddress=%s',
						'URL'	:	"http://www.yougetsignal.com/tools/web-sites-on-web-server/php/get-web-sites-on-web-server-json-data.php",
						'REGEX'	:	r'\["(.*?)",\s"?"\]',
					},
					# {
					# 	'SITE'	:	"Whois.WebHosting.info",
					# 	'URL'	:	"http://whois.webhosting.info/%s?pi=%s&ob=SLD&oo=DESC",
					# 	'SP'	:	self.Whoiswebhosting,
					# },
					{
						'SITE'	:	"Ip-adress.com",
						'URL'	:	"http://www.ip-adress.com/reverse_ip/%s",
						'REGEX'	:	r'<td style\=\"font\-size\:8pt\">.\n\[<a href="\/whois\/(.*?)">Whois<\/a>\]',
					},
					{
						'SITE'	:	"Bing.com",
						'URL'	:	"http://api.search.live.net/xml.aspx?Appid=%s&query=ip:%s&Sources=Web&Version=2.0&Web.Count=50&Web.Offset=%s",
						'SP'	:	self.BingApi,
					},
					{
						'SITE'	:	"Ewhois.com",
						'URL'	:	"http://www.ewhois.com/",
						'SP'	:	self.eWhois,
					},
					{
						'SITE'	:	"Sameip.org",
						'URL'	:	"http://sameip.org/ip/%s/",
						'REGEX'	:	r'<a href="http:\/\/.*?" rel=\'nofollow\' title="visit .*?" target="_blank">(.*?)<\/a>',
					},
					{
						'SITE'	:	"Robtex.com",
						'URL'	:	"http://www.robtex.com/ajax/dns/%s.html",
						'REGEX'	:	r'[host|dns]\.robtex\.com\/(.*?)\.html',
					},
					{
						'SITE'	:	"Tools.web-max.ca",
						'URL'	:	"http://ip2web.web-max.ca/?byip=1&ip=%s",
						'REGEX'	:	r'<a href="http:\/\/.*?" target="_blank">(.*?)<\/a>',
					},
					{
						'SITE'	:	"DNStrails.com",
						'URL'	:	"http://www.DNStrails.com/tools/lookup.htm?ip=%s&date=recent",
						'REGEX'	:	r'<a\shref="lookup\.htm\?.*?=(.*?)&date=recent">',
					},
					{
						'SITE'	:	"Pagesinventory.com",
						'URL'	:	"http://www.pagesinventory.com/ip/%s.html",
						'REGEX'	:	r'<td><a\shref="/domain/.*?\.html">(.*?)</a></td>'
					},
					{
						'SITE'	:	"ViewDNS.info",
						'URL'	:	"http://viewdns.info/reverseip/?host=%s",
						'REGEX'	:	r'<tr><td>([a-zA-Z0-9\.\-_]{1,50}?\.[a-zA-Z0-9\.\-_]{1,50}?)</td>'
					}
				]
	def run(self, frmwk, args):
		self.frmwk	= frmwk
		hosts		= []
		hosts		= self.options['RHOST'].split(',') if self.options['RHOST'] else read_from_file(full_path(self.advanced_options['HOSTLIST']))

		for host in hosts:
			if self.worker(host.strip()) and self.advanced_options['OUTPUT']:
				output	= full_path(self.advanced_options['OUTPUT'] + '/' + self.ip + '.txt')
				append_file(output, self.domains)
				self.frmwk.print_line()
				self.frmwk.print_success('Saved: ' + output)

	def worker(self, rhost):
		self.domains 	= []
		self.victim		= rhost
		try:
			self.ip		= gethostbyname(self.victim)
		except:
			self.frmwk.print_error('Cann\' get IP Address')
			return False
		self.domains.append(self.victim)

		if self.ip in CONFIG.IP_WHITE_LIST:
			self.frmwk.print_error('Site down!')
			return False
		
		self.threadlist	= []
		self.frmwk.print_status("IP : %s" % self.ip)
		self.frmwk.print_line("-------------------------------------------")
	
		for searcher in self.SEARCHERS:
			thread	= Thread(target = self.reverseip, args = (searcher,))
			self.threadlist.append(thread)
			thread.start()
		for thread in self.threadlist:
			try:
				thread.join(CONFIG.TIME_OUT)
				if thread.isAlive():
					thread.terminate()
			except timeout:
				self.frmwk.print_error('Exception Timeout')
				pass

		self.frmwk.print_line("-------------------------------------------\n")
		#import from db
		if self.frmwk.dbconnect:
			self.frmwk.print_status('Getting subdomain in database')
			cursor	= self.frmwk.dbconnect.db.cursor()
			iprow = getIP(cursor, self.ip)
			if iprow:
				dmrow = getDomain(cursor, ['domain_name'], {'ip_id_list': '%%!%s|%%' % iprow[0]})
				for dm in dmrow:
					self.domains.append(dm[0])
			cursor.close()
		
		self.domains	= sortlistdomain(self.domains)
		if self.options['CHECK']:
			self.frmwk.print_status('Checking domain\'s in this IP')
			checker	= checkdomains(self.frmwk, self.ip, self.domains)
			checker.checklistdomain(self.options['THREADS'])
			self.domains	= sorted(list(set(checker.response)))


		if self.frmwk.dbconnect and self.options['CHECK']:
			self.frmwk.print_status('Saving database!')
			self.Saver()
		
		self.frmwk.print_success('List domain:')
		self.frmwk.print_line("----------------")
		self.frmwk.print_line("\n".join(self.domains))
		return True

	def reverseip(self, searcher):
		try:
			if 'SP' not in searcher:
				req	= HTTP(searcher['URL'])
				if 'DATA' in searcher:
					data	= req.Request(searcher['URL'], 'POST', searcher['DATA'] % self.ip)
				else:
					data	= req.Request(searcher['URL'] % self.ip)
				urls	= findall(searcher['REGEX'],data)
				self.frmwk.print_status(self.fmt_string.format(searcher['SITE'],urls.__len__()))
				self.domains	+= urls
			else:
				searcher['SP'](searcher)
		except Exception as e:
			pass
	
	def BingApi(self, searcher):
		KEY	= "49EB4B94127F7C7836C96DEB3F2CD8A6D12BDB71"
		req	= HTTP(searcher['URL'])
		data	= req.Request(searcher['URL'] % (KEY, self.ip, 0))
		total	= search('<web:Total>([0-9]+)<\/web:Total>',data).group(1)
		page	= int(int(total)/50 + 1)
		for i in range(1, page):
			data	+= req.Request(searcher['URL'] % (KEY, self.ip, i))
		result	= findall(r'<web:Url>(.+?)<\/web:Url>',data)
		urls	= []
		for url in result:
			urls.append(url.split('/',3)[2])
		self.frmwk.print_status(self.fmt_string.format(searcher['SITE'],urls.__len__()))
		self.domains	+= urls
	
	def eWhois(self, searcher):
		params				= urlencode({'_method':'POST','data[User][email]':'r12xr00tu@gmail.com','data[User][password]':'RitX:::R1tX','data[User][remember_me]':'0'})
		req					= HTTP("http://www.ewhois.com/")
		req.storecookie		= True
		req.rand_useragent	= False
		data				= req.Request('http://www.ewhois.com/login/', 'POST', params)
		data				= req.Request("http://www.ewhois.com/export/ip-address/%s/" % self.ip)
		urls				= findall(r'"(.*?)","","","[UA\-[0-9]+\-[0-9]+|]",""',data)
		self.frmwk.print_status(self.fmt_string.format(searcher['SITE'],urls.__len__()))
		self.domains		+= urls
	
	def Whoiswebhosting(self, searcher):
		req	= HTTP(searcher['URL'])
		urls	= []
		data	= req.Request(searcher['URL'] % (self.ip,1))
		last	= search(r'\?pi=([0-9]+)\&ob=SLD\&oo=DESC">\&nbsp\;\&nbsp\;Last\&nbsp\;&gt;\&gt\;<\/a>', data)
		url	= findall(r'<td><a href="http:\/\/whois\.webhosting\.info\/.*?\.">(.*?)\.<\/a><\/td>', data)
		urls	+= url
		if last:
			page = last.group(1)
			for i in range(2,int(page)):
				data	= req.Request(searcher['URL'] % (self.ip,i))
				if search('The security key helps us prevent automated searches', data):
					break
				url	= findall(r'<td><a href="http:\/\/whois\.webhosting\.info\/.*?\.">(.*?)\.<\/a><\/td>', data)
				urls	+= url
			self.frmwk.print_status(self.fmt_string.format(searcher['SITE'],urls.__len__()))
			self.domains	+= urls
		else:
			self.frmwk.print_status(self.fmt_string.format(searcher['SITE'],urls.__len__()))
			self.domains	+= urls
	def Saver(self):
		listip	= {self.ip : self.domains}
		info = []
		for ip in listip.keys():
			ipinfo					= {}
			ipinfo['ip']			= ip
			
			dminfo	= []
			for dm in listip[ip]:
				dmi 				= {}
				dmi['domain_name']	= dm
				dminfo.append(dmi)
			
			ipinfo['domains']		= dminfo
			info.append(ipinfo)
		IPInSerter(self.frmwk.dbconnect.db, info)
		
##################################
def realdomain(d):
	if search('([0-9]*?)\.([0-9]*?)\.([0-9]*?)\.([0-9]*?)', d):
		return False
	return d.lower().replace('www.', '')

def sortlistdomain(domains):
	result	= []
	for domain in domains:
		domain	= realdomain(domain)
		if domain:
			result.append(domain)
	return sorted(list(set(result)))
##################################
class checkdomains:
	def __init__(self,frmwk , ip, domains):
		self.frmwk		= frmwk
		self.ip			= ip
		self.domains	= domains
		self.dmslen		= len(domains)
		self.response	= []
		self.threadlist	= []
	
	def checklistdomain(self,threads):	# threading to check all domain
		for i in range(threads):
			thread	= Thread(target = self.checkdomain, args = ())
			self.threadlist.append(thread)
			thread.start()
		for thread in self.threadlist:
			thread.join()
		self.frmwk.print_line('')
	
	def checkdomain(self):			#check domain is true
		while len(self.domains) > 0:	#loop check if have domain in list checking
			domain	= self.domains.pop(0)
			dip		= ''
			try:
				dip	= gethostbyname(domain)
			except:
				try:
					dip	= gethostbyname('www.' + domain)
				except:
					pass
			if dip == self.ip:
				self.response.append(domain)
			percent	= 100 - int((len(self.domains)*100)/self.dmslen)
			self.frmwk.print_process(percent)