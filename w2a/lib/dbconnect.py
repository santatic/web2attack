# -*- coding: utf-8 -*-

from w2a.lib.mysql import connector
from w2a.config import CONFIG
from datetime import datetime

class Config():
	"""docstring for Config"""
	HOST		= '127.0.0.1'
	PORT		= 3306
	DATABASE	= 'WebAttanker'
	USER		= 'root'
	PASSWORD	= 'dunghackem:('

	CHARSET		= 'utf8'
	UNICODE		= True
	WARNINGS	= True

	@classmethod
	def dbinfo(cls):
		return {
		'host':		cls.HOST,
		'database':	cls.DATABASE,
		'user':		cls.USER,
		'password':	cls.PASSWORD,
		'charset':	cls.CHARSET,
		'use_unicode':	cls.UNICODE,
		'get_warnings':	cls.WARNINGS,
		'port':		cls.PORT,
		}

class DBConnect():
	"""docstring for Connect"""
	def __init__(self):
		config		= Config.dbinfo().copy()
		self.db		= connector.Connect(**config)

	def close(self):
		self.db.close()

def getIP(cursor, ip):
	query	= "SELECT * FROM IPAddress WHERE ip='%s'" % ip
	cursor.execute(query)
	row	= cursor.fetchone()
	return row
	
def getDomain(cursor, column = ['*'], where = {'1':'1'}):
	query	= "SELECT " + ','.join(column) + " FROM Domains WHERE " + " and ".join("{0} like '{1}'".format(k,v) for k,v in where.items())
	cursor.execute(query)
	row	= cursor.fetchall()
	return row

def getUser(cursor, column = ['*'], where = {'1':'1'}):
	query	= "SELECT " + ','.join(column) + " FROM Member WHERE " + " and ".join("{0} like '{1}'".format(k,v) for k,v in where.items())
	cursor.execute(query)
	row	= cursor.fetchall()
	return row

def InsertIP(cursor, columns):
	row	= getIP(cursor, columns['ip'])
	if row == None:
		query	= "INSERT INTO IPAddress(" + ",".join(columns.keys()) + ", update_time) VALUES ('" + "','".join(v for k,v in columns.items()) +"', '" + str(datetime.today()) + "')"
		cursor.execute(query)
		return cursor.lastrowid
	else:
		return row[0]

def InsertDomain(cursor, ipid, columns):
	today	= str(datetime.today())
	row		= getDomain(cursor, ['id', 'mail_list', 'shell_list'], {'domain_name': columns['domain_name']})
	if len(row) == 0:
		query	= "INSERT INTO Domains (" + ",".join(columns.keys()) + ", ip_id_list, update_time) VALUES ('" + "','".join(v for k,v in columns.items()) +"', '!"+ str(ipid) +"|', '" + today + "')"
		cursor.execute(query)
	else:
		row	= row[0]
		if row[1] and 'mail_list' in columns:		#email
			# db_emails	= row[1].strip()
			# emails 		= columns['mail_list'].split('\n') + db_emails.split('\r\n')
			columns['mail_list']	= '\n'.join(sorted(list(set(columns['mail_list'].split('\n') + row[1].strip().split('\r\n')))))

		if row[2] and 'shell_list' in columns:		#shell
			# db_shells	= row[2].strip()
			columns['shell_list']	= '\n'.join(sorted(list(set(columns['shell_list'].split('\n') + '\n' + row[2].strip().split('\r\n')))))

		query	= "UPDATE Domains SET " + ','.join("{0}='{1}'".format(k,v) for k,v in columns.items()) + ", ip_id_list='!"+ str(ipid) +"|',update_time='" + today + "' WHERE id=" + str(row[0])
		cursor.execute(query)

def IPInSerter(db, iplist):
	# iplist = [
	# 	{	'ip': '192...',
	# 		'update_time': '2012-11-20',
	# 		'...': None,
	# 		'domains': [{	'domain_name'	: 'example.com',
	# 						'ip_id_list'	: '!1|',
	# 						'mail_list'		: 'a@example.com|'
	# 				}]
	# 	},
	# 	.....
	# ]
	cursor	= db.cursor()
	for ip in iplist:
		domains = ip['domains']
		del ip['domains']
		ipid	= InsertIP(cursor, ip)
		db.commit()
		for dm in domains:
			InsertDomain(cursor, ipid, dm)
			db.commit()
	cursor.close()
