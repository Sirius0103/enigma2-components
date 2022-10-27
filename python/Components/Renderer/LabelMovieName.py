# LabelMovieName Render
# Copyright (c) 2boom 2022
# v.0.1-r2
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
from Components.VariableText import VariableText
from Components.Renderer.Renderer import Renderer

from enigma import eLabel

class LabelMovieName(VariableText, Renderer):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)

	GUI_WIDGET = eLabel
		
	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))

	def changed(self, what):
		self.tmptext = self.text = self.medianame = ''
		if what[0] == self.CHANGED_CLEAR:
			self.text = ''
		else:
			self.text = ''
		ListOfTags = ['WEB-DLRip', 'WEB-DL', 'BDRip', 'BluRay', 'HDRip-AVC', 'WEB-DLRip-AVC', 'WEBRip', 'HDRip', '720p', '1080p', '2160p', 'x264', 'AC3']
		self.medianame = self.source.text.replace(' ', '.').replace('(', '').replace(')', '')
		for tags in ListOfTags:
			self.medianame = self.medianame.replace(tags, '')
		for i in range(len(self.medianame.split('.'))):
			if self.medianame.split('.')[i].isdigit() and len(self.medianame.split('.')[i]) == 4 and int(self.medianame.split('.')[i]) > 1900:
				self.tmptext = '%s (%s)' % (self.medianame.split(self.medianame.split('.')[i])[0], self.medianame.split('.')[i])
			elif self.medianame.split('.')[i].startswith('S') and self.medianame.split('.')[i][1:3].isdigit() and self.medianame.split('.')[i][3] == 'E' and self.medianame.split('.')[i][4:6].isdigit() and len(self.medianame.split('.')[i]) == 6:
				self.tmptext = '%s (%s)' % (self.medianame.split(self.medianame.split('.')[i])[0], self.medianame.split('.')[i].upper())
		if self.tmptext == '':
			self.tmptext = self.medianame[:-4]
				
		self.text = ' '.join(self.tmptext.strip().replace('.', ' ').split())
