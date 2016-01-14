# -*- coding: utf-8 -*-
from random import randint
from hashlib import md5
from re import match
def RandChar(len):
	res	= ''
	for i in range(len):
		x	= randint(32, 126)
		res += "%c" % x
	return res

def Md5(str):
	return md5(str.encode()).hexdigest()

def CheckUser(uname):
	if match('^[a-zA-Z0-9_]{3,30}$',uname):
		return True
	return False