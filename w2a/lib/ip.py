from socket import gethostbyname
from w2a.config import CONFIG
from w2a.lib.thread import Thread
from w2a.core.printer import print_process,print_line

class IP:
	def __init__(self, *args, **kwargs):
		pass
	def getListIP(self, subs, thread = 1):
		self.listip	= {}
		self.subs	= subs
		threads		= []
		self.sublen	= len(subs)
		self.len	= 0
		for i in range(thread):
			t	= Thread(target = self.getIPThread)
			threads.append(t)
			t.start()
		for t in threads:
			t.join()
		print_line()
		return self.listip

	def getIPThread(self):
		while len(self.subs) > 0:
			self.len += 1
			per = int(self.len*100/self.sublen)
			print_process(per)

			d = self.subs.pop(0)
			try:
				sip	= str(gethostbyname(d))
			except:
				try:
					sip	= str(gethostbyname('www.'+d))
				except:
					continue

			if sip not in CONFIG.IP_WHITE_LIST:
				if sip in self.listip.keys():
					self.listip[sip].append(d)
				else:
					self.listip[sip] = [d]