# CamdInfo3
# Copyright (c) 2boom 2011-16
# v.1.1
# 
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
#	<convert type="CamdInfo3">Camd</convert>
# 
# 25.01.2020 code optimization mod by Sirius

from Poll import Poll
from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.ConfigList import ConfigListScreen
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Components.Element import cached
from Tools.Directories import fileExists
import os

class CamdInfo3(Poll, Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.poll_interval = 2000
		self.poll_enabled = True

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		if not service:
			return None
		camd = ""
		emu = server = ""
		serlist = camdlist = None
		nameemu = []
		nameser = []
		if not info:
			return ""
		# Alternative SoftCam Manager
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/AlternativeSoftCamManager/plugin.pyo"):
			try:
				if config.plugins.AltSoftcam.actcam.value is not None:
					return config.plugins.AltSoftcam.actcam.value
			except:
				return None
		# E-Panel
#		elif fileExists("/usr/lib/enigma2/python/Plugins/Extensions/epanel/plugin.pyo"):
#			try:
#				if config.plugins.epanel.activeemu.value is not None:
#					return config.plugins.epanel.activeemu.value
#			except:
#				return None
		# PKT
		elif fileExists("/usr/lib/enigma2/python/Plugins/Extensions/PKT/plugin.pyo"):
			try:
				if config.plugins.emuman.cam.value is not None:
					return config.plugins.emuman.cam.value
			except:
				return None
		# GlassSysUtil
		elif fileExists("/tmp/ucm_cam.info"):
			try:
				return open("/tmp/ucm_cam.info").read()
			except:
				return None
		# TS-Panel
		elif fileExists("/etc/startcam.sh"):
			try:
				for line in open("/etc/startcam.sh"):
					if "script" in line:
						return "%s" % line.split('/')[-1].split()[0][:-3]
			except:
				return None
		# VTI
		elif fileExists("/tmp/.emu.info"):
			try:
				for line in open("/tmp/.emu.info"):
					return line.strip('\n')
			except:
				return None
		# BlackHole
		elif fileExists("/etc/CurrentBhCamName"):
			try:
				return open("/etc/CurrentBhCamName").read()
			except:
				return None
		# Domica
		elif fileExists("/etc/active_emu.list"):
			try:
				return open("/etc/active_emu.list").read()
			except:
				return None
		# Egami old
		elif os.path.isfile("/etc/CurrentEGCamName"):
			try:
				return open("/etc/CurrentEGCamName").read()
			except:
				return None
		# Egami
		elif fileExists("/tmp/egami.inf"):
			try:
				for line in open("/tmp/egami.inf"):
					item = line.split(":",1)
					if item[0] == "Current emulator":
						return item[1].strip()
			except:
				return None
		# OoZooN
		elif fileExists("/tmp/cam.info"):
			try:
				return open("/tmp/cam.info").read()
			except:
				return None
		# Merlin2
		elif fileExists("/etc/clist.list"):
			try:
				return open("/etc/clist.list").read()
			except:
				return None
		# HDMU
		elif fileExists("/etc/.emustart"):
			try:
				for line in open("/etc/.emustart"):
					return line.split()[0].split('/')[-1]
			except:
				return None
		# GP3
		elif fileExists("/usr/lib/enigma2/python/Plugins/Bp/geminimain/lib/libgeminimain.so"):
			try:
				from Plugins.Bp.geminimain.plugin import GETCAMDLIST
				from Plugins.Bp.geminimain.lib import libgeminimain
				camdl = libgeminimain.getPyList(GETCAMDLIST)
				cam = None
				for x in camdl:
					if x[1] == 1:
						cam = x[2] 
				return cam
			except:
				return None
		# Pli & ATV
		elif fileExists("/etc/init.d/softcam") or fileExists("/etc/init.d/cardserver"):
			try:
				for line in open("/etc/init.d/softcam"):
					if 'echo' in line:
						nameemu.append(line)
				camdlist = "%s" % nameemu[1].split('"')[1]
			except:
				pass
			try:
				for line in open("/etc/init.d/cardserver"):
					if 'echo' in line:
						nameser.append(line)
				serlist = "%s" % nameser[1].split('"')[1]
			except:
				pass
			if serlist is not None and camdlist is not None:
				return ("%s %s" % (serlist, camdlist))
			elif camdlist is not None:
				return "%s" % camdlist
			elif serlist is not None:
				return "%s" % serlist
			return ""
		else:
			return None

		if serlist is not None:
			try:
				cardserver = ""
				for current in serlist.readlines():
					cardserver = current
				serlist.close()
			except:
				pass
		else:
			cardserver = " "

		if camdlist is not None:
			try:
				emu = ""
				for current in camdlist.readlines():
					emu = current
				camdlist.close()
			except:
				pass
		else:
			emu = " "

		return "%s %s" % (cardserver.split('\n')[0], emu.split('\n')[0])

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, what)
