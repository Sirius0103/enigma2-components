# -*- coding: UTF-8 -*-
#Coders by Nikolasi
# v1.2
# code optimization (by Sirius)
# fix search Paths (by Sirius)
# py3 fix

from Components.Renderer.Renderer import Renderer
from Components.Converter.Poll import Poll
from Components.Pixmap import Pixmap
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, fileExists, resolveFilename
from enigma import eServiceCenter, ePixmap, ePicLoad, loadPic, eTimer
import os

class MovieCover(Renderer, Poll):
	__module__ = __name__
	searchPaths = ('/media/hdd/%s/', '/media/usb/%s/', '/media/sdb1/%s/', '/media/sdb2/%s/')

	def __init__(self):
		Poll.__init__(self)
		Renderer.__init__(self)
		self.path = 'covers'
		self.nameCache = {}
		self.size = []
		self.pics = []
		self.pixmaps = []
		self.pngname = ''
		self.png = ''
		self.picon = ePicLoad()
		self.pixdelay = 60

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value) in self.skinAttributes:
			if attrib == 'path':
				self.path = value
			elif attrib == 'size':
				self.size = value.split(',')
			elif attrib == 'pixdelay':
				self.pixdelay = int(value)
			attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		self.poll_interval = 2000
		self.poll_enabled = True
		if self.instance:
			pngname = ''
			if (what[0] != self.CHANGED_CLEAR):
				sname = self.source.text
				pngname = self.nameCache.get(sname, '')
				if (pngname == ''):
					pngname = self.findPicon(sname)
					if (pngname != ''):
						self.nameCache[sname] = pngname
			if (pngname == ''):
				pngname = self.nameCache.get('default', '')
				if (pngname == ''):
					pngname = self.findPicon('picon_default')
					if (pngname == ''):
						tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'no_poster.png')
						if fileExists(tmp):
							pngname = tmp
						self.nameCache['default'] = pngname
			if (self.pngname != pngname):
				self.pngname = pngname
				self.instance.setScale(1)
			self.picon.setPara((int(self.size[0]), int(self.size[1]), 1, 1, False, 1, '#00000000'))
			self.picon.startDecode(self.pngname, 0, 0, False)
			self.png = self.picon.getData()
			self.instance.setPixmap(self.png)
			self.runAnim()

	def findPicon(self, serviceName):
		for path in self.searchPaths:
			try:
				name = ((path % self.path) + serviceName)
				pngname = name + '.jpg'
				if fileExists(pngname):
					return pngname
			except:
				return ''
		return ''

	def runAnim(self):
		txt=[]
		text = ""
		if len(self.pics) == 0:
			for x in self.pixmaps:
				self.pics.append(loadPic(resolveFilename(SCOPE_SKIN_IMAGE, x), int(self.size[0]), int(self.size[1]), 0, 0, 0, 1))
			self.slide = len(self.pics)
			self.timer = eTimer()
			self.timer.callback.append(self.timerEvent)
			self.timer.start(self.pixdelay, True)
		else:
			self.instance.setPixmap(self.png)

	def timerEvent(self):
		if self.slide > 0:
			self.timer.stop()
			self.instance.setPixmap(self.pics[len(self.pics) - self.slide])
			self.slide = self.slide - 1
			self.timer.start(self.pixdelay, True)
		else:
			self.timer.stop()
			self.instance.setPixmap(self.png)
