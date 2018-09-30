#  Copyright 2012 Kid :">

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header
from email import encoders
from os.path import basename
from time import sleep

from w2a.lib.file import full_path, read_from_file
from w2a.core.templates import Templates
from w2a.config import CONFIG

class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Auto send email'
		self.detailed_description	= 'This module retreives send email to many people'
		
		self.options.add_string('SENDER', 'Fake name to hide sender', default = '')
		self.options.add_string('TO', 'list email (support : email1,email2 ...)', False)
		self.options.add_path('TOLIST', 'list email from file', False)
		self.options.add_string('SUBJECT', 'Subject of email', default = 'Yêu cầu báo cáo tình hình KTXH 6 tháng cuối năm!')
		self.options.add_string('CONTENT', 'Text of content email', default = 'Dear anh/chị !<br/><br/>Em gởi anh/chị  bản kế hoach cuối năm bên mình, anh/chị xem qua rồi gởi Feedback lại cho em để em còn tổng hợp gởi sếp !<br/><br/>Thu Trang !')
		self.options.add_path('ATTACHFILE', 'Path to file', False)
		self.options.add_boolean('TLS', 'TLS support', default = False)
		self.options.add_integer('DELAY', 'Delay time for a request', default = 1)
		self.options.add_integer('COUNT', 'count email/request', default = 20)

		self.advanced_options.add_string('SMTPSERVER', 'ip/domain of smtp server (fake email: 127.0.0.1)', default = '127.0.0.1')
		self.advanced_options.add_string('USERNAME', 'smtp username', default = '')
		self.advanced_options.add_string('PASSWORD', 'smtp password', default = '')
		self.advanced_options.add_boolean('BCC', 'send email via bcc(faster)', default = False)
	
	def run(self, frmwk, args):
		server 	= self.advanced_options['SMTPSERVER']
		uname	= self.advanced_options['USERNAME']
		passwd 	= self.advanced_options['PASSWORD']
		bcc 	= self.advanced_options['BCC']
		tls 	= self.options['TLS']
		delay 	= self.options['DELAY']
		subject	= self.options['SUBJECT']
		attach	= self.options['ATTACHFILE']
		sender 	= self.options['SENDER']
		content = self.options['CONTENT']
		count 	= self.options['COUNT']

		if self.options['TO']:
			to		= self.options['TO'].split(',')
		elif self.options['TOLIST']:
			to = read_from_file(full_path(self.options['TOLIST']))
		else:
			frmwk.print_error('Nothing to do! set TO/TOLIST value (advanced options)')
			return
		
		if server in ['127.0.0.1', 'localhost']:
			uname	= sender

		frmwk.print_status('Init email sender!')
		msg				= MIMEMultipart()
		msg['From']		= "\"%s\" <%s>" % (sender,uname)
		# msg['To']		= '' #, '.join(to)
		msg['Subject']	= Header(subject, 'utf-8')

		msg.attach(MIMEText(content, 'html', 'UTF-8'))
		if attach:
			part = MIMEBase('application', 'octet-stream')
			part.set_payload(open(attach, 'rb').read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % basename(attach))
			msg.attach(part)
		frmwk.print_status('Login smtp server!')
		try:
			mailServer	= SMTP(server)
			mailServer.set_debuglevel(3)
			if server not in ['127.0.0.1', 'localhost']:
				mailServer.ehlo()
				if tls:
					mailServer.starttls()
					mailServer.ehlo()
				mailServer.login(uname, passwd)
			else:
				uname = sender
			frmwk.print_status('Login success!\nStart send all email!')
		except Exception as ex:
			frmwk.print_error('Login error: %s' % ex)
			return
		
		try:
			if bcc:
				mailServer.sendmail(uname, [t[0], '', ', '.join(t[1:])], msg.as_string())
			else:
				t	= []
				while len(to) > 0:
					if len(t) == count:
						mailServer.sendmail(uname, t, msg.as_string())
						frmwk.print_status('Sent to ' + ', '.join(t))
						t	= []
						sleep(delay)
					else:
						t.append(to.pop(0))
				if len(t) > 0:
					mailServer.sendmail(uname, t, msg.as_string())
					frmwk.print_status('Sent to ' + ', '.join(t))
			sleep(delay)

			frmwk.print_success('Successful!')
		except Exception as ex:
			frmwk.print_error('Send mail error: %s' % ex.args)
			pass
		mailServer.close()
		frmwk.print_status('Finished!')