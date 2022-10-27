# TunerBar Converter
# Copyright (c) 2boom 2014-22
# v.0.3-r2
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
# 27.05.2022 py3 fix

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
		return '\c' + color_in.lower().replace('#','').replace('a',':').replace('b',';').replace('c','<').replace('d','=').replace('e','>').replace('f','?')

	@cached
	def getText(self):
		string = stringout = ''
		nimletter = []
		for nim in nimmanager.nim_slots:
			if nim.type:
				if nim.slot == self.source.slot_number:
					string += self.workcolor
				elif self.source.tuner_mask & 1 << nim.slot:
					string += self.workcolor
				else:
					string += self.maincolor
				string += chr(ord("A") + nim.slot) + '  '
		for letter in string.split():
			nimletter.append(letter)
		fbc = len(nimletter)/4
		for count in range(0, len(nimletter)):
			if count < fbc:
				stringout += nimletter[count] + '  '
			if count >= fbc * 4:
				stringout +=  nimletter[count] + '  '
		return stringout

	text = property(getText)