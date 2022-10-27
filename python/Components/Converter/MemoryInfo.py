# MemoryInfo
# Copyright (c) 2boom 2013-22
# 0.4
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

# <widget source="session.CurrentService" render="Label" position="189,397" zPosition="4" size="350,20" noWrap="1" valign="center" halign="center" font="Regular;14" foregroundColor="clText" transparent="1"  backgroundColor="#20002450">
#	<convert type="MemoryInfo">MemTotal</convert>
# </widget>

from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.Element import cached
import os

class MemoryInfo(Converter, object):
	MemTotal = 0
	MemFree = 1
	SwapTotal = 2
	SwapFree = 3

	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = {
				"MemTotal": (self.MemTotal),
				"MemFree": (self.MemFree),
				"SwapTotal": (self.SwapTotal),
				"SwapFree": (self.SwapFree),
			}[type]

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		meminfo = open("cat /proc/meminfo", "r")
		if meminfo != None:
			for line in meminfo:
				if self.type == self.MemTotal and "MemTotal" in line:
					try:
						info = "%s Kb" % line.split()[1]
					except:
						return None
				elif self.type == self.MemFree and "MemFree" in line:
					try:
						info = "%s Kb" % line.split()[1]
					except:
						return None
				elif self.type == self.SwapTotal and "SwapTotal" in line:
					try:
						info = "%s Kb" % line.split()[1]
					except:
						return None
				elif self.type == self.SwapFree and "SwapFree" in line:
					try:
						info = "%s Kb" % line.split()[1]
					except:
						return None
			meminfo.close()
			return info
		else:
			meminfo.close()
			return ""

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, what)
