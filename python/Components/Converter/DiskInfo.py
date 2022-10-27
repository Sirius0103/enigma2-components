# DiskInfo Converter
# Copyright (c) 2boom 2014-22
# v.0.1-r3
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
# py3 fix

#Fotmat string: %C - capacity, %F - free, %M - model, %S - filesystem, %D - devpoint

from Components.Converter.Converter import Converter
from Components.Converter.Poll import Poll
from Components.Element import cached
from Components.Harddisk import harddiskmanager
from Tools.Directories import fileExists

class DiskInfo(Poll, Converter, object):
	capacity = 0
	free = 1
	model = 2
	fsystem = 3
	dpoint = 4
	format = 5

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.paramert_str = ''
		if type.startswith('capacity'):
			self.type = self.capacity
			self.device = type.split()[-1].strip()
		elif type.startswith('free'):
			self.type = self.free
			self.device = type.split()[-1].strip()
		elif type.startswith('model'):
			self.type = self.model
			self.device = type.split()[-1].strip()
		elif type.startswith('fsystem'):
			self.type = self.fsystem
			self.device = type.split()[-1].strip()
		elif type.startswith('dpoint'):
			self.type = self.dpoint
			self.device = type.split()[-1].strip()
		elif type.startswith('Format:'):
			self.type = self.format
			self.paramert_str = type

		self.poll_interval = 2000
		self.poll_enabled = True

	def filesystem(self, mountpoint):
		if fileExists("/proc/mounts"):
			for line in open("/proc/mounts"):
				if mountpoint in line:
					return "%s  %s" % (line.split()[2], line.split()[3].split(',')[0])
		return ''

	def devpoint(self, mountpoint):
		if fileExists("/proc/mounts"):
			for line in open("/proc/mounts"):
				if mountpoint in line:
					return line.split()[0]
		return ''

	@cached
	def getText(self):
		data = tmpdata = ''
		hddlist = harddiskmanager.HDDList()
		if hddlist:
			try:
				for count in range(len(hddlist)):
					hdd = hddlist[count][1]
					if 'hdd' in self.paramert_str:
						self.device = 'hdd'
					elif 'usb' in self.paramert_str:
						self.device = 'usb'
					if hdd.mountDevice() == '/media/%s' % self.device:
						if self.type == self.capacity:
							data = hdd.capacity()
						elif self.type == self.free:
							if int(hdd.free()) > 1024:
								data = '%d.%03d GB' % (hdd.free()/1024 , hdd.free()%1024)
							else:
								data = '%03d MB' % hdd.free()
						elif self.type == self.model:
							data = hdd.model()
						elif self.type == self.fsystem:
							data = self.filesystem(hdd.mountDevice())
						elif self.type == self.dpoint:
							data = self.devpoint(hdd.mountDevice())
						elif self.type == self.format:
							if int(hdd.free()) > 1024:
								tmpdata = '%d.%03d GB' % (hdd.free()/1024 , hdd.free()%1024)
							else:
								tmpdata = '%03d MB' % hdd.free()
							data = self.paramert_str.replace('Format:', '').replace('hdd', '').replace('usb', '').replace('%C', hdd.capacity()).replace('%M', hdd.model())\
								.replace('%S', self.filesystem(hdd.mountDevice())).replace('%D', self.devpoint(hdd.mountDevice())).replace('%F', tmpdata)
			except:
				pass
		return data

	text = property(getText)

	def changed(self, what):
		if what[0] == self.CHANGED_SPECIFIC:
			Converter.changed(self, what)
		elif what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)
