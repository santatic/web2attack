#  modules/scan/port.py
#
#  Copyright 2012 Kid :">

# Module Options
# ==============

#   Name       Current Setting               Required   Description
#   ----       ---------------               --------   -----------
#   HOSTS      10.97.42.1-255,10.97.43.1.255 yes        Range of ip
#   PORTS      4899,21-1024                  no         List/Range of port
#   TIMEOUT    8                             yes        Timout connect
#   THREADS    10                            yes        Threads numbers of scanner



import socket
from w2a.lib.net import socks
from w2a.core.templates import Templates
from w2a.config import CONFIG
from w2a.lib.thread import Thread
from threading import Lock

class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Automatic check open ports'
		self.detailed_description	= 'This module retreives check open ports'
		
		self.options.addString('HOSTS', 'Range of ip')
		self.options.addString('PORTS', 'List/Range of port', False, default = '21,22,25,80,445,1433,3306,3389,4899,8080,1521')
		self.options.addInteger('TIMEOUT', 'Timout connect', default = '8')
		self.options.addInteger('THREADS', 'Threads numbers of scanner', default = 10)
	
	def run(self, frmwk, args):
		self.frmwk 			= frmwk
		self.result			= []
		self.ports 			= []
		self.hosts 			= []
		self.threads 		= self.options['THREADS']
		self.list_threads	= []
		self.timeout 		= int(self.options['TIMEOUT'])
		self.lock			= Lock()
		self.thread_lock	= Lock()
		self.thread_flag	= True

		
		for host in self.options['HOSTS'].split(','):
			if host.find('-') != -1:
				r	= host.split('-')
				lr	= r[0].rsplit('.', 1)
				for i in range(int(lr[1]), int(r[1]) + 1):
					self.hosts.append(lr[0] +'.'+ str(i))
			else:
				self.hosts.append(host)
		
		if not self.options['PORTS']:
			for p in range(1, 65536):
				self.ports.append(p)
		else:
			for p in self.options['PORTS'].split(','):
				if p.find('-') != -1:
					r = p.split('-', 1)
					for p in range(int(r[0]) ,int(r[1]) + 1):
						self.ports.append(p)
				else:
					self.ports.append(int(p))
		###
		# print(self.ports)
		self.lock.acquire()

		for i in range(min(self.threads, len(self.hosts))):
			self.threader()

		self.lock.acquire()
		###
		self.result = sorted(self.result)
		self.frmwk.print_success("=============================================== [+]")
		for host in self.result:
			self.frmwk.print_success("[OPEN]\tHost : " + host[0] + "\tPort : " + str(host[1]))
		self.frmwk.print_success("=============================================== [+]")

	def threader(self):
		self.thread_lock.acquire()
		if(len(self.hosts) > 0):
			t = Thread(target = self.scanner, args = (self.hosts.pop(0),))
			t.start()
			self.list_threads.append(t)
		else:
			try:
				self.thread_flag = False
				for t in self.list_threads:
					if t.isAlive():
						t.join(self.timeout * len(self.ports) + 5)
						if t.isAlive():
							t.terminate()
			except:
				for t in self.list_threads:
					if t.isAlive():
						t.terminate()
			self.lock.release()
		self.thread_lock.release()

	def scanner(self, host):
		try:
			for p in self.ports:
				self.frmwk.print_status("[SCANNING]\tHost : " + host + "\tPort : " + str(p))
				try:
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
					s.settimeout(self.timeout)
					s.connect((host, p))
					s.shutdown(socket.SHUT_RDWR)
					self.result.append([host, p])

					self.frmwk.print_success("[OPEN]\tHost : " + host + "\tPort : " + str(p))
				except socket.timeout:
					self.frmwk.print_error("[CLOSE]\tHost : " + host + "\tPort : " + str(p))
				except:
					self.frmwk.print_error("Connect error !")
				finally:
					s.close()
			if self.thread_flag:
				Thread(target = self.threader).start()
		except KeyboardInterrupt:
			pass