# WifiInfo
# Copyright (c) 2boom 2012-22
# v.1.1.3
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
#<widget source="session.CurrentService" render="Progress" pixmap="750HD/icons/linkq_ico.png" position="1103,35" zPosition="3" size="28,15" transparent="1" >
#    <convert type="WiFiInfo">linkqua</convert>
#  </widget>
#<widget source="session.CurrentService" render="Label" position="462,153" size="50,22" font="Regular; 17" zPosition="2" backgroundColor="background1" foregroundColor="white" transparent="1">
#    <convert type="WiFiInfo">link | level | noise | bitrate | ssid | encryption</convert>
#  </widget>


from Components.Converter.Poll import Poll
from Components.Converter.Converter import Converter
from Components.Element import cached
from pythonwifi.iwlibs import  Wireless
from Tools.Directories import fileExists

ifobj = Wireless('ra0')
type = 'ra0'
for line in open("/proc/net/wireless"):
	if line.split()[0] == "wlan0:":
		ifobj = Wireless('wlan0')
		type = 'wlan0'

class WiFiInfo(Poll, Converter, object):
	link = 0
	level = 1
	noise = 2
	linkqua = 3
	bitrate = 4
	ssid = 5
	encryption = 6
	wifilabel = 7
	wifionoff = 8
	
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "link":
			self.type = self.link
		elif type == "level":
			self.type = self.level
		elif type == "noise":
			self.type = self.noise
		elif type == "linkqua":
			self.type = self.linkqua
		elif type == "bitrate":
			self.type = self.bitrate
		elif type == "ssid":
			self.type = self.ssid
		elif type == "encryption":
			self.type = self.encryption
		elif type == "wifilabel":
			self.type = self.wifilabel
		elif type == "wifionoff":
			self.type = self.wifionoff
		self.poll_interval = 3000
		self.poll_enabled = True

	@cached
	def getText(self):
		wifi = " "
		for line in open("/proc/net/wireless"):
			if self.type == self.link and (line.split()[0] == "wlan0:" or line.split()[0] == "ra0:"):
				try:
					linkq = int(int(line.split()[2][:-1]) * 100) / int(ifobj.getQualityMax().quality)
				except:
					linkq = 0
				if linkq == 0:
					wifi = " "
				else:
					wifi = "%s%%" % linkq
			elif self.type == self.ssid and (line.split()[0] == "wlan0:" or line.split()[0] == "ra0:"):
				try:
					wifi = "%s" % ifobj.getEssid()
				except:
					wifi = " "
			elif self.type == self.wifilabel and (line.split()[0] == "wlan0:" or line.split()[0] == "ra0:"):
				if line.split()[2] == "0.":
					wifi = " "
				else:
					wifi = "WiFi:"
			elif self.type == self.bitrate and (line.split()[0] == "wlan0:" or line.split()[0] == "ra0:"):
				try:
					wifi = "%s" % ifobj.getBitrate()
				except:
					wifi = " "
			elif self.type == self.level and (line.split()[0] == "wlan0:" or line.split()[0] == "ra0:"):
				wifi = ("%s dBm" % line.split()[3])
			elif self.type == self.noise and (line.split()[0] == "wlan0:" or line.split()[0] == "ra0:"):
				wifi = ("%s dBm" % line.split()[4])
			elif self.type == self.encryption and (line.split()[0] == "wlan0:" or line.split()[0] == "ra0:"):
				if fileExists("/etc/wpa_supplicant.%s.conf" % type):
					wifi = "Open"
					for line in open("/etc/wpa_supplicant.%s.conf" % type):
						if "proto" in line:
							if line.split('=')[1] == "WPA\n":
								wifi = "WPA"
							elif line.split('=')[1] == "RSN\n":
								wifi = "WPA2"
							elif line.split('=')[1] == "WPA RSN\n":
								wifi = "WPA/WPA2"
						if "wep_key0" in line:
							wifi = "WEP"
		return wifi
	text = property(getText)

	@cached
	def getValue(self):
		linkq = 0
		for line in open("/proc/net/wireless"):
			if self.type == self.linkqua and (line.split()[0] == "wlan0:" or line.split()[0] == "ra0:"):
				try:
					linkq = int(int(line.split()[2][:-1]) * 100) / int(ifobj.getQualityMax().quality)
				except:
					linkq = 0
		return linkq
	value = property(getValue)
	range = 100

	@cached
	def getBoolean(self):
		info = False
		for line in open("/proc/net/route"):
			if self.type == self.wifionoff and (line.split()[0] == "wlan0" or line.split()[0] == "ra0") and line.split()[3] == "0003":
				info = True
		return info

	boolean = property(getBoolean)

	def changed(self, what):
		if what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)
