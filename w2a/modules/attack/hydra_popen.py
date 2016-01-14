#  modules/attack/hydra_popen.py
#
#  Copyright 2013 Kid :">

from w2a.core.templates import Templates
from w2a.config import CONFIG
from w2a.lib.thread import Thread
from w2a.lib.file import FullPath, ReadFromFile
from w2a.lib.net import socks

from threading import Lock
from subprocess import Popen, PIPE
from os import unlink,path
import socket

class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Automatic check open ports'
		self.detailed_description	= 'This module retreives check open ports'
		########
		self.options.addString('HOSTS', 'Range of ip')
		self.options.addString('SERVICE', 'Service:Port hydra brute', default = 'smb:445')
		self.options.addPath('ACCOUNT', 'File containing username:password list')
		self.options.addInteger('TIMEOUT', 'Timeout connect', default = 16)
		self.options.addInteger('THREADS', 'Threads numbers of scanner', default = 8)
		########
		self.advanced_options.addString('HYDRAPOPEN', 'Hydra popen string', default = 'proxychains4 -f ~/.proxychains/pivoting.conf hydra')
		self.advanced_options.addString('DELAY', 'Delay of 1 connect/1 login', default =60)
	
	def run(self, frmwk, args):
		
		self.service, self.port	= tuple(self.options['SERVICE'].split(':'))
		self.threads 			= self.options['THREADS']
		self.timeout 			= int(self.options['TIMEOUT'])
		self.hydra 				= self.advanced_options['HYDRAPOPEN']
		self.delay 				= self.advanced_options['DELAY']
		###
		self.frmwk 			= frmwk
		self.result			= []
		self.ports 			= []
		self.hosts 			= []
		self.list_threads	= []
		self.lock			= Lock()
		self.thread_lock	= Lock()
		self.thread_flag	= True
		self.restore_file	= 'hydra.restore'
		self.accounts 		= FullPath(self.options['ACCOUNT'])
		try:
			for host in self.options['HOSTS'].split(','):
				if host.find('-') != -1:
					r	= host.split('-')
					lr	= r[0].rsplit('.', 1)
					for i in range(int(lr[1]), int(r[1]) + 1):
						self.hosts.append(lr[0] +'.'+ str(i))
				else:
					self.hosts.append(host)
			
			self.lock.acquire()

			for i in range(min(self.threads, len(self.hosts))):
				self.threader()

			self.lock.acquire()
		except KeyboardInterrupt:
			pass
		###
		self.ports = sorted(self.ports)
		self.result = sorted(self.result)

		self.frmwk.print_success("=============================================== [+]")
		for port in self.ports:
			self.frmwk.print_success(port)
		self.frmwk.print_success("=============================================== [+]")
		for host in self.result:
			self.frmwk.print_success(host)
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
						t.join(self.timeout * len(self.accounts) + 5)
						if t.isAlive():
							t.terminate()
			except:
				for t in self.list_threads:
					if t.isAlive():
						t.terminate()
			self.lock.release()
		self.thread_lock.release()

	def scanner(self, host):
		self.frmwk.print_status("[SCANNING]\tHost : " + host + "\tPort : " + self.port)
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.settimeout(self.timeout)
			s.connect((host, int(self.port)))
			s.shutdown(socket.SHUT_RDWR)

			port = "[OPEN]\tHost : " + host + "\tPort : " + self.port
			self.ports.append(port)
			self.frmwk.print_success(port)
			try:
				
				if path.exists(self.restore_file):
					unlink(self.restore_file)
				self.frmwk.print_status("[SCANNING]\tHost : " + host)
				hydra 		= self.hydra + ' -F -W ' + self.delay + ' -w '+ str(self.timeout) + ' -t 1 -C \'' + self.accounts + '\' ' + host + ' ' + self.service
				self.frmwk.print_line(hydra)
				
				proc 		= Popen(hydra, shell=True, stderr=PIPE, stdout=PIPE)
				ret_code 	= proc.wait()
			except KeyboardInterrupt:
				proc.kill()

			for line in proc.stdout:
				line 	= line.decode("utf-8").strip()
				self.frmwk.print_line(line)
				if line.find('  password: ') != -1:
					self.result.append(line)
					self.frmwk.print_success(line)
		except socket.timeout:
			self.frmwk.print_error("[CLOSE]\tHost : " + host + "\tPort : " + self.port)
		except:
			self.frmwk.print_error("Connect error !")
			self.thread_flag 	= False
		finally:
			s.close()
			
		if self.thread_flag:
			Thread(target = self.threader).start()
