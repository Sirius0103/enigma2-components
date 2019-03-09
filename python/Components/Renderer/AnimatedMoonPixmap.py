# Coded by Nikolasi
# v1.4
# code optimization (by Sirius)
# fix search Paths (by Sirius)

from Renderer import Renderer 
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, fileExists, resolveFilename
from enigma import ePixmap, eTimer
import os

class AnimatedMoonPixmap(Renderer):
	__module__ = __name__
#	searchPaths = ('/media/hdd/%s/', '/media/usb/%s/', '/media/sdb1/%s/', '/media/sdb2/%s/')

	def __init__(self):
		Renderer.__init__(self)
#		self.path = 'AnimatedMoonPixmap'
		if fileExists('/usr/share/enigma2/AnimatedMoonPixmap'):
			self.path = '/usr/share/enigma2/AnimatedMoonPixmap'
		elif fileExists('/media/hdd/AnimatedMoonPixmap'):
			self.path = '/media/hdd/AnimatedMoonPixmap'
		elif fileExists('/media/usb/AnimatedMoonPixmap'):
			self.path = '/media/usb/AnimatedMoonPixmap'
		elif fileExists('/media/sdb1/AnimatedMoonPixmap'):
			self.path = '/media/sdb1/AnimatedMoonPixmap'
		elif fileExists('/media/sdb2/AnimatedMoonPixmap'):
			self.path = '/media/sdb2/AnimatedMoonPixmap'
		else:
			self.path = None
		self.pixdelay = 100
		self.control = 1
		self.ftpcontrol = 0
		self.slideicon = None

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value,) in self.skinAttributes:
			if attrib == 'path':
				self.path = value
			elif attrib == 'pixdelay':
				self.pixdelay = int(value)
			elif attrib == 'ftpcontrol':
				self.ftpcontrol = int(value)
			elif attrib == 'control':
				self.control = int(value)
			else:
				attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			sname = ''
			ext = ''
			name = ''
			if (what[0] != self.CHANGED_CLEAR):
				try:
					ext = self.source.iconfilename
					if ext != "":
						sname = os.path.split(ext)[1]
						sname = sname.replace('.gif', '')
				except:
					sname = self.source.text
			self.runAnim(sname)

	def runAnim(self, id):
		global total
		animokicon = False
		if fileExists('%s/%s' % (self.path, id)):
			pathanimicon = '%s/%s/a' % (self.path, id)
			path = '%s/%s' % (self.path, id)
			dir_work = os.listdir(path)
			total = len(dir_work)
			self.slideicon = total
			animokicon = True
		else:
			if fileExists('%s/NA' % self.path):
				pathanimicon = '%s/NA/a' % self.path
				path = '%s/NA'  % self.path
				dir_work = os.listdir(path)
				total = len(dir_work)
				self.slideicon = total
				animokicon = True
		if animokicon == True:
			self.picsicon = []
			for x in range(self.slideicon):
				self.picsicon.append(LoadPixmap(pathanimicon + str(x) + '.png'))
			self.timericon = eTimer()
			self.timericon.callback.append(self.timerEvent)
			self.timericon.start(100, True)

	def timerEvent(self):
		if self.slideicon == 0:
			self.slideicon = total
		self.timericon.stop()
		self.instance.setScale(1)
		try:
			self.instance.setPixmap(self.picsicon[self.slideicon - 1])
		except:
			pass
		self.slideicon = self.slideicon - 1
		self.timericon.start(self.pixdelay, True)
