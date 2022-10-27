# LabelSeparatorColors Render
# Copyright (c) 2boom 2022
# v.0.1-r1
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

class LabelSeparatorColor(VariableText, Renderer):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.colors = self.firstColor = self.secondColor = self.tmptext = self.text = self.separatorwithcolor = ""
		self.separatorsymbol = '|*'
		self.separator = '|'

	GUI_WIDGET = eLabel

	def convert_color(self, color_in):
		return '\c' + color_in.lower().replace('#','').replace('a',':').replace('b',';').replace('c','<').replace('d','=').replace('e','>').replace('f','?')

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value,) in self.skinAttributes:
			if attrib == 'foregroundColor':
				self.colors = value
			else:
				attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)
		
	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))

	def changed(self, what):
		self.tmptext = self.text = ''
		self.firstColor = self.convert_color(self.colors.split(',')[0].strip())
		self.secondColor = self.convert_color(self.colors.split(',')[-1].strip())
		if what[0] == self.CHANGED_CLEAR:
			self.text = ''
		else:
			self.text = ''
		for i in range(len(self.separatorsymbol)):
			if self.separatorsymbol[i] in self.source.text:
				self.separator = self.separatorsymbol[i]
		if self.separator in self.source.text:
			self.separatorwithcolor = '%s%s%s' % (self.secondColor, self.separator, self.firstColor)
			self.tmptext = '%s%s' % (self.firstColor, self.source.text.replace(self.separator, self.separatorwithcolor))
		else:
			self.tmptext = self.source.text

		self.text = ' '.join(self.tmptext.strip().split())
