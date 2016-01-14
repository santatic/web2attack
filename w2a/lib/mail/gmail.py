import imaplib
from email import message_from_string
from email.header import decode_header
from re import compile

class Gmail():
	"""docstring for Gmail"""
	def __init__(self):
		# imaplib.Debug		= 4
		self.imap_server	= 'imap.gmail.com'
		self.imap_port		= 993
		self.extracter		= compile(r'(?P<id>\d*) \(UID (?P<uid>\d*) FLAGS \((?P<flags>.*)\)\s')
		self.server 		= imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
		self.inbox			= []
	def login(self, username, password):
		self.server.login(username,password)

	def logout(self):
		self.server.logout()

	def getInbox(self):
		self.server.select('INBOX',readonly=1)
		resp, data	= self.server.search(None, '(UNDELETED)')
		fetch_list	= ','.join((b' '.join(data).decode('utf-8')).split(' '))
		if fetch_list:
			fetch	= self.server.fetch(fetch_list, '(UID FLAGS BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
			for fm in fetch[1]:
				if len(fm) > 1:
					self.inbox.insert(0,self.extracter.match(fm[0].decode('utf-8')).groupdict())

	def getInboxContent(self,ilen):
		result	= []
		for i in range(ilen):
			if len(self.inbox) <= i:
				break
			status, data =self.server.uid('fetch', self.inbox[i]['uid'], 'RFC822')
			messagePlainText = ''
			messageHTML = ''
			for response_part in data:
				if isinstance(response_part, tuple):
					msg = message_from_string(response_part[1].decode('utf-8'))
					for part in msg.walk():
						if str(part.get_content_type()) == 'text/plain':
							messagePlainText = messagePlainText + part.get_payload(decode=True).decode('utf-8', 'replace')
						if str(part.get_content_type()) == 'text/html':
							messageHTML = messageHTML + part.get_payload(decode=True).decode('utf-8', 'replace')

			if messageHTML:
				Body = messageHTML
			else:
				Body = messagePlainText
			if('Subject' in msg):
				subject, charset = decode_header(msg['Subject'])[0]
				subject = subject.decode('utf-8', 'replace')
			else:
				subject = ''
			result.append({'from':msg['From'], 'subject':subject, 'body':Body, 'date':msg['Date']})
		return result
	