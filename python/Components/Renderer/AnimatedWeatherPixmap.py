# Coded by Nikolasi
# v1.3
# code otimization (by Sirius)
# fix searchPaths (by Sirius)

from Renderer import Renderer 
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, fileExists, resolveFilename
from enigma import ePixmap, eTimer
import os

class AnimatedWeatherPixmap(Renderer):
	__module__ = __name__
#	searchPaths = ('/media/hdd/%s/', '/media/usb/%s/', '/media/sdb1/%s/', '/media/sdb2/%s/')

	def __init__(self):
		Renderer.__init__(self)
#		self.path = 'AnimatedWeatherPixmap'
		if fileExists('/media/hdd/AnimatedWeatherPixmap'):
			self.path = '/media/hdd/AnimatedWeatherPixmap'
		elif fileExists('/media/usb/AnimatedWeatherPixmap'):
			self.path = '/media/usb/AnimatedWeatherPixmap'
		elif fileExists('/media/sdb1/AnimatedWeatherPixmap'):
			self.path = '/media/sdb1/AnimatedWeatherPixmap'
		elif fileExists('/media/sdb2/AnimatedWeatherPixmap'):
			self.path = '/media/sdb2/AnimatedWeatherPixmap'
		else:
			self.path = None
		self.pixdelay = 100
		self.control = 1
		self.ftpcontrol = 0
		self.slideicon = None
		self.txt_naim = {'17': '0', '35': '0', '16': '14', '42': '14', '43': '14', '40': '18', '24': '23', '29': '27', '33': '27' ,'30': '28' ,'34': '28' ,'38': '37' ,'25': '44'}

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
			if sname == '1' or sname == '2' or sname == '3' or sname == '4':
				name = '0'
			elif sname == '9':
				name = '8'
			else:
				name = self.txt_naim.get(sname, sname)
#			if self.ftpcontrol == 1:
#				if fileExists('/tmp/AnimatedWeatherPixmap'):
#					self.runAnim(name)
#				else:
#					self.dovloud(name)
#			else:
#				self.runAnim(name)
			self.runAnim(name)

#	def dovloud(self, id):
#		os.system('wget -q ftp://u5616:f4bca98e@frog.hostink.ru/public_ftp/AnimatedWeatherPixmap.tar.gz -O /tmp/AnimatedWeatherPixmap.tar.gz')
#		os.system('tar xzvf /tmp/AnimatedWeatherPixmap.tar.gz -C /')
#		os.system('rm -rf /tmp/AnimatedWeatherPixmap.tar.gz')
#		self.runAnim(id)

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
		self.instance.setPixmap(self.picsicon[self.slideicon - 1])
		self.slideicon = self.slideicon - 1
		self.timericon.start(self.pixdelay, True)
