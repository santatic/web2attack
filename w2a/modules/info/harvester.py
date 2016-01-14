#  modules/harvester.py
#
#  Copyright 2012 Kid :">

from w2a.core.templates import Templates
from w2a.lib.searcher import google, bing, yahoo, baidu, exalead, filter
from w2a.config import CONFIG
from w2a.lib.thread import Thread
from w2a.lib.dbconnect import IPInSerter, getDomain
from w2a.lib.ip import IP
from w2a.lib.file import FullPath, ReadFromFile, AppendFile

from socket import gethostbyname

class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		############################
		self.version		= 1
		self.author			= ['Kid']
		self.description 	= 'Get subdomain and email'
		self.detailed_description	= 	\
			'\tModule dùng để lấy subdomain và email của 1 hoặc nhiều domain\n' + \
			'thông qua bruteforce subdomain và lấy thông tin từ các search engineer\n\n'+\
			'- Có thể set nhiều domain cùng lúc thông qua option DOMAIN ngăn cách bằng dấu phẩy.\n'+\
			'	w2a > set DOMAIN google.com,bing.com,yahoo.com\n\n'+\
			'* Note: NẾU ko set option DOMAIN thì DOMAINLIST sẽ được sử dụng\n'+\
			'        để xóa DOMAIN dùng cmd : w2a > unset DOMAIN\n\n'+\
			'- Để get nhiều domain trong list domain dùng advanced option DOMAINLIST\n'+\
			'	w2a > set DOMAINLIST [path đến list domain])\n\n'+\
			'- Option TYPE dùng để thực hiện 3 mức scan nhanh->chậm\n'+\
			'tùy theo số kết quả (domain hoặc email) trên 1 request\n'+\
			'và thực hiện lấy thông tin lần nửa trong site đó\n\n'+\
			'- Option SUBLIST là path đến subdomain list,dùng để bruteforce subdomain\n\n'+\
			'	Nếu không bruteforce thì unset: w2a> unset SUBLIST\n\n'
										
		############################
		self.options.addString('DOMAIN', 'Domain/Company to search or company name (support: domain1,domain2...)', False)
		self.options.addString('SEARCHER', 'Select search enginee: google, bing, yahoo, baidu, exalead, all', default = 'all', complete = ['google', 'bing', 'yahoo', 'baidu', 'exalead', 'all'])
		self.options.addInteger('LIMIT', 'Set limit search', default = 1000)
		self.options.addString('TYPE', 'Type scan(fast, nomal , slow)', default = 'slow', complete = ['fast', 'nomal', 'slow'])
		self.options.addInteger('DELAY', 'Delay time', default = 1)
		self.options.addBoolean('MULTITHREADS', 'Get subdomain and email with multithreading', default = False)
		self.options.addPath('SUBLIST', 'Bruteforce subdomain list', False, default = CONFIG.DATA_PATH + '/dict/subdomain.vn')
		############################
		self.advanced_options.addInteger('SUBTHREADS', 'Thread bruteforce subdomain', default = 5)
		self.advanced_options.addBoolean('REVERSEIP', 'Reverse ip to find subdomain', False)
		self.advanced_options.addPath('DOMAINLIST', 'Path to domain list', False)
		self.advanced_options.addPath('OUTPUT', 'Output directory', False)

	def run(self, frmwk, args):
		self.frmwk			= frmwk
		self.domain			= self.options['DOMAIN']
		self.limit			= self.options['LIMIT']
		self.searcher		= self.options['SEARCHER']
		self.multithread	= self.options['MULTITHREADS']
		self.delay			= self.options['DELAY']
		self.subbrute		= self.options['SUBLIST'] if self.options['SUBLIST'] else []
		self.domainlist		= self.advanced_options['DOMAINLIST']
		self.output			= self.advanced_options['OUTPUT']
		self.subbrutethread	= self.advanced_options['SUBTHREADS']
		self.reverseip		= self.advanced_options['REVERSEIP']
		dms			= []
		if not self.domain:
			if self.domainlist:
				dms	= ReadFromFile(FullPath(self.domainlist))
			else:
				self.frmwk.print_error('Nothing to do! Must set DOMAIN/DOMAINLIST options first')
				return
		else:
			dms	= self.domain.split(',')

		for domain in dms:
			domain	= domain.replace('www.', '').strip()
			self.worker(domain)
			if self.output:
				output	= FullPath(self.output + '/' + domain + '.txt')
				AppendFile(output, self.emails)

	def worker(self, domain):
		threads		= []
		self.subs	= [domain]
		self.emails	= []
		self.listip	= {}
		##################################################

		subbrute = []
		for ext in ['.', '-', '']:
			for sub in self.subbrute:
				subbrute.append(sub + ext + domain)
		if len(subbrute) > 0:
			self.frmwk.print_status('Starting bruteforce subdomain in : %d thread' % self.subbrutethread)
			self.listip	= IP().getListIP(subbrute, self.subbrutethread)
		del subbrute
		##################################################
		if self.options['TYPE'].strip().lower() == "fast":
			type	= 2
		elif self.options['TYPE'].strip().lower() == "slow":
			type	= 0
		else:
			type	= 1
		
		##################################################
		self.frmwk.print_status("%s : Start search enginee !" % domain)
		keywork = '"@' + domain + '" ext:(' + ' OR '.join(CONFIG.EXTENSION) + ')'
		if self.searcher in ("yahoo", "all"):
			yh 	= yahoo.yahoo(keywork, self.limit, self.delay)
			yh.start()
			threads.append(yh)
	
		if self.searcher in ("bing", "all"):
			bg 	= bing.bing(keywork, self.limit, self.delay)
			bg.start()
			threads.append(bg)
		
		if self.searcher in ("baidu", "all"):
			bd 	= baidu.baidu('"@' + domain + '"', self.limit, self.delay)
			bd.start()
			threads.append(bd)
	
		if self.searcher in ("exalead", "all"):
			el 	= exalead.exalead(keywork, self.limit, self.delay)
			el.start()
			threads.append(el)

		if self.searcher in ("google", "all"):
			gg 	= google.google(keywork, self.limit, self.delay)
			gg.start()
			threads.append(gg)
		############### get info from db ##################
		if self.frmwk.dbconnect:
			self.frmwk.print_status('Getting data in database')
			cursor	= self.frmwk.dbconnect.db.cursor()
			dmrow = getDomain(cursor, ['domain_name', 'mail_list'], {'domain_name': '%%%s' % domain})
			if dmrow:
				for dm in dmrow:
					self.subs.append(dm[0])
					if dm[1]:
						for e in dm[1].split('\n'):
							self.emails.append(e.split('|')[0].strip())
				
			else:
				self.frmwk.print_status('Nothing in Database!')
			cursor.close()
		else:
			self.frmwk.print_error('Database connect false!')
		##################################################
		docsthreads	= []
		try:
			for t in threads:
				t.join()
				self.frmwk.print_status("Harvesting : <[ {0:<25} {1:d}".format(t.name, len(t.info)))
				if self.multithread:
					ps	= Thread(target = filter.Filter, args = (domain, t.info, type,))
					docsthreads.append(ps)
					ps.start()
				else:
					s,e 	= filter.Filter(domain, t.info, type)
					self.subs	+= s
					self.emails	+= e
		except KeyboardInterrupt:
			for t in threads:
				if t.isAlive():
					t.terminate()
			for t in docsthreads:
				if t.isAlive():
					t.terminate()
			pass
		if len(docsthreads) > 0:
			for ps in docsthreads:
				s,e = ps.join()
				self.subs	+= s
				self.emails	+= e

		self.subs.append(domain)
		self.subs	= sorted(list(set(self.subs)))
		self.emails	= sorted(list(set(self.emails)))
		############ check subdomain ##############
		self.frmwk.print_status('Checking subdomain in : %d thread' % self.subbrutethread)
		ips	= IP().getListIP(self.subs, self.subbrutethread)
		for ip in ips.keys():
			if ip in self.listip:
				self.listip[ip] = sorted(list(set(self.listip[ip] + ips[ip])))
			else:
				self.listip[ip] = ips[ip]
		del ips
		
		################ insert db #################
		if self.frmwk.dbconnect:
			self.frmwk.print_status('start save database!')
			self.DBInsert(domain)
		################# reverse ip ###############
		if self.reverseip:
			for ip in self.listip.keys():
				reip	= self.frmwk.modules['info/reverse_ip']
				reip.options.addString('RHOST', 'IP/Domain to reverse(support : ip1,ip2...)', default = ip)
				reip.options.addBoolean('CHECK', 'check domain is in this IP ', default = True)
				reip.options.addInteger('THREADS', 'thread check domain', default = 10)
				############################
				reip.advanced_options.addPath('HOSTLIST', 'Path to domain list', False)
				reip.advanced_options.addPath('OUTPUT', 'Output directory', False)
				reip.run(self.frmwk, None)
				self.frmwk.reload_module('info/reverse_ip')
				for d in reip.domains:
					if d.endswith(domain):
						self.listip[ip].append(d)
				self.listip[ip]	= sorted(list(set(self.listip[ip])))
		###########################################
		self.frmwk.print_line()
		self.frmwk.print_success("Hosts found in search engines:\n------------------------------")
		for ip in self.listip.keys():
			self.frmwk.print_success('IP Server : ' + ip)
			for dm in self.listip[ip]:
				self.frmwk.print_line('\t. ' + dm)
			self.frmwk.print_line()
		self.frmwk.print_line()
		
		self.frmwk.print_success("Emails found:\n-------------")
		self.frmwk.print_line("\n".join(self.emails))
		self.frmwk.print_line('')

	def DBInsert(self, domain):
		info = []
		for ip in self.listip.keys():
			ipinfo					= {}
			ipinfo['ip']			= ip
			
			dminfo	= []
			for dm in self.listip[ip]:
				dmi 				= {}
				dmi['domain_name']	= dm
				if dm == domain:
					dmi['mail_list']	= '|\n'.join(self.emails) + '|'
				dminfo.append(dmi)
			
			ipinfo['domains']		= dminfo
			info.append(ipinfo)
		IPInSerter(self.frmwk.dbconnect.db, info)