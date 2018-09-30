# language/en-GB/en-GB.xml
#  Copyright 2012 Kid :">

from w2a.core.templates import Templates
# from w2a.lib.net.http import HTTP

from re import search

class Module(Templates):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.version		= 1
		self.author			= [ 'Kid' ]
		self.description 	= 'Brute joomla administrator account'
		self.detailed_description	= 'This module retreives connect with dictionary username and password'
		#######################
		self.options.add_string('URL', 'Link home page')

	def run(self, frmwk, args):
		self.version	= None
		url				= self.options['URL']
		if not url.endswith('/'):
			url +='/'
		###### dict from http://www.pepelux.org/programs/joomlascan/ #######
		storeversion	= [	
							['language/en-GB/en-GB.ini',[
								['version 1.5.x 2005-10-30 14:10:00','1.5.0.Beta-1.5.0.Beta'],
								['9913 2008-01-09 21:28:35Z','1.5.0.Stable-1.5.0.Stable'],
								['9990 2008-02-05 21:54:06Z','1.5.1.Stable-1.5.1.Stable'],
								['10053 2008-02-21 18:57:54Z','1.5.2.Stable-1.5.2.Stable'],
								['10208 2008-04-17 16:43:15Z','1.5.3.Stable'],
								['10498 2008-07-04 00:05:36Z','1.5.4.Stable-1.5.7.Stable'],
								['11214 2008-10-26 01:29:04Z','1.5.8.Stable-1.5.8.Stable'],
								['11391 2009-01-04 13:35:50Z','1.5.9.Stable-1.5.11.Stable'],
								['Copyright (C) 2005 - 2010 Open Source Matters','1.5.16.Stable-1.5.20.Stable'],
								['Problem with Joomla site','1.5.17.Stable-1.5.17.Stable'],
								['17165 2010-05-17 15:59:19Z','1.6.0.Beta1-1.6.0.Beta1'],
								['17420 2010-05-31 11:14:10Z','1.6.0.Beta2-1.6.0.Beta2'],
								['17675 2010-06-14 10:20:52Z','1.6.0.Beta3-1.6.0.Beta3'],
								['17903 2010-06-28 01:52:11Z','1.6.0.Beta4-1.6.0.Beta4'],
								['18082 2010-07-12 01:02:52Z','1.6.0.Beta5-1.6.0.Beta5'],
								['18198 2010-07-21 00:58:13Z','1.6.0.Beta6-1.6.0.Beta8'],
								['20196 2011-01-09 02:40:25Z','1.6.0.Stable-1.6.1.Stable'],
								['20990 2011-03-18 16:42:30Z','1.6.2.Stable-1.7.5.Stable']
							]],
							['components/com_contact/metadata.xml',[
								['8178 2007-07-23 05:39:47Z','1.5.0.RC2-1.5.18.Stable'],
								['17437 2010-06-01 14:35:04Z','1.5.19.Stable-1.5.20.Stable'],
								['16235 2010-04-20 04:13:25Z','1.6.0.Stable-1.7.5.Stable']
							]],
							['htaccess.txt',[
								['47 2005-09-15 02:55:27Z','1.0.0-1.0.2'],
								['423 2005-10-09 18:23:50Z','1.0.3-1.0.3'],
								['1005 2005-11-13 17:33:59Z','1.0.4-1.0.5'],
								['1570 2005-12-29 05:53:33Z','1.0.6-1.0.7'],
								['2368 2006-02-14 17:40:02Z','1.0.8-1.0.9'],
								['4085 2006-06-21 16:03:54Z','1.0.10-1.0.10'],
								['4756 2006-08-25 16:07:11Z','1.0.11-1.0.11'],
								['5973 2006-12-11 01:26:33Z','1.0.12-1.0.12'],
								['5975 2006-12-11 01:26:33Z','1.0.13-1.0.14.RC1'],
								['9317 2007-11-07 03:02:08Z','1.5.0.RC4-1.5.0.Stable'],
								['10492 2008-07-02 06:38:28Z','1.5.0.Beta-1.5.14.Stable'],
								['13415 2009-11-03 15:53:25Z','1.5.15.Stable-1.5.15.Stable'],
								['14401 2010-01-26 14:10:00Z','1.5.16.Stable-1.5.20.Stable'],
								['14276 2010-01-18 14:20:28Z','1.6.0.Beta1-1.6.0.Beta8'],
								['20196 2011-01-09 02:40:25Z','1.6.0.Stable-1.6.1.Stable'],
								['21101 2011-04-07 15:47:33Z','1.6.2.Stable-1.7.5.Stable']
							]],
							['administrator/language/en-GB/en-GB.ini',[
								['version 1.5.x 2005-10-30 14:10:00','1.5.0.Beta-1.5.0.Beta'],
								['9869 2008-01-05 04:00:13Z','1.5.0.Stable-1.5.0.Stable'],
								['9990 2008-02-05 21:54:06Z','1.5.1.Stable-1.5.1.Stable'],
								['10122 2008-03-10 11:58:27Z','1.5.2.Stable-1.5.2.Stable'],
								['10186 2008-04-02 13:10:12Z','1.5.3.Stable-1.5.3.Stable'],
								['10500 2008-07-04 06:57:07Z','1.5.4.Stable-1.5.4.Stable'],
								['10571 2008-07-21 01:27:35Z','1.5.5.Stable-1.5.7.Stable'],
								['11213 2008-10-25 12:43:11Z','1.5.8.Stable-1.5.8.Stable'],
								['11391 2009-01-04 13:35:50Z','1.5.9.Stable-1.5.9.Stable'],
								['11667 2009-03-08 20:32:38Z','1.5.10.Stable-1.5.10.Stable'],
								['11799 2009-05-06 02:15:50Z','1.5.11.Stable-1.5.11.Stable'],
								['12308 2009-06-23 04:05:28Z','1.5.12.Stable-1.5.14.Stable'],
								['13243 2009-10-20 04:01:04Z','1.5.15.Stable-1.5.15.Stable'],
								['16380 2010-04-23 09:19:48Z','1.5.16.Stable-1.5.20.Stable'],
								['17165 2010-05-17 15:59:19Z','1.6.0.Beta1-1.6.0.Beta1'],
								['17387 2010-05-30 16:28:20Z','1.6.0.Beta2-1.6.0.Beta2'],
								['17675 2010-06-14 10:20:52Z','1.6.0.Beta3-1.6.0.Beta3'],
								['17898 2010-06-27 13:03:01Z','1.6.0.Beta4-1.6.0.Beta4'],
								['18090 2010-07-12 10:49:58Z','1.6.0.Beta5-1.6.0.Beta5'],
								['18198 2010-07-21 00:58:13Z','1.6.0.Beta6-1.6.0.Beta6'],
								['18378 2010-08-09 17:29:44Z','1.6.0.Beta7-1.6.0.Beta7'],
								['18572 2010-08-22 09:57:58Z','1.6.0.Beta8-1.6.0.Beta8'],
								['20196 2011-01-09 02:40:25Z','1.6.0.Stable-1.6.0.Stable'],
								['20899 2011-03-07 20:56:09Z','1.6.1.Stable-1.6.1.Stable'],
								['20990 2011-03-18 16:42:30Z','1.6.2.Stable-1.6.6.Stable'],
								['21721 2011-07-01 08:48:47Z','1.7.0.Stable-1.7.2.Stable'],
								['22370 2011-11-09 16:18:06Z','1.7.3.Stable-1.7.5.Stable']
							]],
							['language/en-GB/en-GB.com_media.ini',[
								['10496 2008-07-03 07:08:39Z','1.5.0.Beta-1.5.12.Stable'],
								['12540 2009-07-22 17:34:44Z','1.5.13.Stable-1.5.14.Stable'],
								['13311 2009-10-24 04:13:49Z','1.5.15.Stable-1.5.15.Stable'],
								['14401 2010-01-26 14:10:00Z','1.5.16.Stable-1.5.20.Stable'],
								['17044 2010-05-14 09:52:50Z','1.6.0.Beta1-1.6.0.Beta3'],
								['17769 2010-06-20 01:50:48Z','1.6.0.Beta4-1.6.0.Beta8'],
								['20196 2011-01-09 02:40:25Z','1.6.0.Stable-1.6.6.Stable'],
								['21660 2011-06-23 13:25:32Z','1.7.0.Stable-1.7.0.Stable'],
								['21948 2011-08-08 16:02:50Z','1.7.1.Stable-1.7.5.Stable']
							]],
							['configuration.php-dist',[
								['47 2005-09-15 02:55:27Z','1.0.0-1.0.0'],
								['217 2005-09-21 15:15:58Z','1.0.1-1.0.2'],
								['506 2005-10-13 05:49:24Z','1.0.3-1.0.7'],
								['2622 2006-02-26 04:16:09Z','1.0.8-1.0.8'],
								['3754 2006-05-31 12:08:37Z','1.0.9-1.0.10'],
								['4802 2006-08-28 16:18:33Z','1.0.11-1.0.12'],
								['7424 2007-05-17 15:56:10Z','1.0.13-1.0.15'],
								['9991 2008-02-05 22:13:22Z','1.5.0.Stable-1.5.8.Stable'],
								['11409 2009-01-10 02:27:08Z','1.5.9.Stable-1.5.9.Stable'],
								['11687 2009-03-11 17:49:23Z','1.5.10.Stable-1.5.15.Stable'],
								['14401 2010-01-26 14:10:00Z','1.5.16.Stable-1.5.20.Stable']
							]]
						]
		requester		= HTTP(url)

		for link in storeversion:
			frmwk.print_status('Checking: ' + url + link[0])
			data	= requester.Request( url + link[0])
			if requester.response.status == 200:
				for vstr in link[1]:
					if data.find(vstr[0]) != -1:
						self.version	= vstr[1]
						break
			if self.version:
				break

		if not self.version:
			frmwk.print_status('Checking: ' + url + 'language/en-GB/en-GB.xml')
			data	= requester.Request( url + 'language/en-GB/en-GB.xml')
			if requester.response.status == 200:
				version	= search('<version>(.*?)</version>', data)
				if version:
					self.version	= version.group(1)
		if not self.version:
			frmwk.print_status('Checking: ' + url + 'components/com_mailto/mailto.xml')
			data	= requester.Request( url + 'components/com_mailto/mailto.xml')
			if requester.response.status == 200:
				version	= search('<version>(.*?)</version>', data)
				if version:
					self.version	= version.group(1)

		if self.version:
			frmwk.print_success('Fount version: ' + self.version)
		else:
			frmwk.print_error('Unknown version !')
