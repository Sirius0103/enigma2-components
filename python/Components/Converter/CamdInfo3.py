# 2boom 2011-16
# CamdInfo3 - Converter
# 
#	<convert type="CamdInfo3">Camd</convert>
# 
# 25.11.2018 code optimization mod by Sirius

from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.ConfigList import ConfigListScreen
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Components.Element import cached
from Tools.Directories import fileExists
from Poll import Poll
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
		emu = ""
		server = ""
		serlist = None
		camdlist = None
		nameemu = []
		nameser = []
		if not info:
			return ""
		# Alternative SoftCam Manager
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/AlternativeSoftCamManager/plugin.pyo"):
			if config.plugins.AltSoftcam.actcam.value != "none":
				camdlist = config.plugins.AltSoftcam.actcam.value
			else:
				return None
		# E-Panel
		elif fileExists("//usr/lib/enigma2/python/Plugins/Extensions/epanel/plugin.pyo"):
			if config.plugins.epanel.activeemu.value != "none":
				camdlist = config.plugins.epanel.activeemu.value
			else:
				return None
		#PKT
		elif fileExists("//usr/lib/enigma2/python/Plugins/Extensions/PKT/plugin.pyo"):
			if config.plugins.emuman.cam.value:
				camdlist = config.plugins.emuman.cam.value
			else:
				return None
		# GlassSysUtil
		elif fileExists("/tmp/ucm_cam.info"):
			try:
				camdlist = open("/tmp/ucm_cam.info", "r")
			except:
				return None
		# VTI
		elif fileExists("/tmp/.emu.info"):
			try:
				camdlist = open("/tmp/.emu.info", "r")
			except:
				return None
		# BlackHole
		elif fileExists("/etc/CurrentBhCamName"):
			try:
				camdlist = open("/etc/CurrentBhCamName", "r")
			except:
				return None
		# Domica
		elif fileExists("/etc/active_emu.list"):
			try:
				camdlist = open("/etc/active_emu.list", "r")
			except:
				return None
		# Egami old
		elif os.path.isfile("/etc/CurrentEGCamName"):
			try:
				camdlist = open("/etc/CurrentEGCamName", "r")
			except:
				return None
		# Egami
		elif fileExists("/tmp/egami.inf"):
			for line in open("/tmp/egami.inf"):
				item = line.split(":",1)
				if item[0] == "Current emulator":
					camdlist = item[1].strip()
				else:
					return None
		# OoZooN
		elif fileExists("/tmp/cam.info"):
			try:
				camdlist = open("/tmp/cam.info", "r")
			except:
				return None
		# Merlin2
		elif fileExists("/etc/clist.list"):
			try:
				camdlist = open("/etc/clist.list", "r")
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
		#HDMU
		elif fileExists("/etc/.emustart") and fileExists("/etc/image-version"):
			try:
				for line in open("/etc/.emustart"):
					camdlist = line.split()[0].split('/')[-1]
			except:
				return None
		# ATV
		elif fileExists("/etc/image-version") and not fileExists("/etc/.emustart"):
			for line in open("/etc/issue"):
				if "openatv" in line:
					for line in open("/etc/enigma2/settings"):
						if line.find("config.softcam.actCam=") > -1:
							emu = line.split("=")[-1].strip('\n')
						if line.find("config.softcam.actCam2=") > -1:
							server = line.split("=")[-1].strip('\n')
							if server.find("no CAM 2 active") > -1:
								server = ""
			return "%s %s" % (emu, server)
		# Pli
		elif fileExists("/etc/init.d/softcam") or fileExists("/etc/init.d/cardserver"):
			for line in open("/etc/issue"):
				if "openpli" in line:
					try:
						for line in open("/etc/init.d/softcam"):
							if "echo" in line:
								nameemu.append(line)
						camdlist = "%s" % nameemu[1].split('"')[1]
					except:
						pass
					try:
						for line in open("/etc/init.d/cardserver"):
							if "echo" in line:
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
		# Script
		elif fileExists("/etc/startcam.sh"):
			try:
				for line in open("/etc/startcam.sh"):
					if "script" in line:
						camdlist = "%s" % line.split("/")[-1].split()[0][:-3]
			except:
				camdlist = None
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
