# TunerBar Converter
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

#WARNING! source="session.FrontendInfo"

from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.NimManager import nimmanager

class TunerBar(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type.split(',')
		self.maincolor = self.convert_color(self.type[0].strip())
		self.workcolor = self.convert_color(self.type[1].strip())

	def convert_color(self, color_in):
		hex_color = {'0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9',\
			'a':':', 'b':';', 'c':'<', 'd':'=', 'e':'>', 'f':'?', 'A':':', 'B':';', 'C':'<', 'D':'=', 'E':'>', 'F':'?'}
		color_out = '\c'
		for i in range(1, len(color_in)):
			color_out += hex_color.get(color_in[i])
		return color_out

	@cached
	def getText(self):
		string = ''
		for nim in nimmanager.nim_slots:
			if nim.type:
				if nim.slot is self.source.slot_number:
					string += self.workcolor
				elif self.source.tuner_mask & 1 << nim.slot:
					string += self.workcolor
				else:
					string += self.maincolor
				string += chr(ord("A") + nim.slot) + '  '
		return string

	text = property(getText)