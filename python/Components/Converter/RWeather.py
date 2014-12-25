# RWeather Converter
# xml from rambler weather
# Copyright (c) 2boom 2014 (10.09.2014)
# v.0.2-r0
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# %S - city, %T - temp, %C - condition, %W - windspeed, %H- humiditydata

from Tools.Directories import fileExists, pathExists
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Console import Console as iConsole
from Components.Language import language
from os import environ
from Poll import Poll
import gettext
import time
import os

time_update = 20
time_update_ms = 3000

class RWeather(Poll, Converter, object):
	city = 0
	temp = 1
	condition = 2
	windtxt = 3
	windspeed = 4
	humiditytxt = 5
	humiditydata = 6
	picon = 7
	allinfo = 8
	format = 9

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "city":
			self.type = self.city
		elif type == "temp":
			self.type = self.temp
		elif type == "condition":
			self.type = self.condition
		elif type == "windtxt":
			self.type = self.windtxt
		elif type == "windspeed":
			self.type = self.windspeed
		elif type == "humiditytxt":
			self.type = self.humiditytxt
		elif type == "humiditydata":
			self.type = self.humiditydata
		elif type == "picon":
			self.type = self.picon
		elif type.startswith('Format:'):
			self.type = self.format
			self.paramert_str = type 
		else:
			self.type = self.allinfo
		self.iConsole = iConsole()
		self.poll_interval = time_update_ms
		self.poll_enabled = True
	
	def write_none(self):
		with open('/tmp/rweather.xml', 'w') as noneweather:
			noneweather.write('None')
		noneweather.close()
	
	def get_xmlfile(self):
		self.iConsole.ePopen("wget -P /tmp -T2 'http://informers.rambler.ru/weather/geoid//?version=4' -O /tmp/rweather.xml", self.control_xml)
	
	def control_xml(self, result, retval, extra_args):
		if retval is not 0:
			self.write_none()

	@cached
	def getText(self):
		info = weather_str = 'NA'
		rweather = {'city':'', 'temp':'', 'condition':'', 'windtxt':'', 'windspeed':'',\
			'humiditytxt':'', 'humiditydata':'', 'picon':'', 'allinfo':''}
		if fileExists("/tmp/rweather.xml"):
			if int((time.time() - os.stat('/tmp/rweather.xml').st_mtime)/60) >= time_update:
				self.get_xmlfile()
		else:
			self.get_xmlfile()
		if not fileExists('/tmp/rweather.xml'):
			self.write_none()
			return info
		if fileExists('/tmp/rweather.xml') and open('/tmp/rweather.xml').read() is 'None':
			return info
		if fileExists('/tmp/rweather.xml'):
			in_file = open('/tmp/rweather.xml').read().replace('\n', ', ').split('></')
			if len(in_file) is 7:
				rweather['picon'] = in_file[1].split('/')[-1].split('.')[0]
				weather_str = in_file[3].split('[')[-1].strip(']').split()
				weather_data = in_file[3].split('[')[-1].strip(']').split(',')
				for i in range(3, len(weather_data[0].split())):
					rweather['city'] += weather_data[0].split()[i] + ' '
				rweather['city'] = rweather['city'].strip()
				rweather['temp'] = weather_data[-3].split()[0]
				for i in range(1, len(weather_data[-3].split())):
					rweather['condition'] += weather_data[-3].split()[i].strip(',') + ' '
				rweather['condition'] = rweather['condition'].strip()
				rweather['windtxt'] = weather_data[-2].split()[0]
				rweather['windspeed'] =  '%s, %s %s' % (weather_data[-2].split()[-1], weather_data[-2].split()[-3], weather_data[-2].split()[-2])
				rweather['humiditytxt'] = weather_data[-1].split()[-2]
				rweather['humiditydata'] = weather_data[-1].split()[-1]
				for i in range(3,len(weather_str)):
					rweather['allinfo'] += weather_str[i] + ' '
				rweather['allinfo'] = rweather['allinfo'].strip()
		if self.type is self.city:
			info = rweather['city']
		if self.type is self.temp:
			info = rweather['temp']
		if self.type is self.condition:
			info = rweather['condition']
		if self.type is self.windtxt:
			info = rweather['windtxt']
		if self.type is self.windspeed:
			info = rweather['windspeed']
		if self.type is self.humiditytxt:
			info = rweather['humiditytxt']
		if self.type is self.humiditydata:
			info = rweather['humiditydata']
		if self.type is self.picon:
			info = rweather['picon']
		if self.type is self.allinfo:
			info = rweather['allinfo']
		if self.type is self.format:
			# %S - city, %T - temp, %C - condition, %W - windspeed, %H- humiditydata
			return self.paramert_str.replace('Format:', '').replace('%S', rweather['city']).replace('%T', rweather['temp']).replace('%C', rweather['condition'])\
				.replace('%W', rweather['windspeed']).replace('%H', rweather['humiditydata'])
		return info
	text = property(getText)

	def changed(self, what):
		Converter.changed(self, (self.CHANGED_POLL,))
