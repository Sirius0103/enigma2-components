# RouteInfo
# Copyright (c) 2boom 2012-22
# v.0.10
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
#
# <widget source="session.CurrentService" render="Label" position="189,397" zPosition="4" size="50,20" valign="center" halign="center" font="Regular;14" foregroundColor="foreground" transparent="1"  backgroundColor="background">
#	<convert type="RouteInfo"/>
# </widget>
#<widget source="session.CurrentService" render="Pixmap" pixmap="750HD/icons/ico_lan_on.png" position="1103,35" zPosition="1" size="28,15" transparent="1" alphatest="blend">
#    <convert type="RouteInfo">Lan  | Wifi | Modem</convert>
#    <convert type="ConditionalShowHide"/>
#  </widget>

from Components.Converter.Converter import Converter
from Components.Element import cached

class RouteInfo(Converter, object):
	Info = 0
	Lan = 1
	Wifi = 2
	Modem = 3

	def __init__(self, type):
		Converter.__init__(self, type)
		self.flag = '\t0003\t'
		if type == "Lan":
			self.type = self.Lan
		elif type == "Wifi":
			self.type = self.Wifi
		elif type == "Modem":
			self.type = self.Modem
		else:
			self.type = self.Info

	@cached
	def getBoolean(self):
		for line in open("/proc/net/route"):
			if self.type == self.Lan and line.startswith('eth0') and self.flag in line:
				return True
			elif self.type == self.Wifi and (line.startswith('wlan0') or line.startswith('wlan3') or line.startswith('ra0')) and self.flag in line:
				return True
			elif self.type == self.Modem and line.startswith('ppp0') and  self.flag in line:
				return True
		return False

	boolean = property(getBoolean)

	@cached
	def getText(self):
		info = ""
		for line in open("/proc/net/route"):
			if self.type == self.Lan and line.startswith('eth0') and self.flag in line:
				info = "Lan"
			elif self.type == self.Wifi and (line.startswith('wlan0') or line.startswith('wlan3') or line.startswith('ra0')) and self.flag in line:
				info = "WiFi"
			elif self.type == self.Modem and line.startswith('ppp0') and  self.flag in line:
				info = "3G/4G"
		return info

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, what)

