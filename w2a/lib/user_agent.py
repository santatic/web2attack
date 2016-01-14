# -*- coding: utf-8 -*-

from random import choice

from w2a.lib.file import FullPath, ReadFromFile
from w2a.config import CONFIG

class User_Agent:
	def __init__(self, filename = CONFIG.DATA_PATH + '/user-agent/user-agents.txt'):
		self.user_agents	= []
		for agent in ReadFromFile(FullPath(filename)):
			self.user_agents.append(agent)
		self.user_agent		= choice(self.user_agents)
	
	def getRandomUserAgent(self):
		return choice(self.user_agents)
	
	def getUserAgent(self):
		return user_agent
class Bot_User_Agent(User_Agent):
	def __init__(self, filename = CONFIG.DATA_PATH + '/user-agent/bot_user-agents.txt'):
		User_Agent.__init__(self, filename)