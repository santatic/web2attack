# -*- coding: utf-8 -*-
from w2a.lib.net.http import HTTP
from urllib.parse import unquote, urlparse
from w2a.core.printer import print_process, print_line

from time import sleep
import re

def Filter(domain, infos, type):
	subs	= []
	emails	= []
	checked	= []
	req		= HTTP('https://docs.google.com/')
	ci	= 0
	il	= len(infos)
	for i in infos:
		ci += 1
		pc = int(ci*100/il)
		print_process(pc)
		if i in checked:
			continue
		i['data']	= unquote(i['data'])
		d	= domain_filter(domain, unquote(i['url']))
		d	+= domain_filter(domain, i['data'])
		e	= email_filter(domain, i['data'])
		d	= sorted(list(set(realdomain(d))))
		e 	= sorted(list(set(realemail(e))))
		if len(d) >= type or len(e) >= type:
			try:
				data	= getLink(req, i['url'])
				d	+= domain_filter(domain, data)
				e	+= email_filter(domain, data)
			except Exception as ex:
				pass
			sleep(2)
		subs	+= sorted(list(set(realdomain(d))))
		emails 	+= sorted(list(set(realemail(e))))
		checked.append(i)
	print_line('')
	return (subs, emails)

def realdomain(dms):
	res	= []
	for d in dms:
		res.append(d.lower().replace('www.',''))
	return res

def realemail(ems):
	res	= []
	for e in ems:
		res.append(e.lower())
	return res

def domain_filter(domain, data):
	domain 	= domain.replace(".", "\.")
	regex	= re.compile('([a-zA-Z0-9]+[a-zA-Z0-9\._-]+' + domain + ')', re.IGNORECASE|re.MULTILINE)
	return regex.findall(data)

def email_filter(domain, data):
	domain 	= domain.replace(".", "\.")
	regex = re.compile('([a-zA-Z]+[a-zA-Z0-9\._-]+@[a-zA-Z0-9._%+-]*' + domain + ')', re.IGNORECASE|re.MULTILINE)
	return regex.findall(data)

def getLink(req, url):
	link	= "https://docs.google.com/viewer?a=gt&url="+ url
	data	= req.Request(link, user_agents = False)
	return data