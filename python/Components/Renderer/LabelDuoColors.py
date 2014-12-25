# LabelDuoColors Render
# Copyright (c) 2boom 2014
# v.0.2-r0
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

from Components.VariableText import VariableText
from Renderer import Renderer

from enigma import eLabel

class LabelDuoColors(VariableText, Renderer):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.colors = self.firstColor = self.secondColor = self.tmptext = self.text = ""

	GUI_WIDGET = eLabel
	
	def convert_color(self, color_in):
		hex_color = {'0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9',\
			'a':':', 'b':';', 'c':'<', 'd':'=', 'e':'>', 'f':'?', 'A':':', 'B':';', 'C':'<', 'D':'=', 'E':'>', 'F':'?'}
		color_out = '\c'
		for i in range(1, len(color_in)):
			color_out += hex_color.get(color_in[i])
		return color_out

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value,) in self.skinAttributes:
			if attrib == 'foregroundColor':
				self.colors = value
			else:
				attribs.append((attrib, value))
		self.skinAttributes = attribs
		self.firstColor = self.convert_color(self.colors.split(',')[0].strip())
		self.secondColor = self.convert_color(self.colors.split(',')[-1].strip())
		return Renderer.applySkin(self, desktop, parent)
		
	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))

	def changed(self, what):
		self.tmptext = self.text = ''
		if what[0] is self.CHANGED_CLEAR:
			self.text = ''
		else:
			self.text = ''
			for i in range(len(self.source.text.split())):
				if i % 2 is 0: 
					self.tmptext += self.firstColor + ' ' + self.source.text.split()[i] + '  '
				else:
					self.tmptext += self.secondColor + self.source.text.split()[i] + '   '
			self.text = self.tmptext.strip()

