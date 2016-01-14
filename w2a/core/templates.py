#  framework/templates.py
#  
#  Copyright 2011 Spencer J. McIntyre <SMcIntyre [at] SecureState [dot] net>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from .options import Options

class Templates:
	def __init__(self):
		self.name					= 'unknown'
		self.version				= 0
		self.author					= ['anonymous']
		self.description			= 'This module is undocumented.'
		self.detailed_description	= 'This module is undocumented.'
		self.options				= Options()
		self.advanced_options		= Options()

	def __repr__(self):
		return '<' + self.__class__.__name__ + ' ' + self.name + ' >'
