# FlashingDotClock Converter
# Copyright (c) 2boom 2015
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

from Components.Converter.Converter import Converter
from Components.Element import cached
from datetime import datetime

class FlashingDotClock(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)

	@cached

	def getText(self):
		dt = datetime.today()
		if dt.second % 2 is 0:
			return dt.strftime('%H:%M')
		else:
			return dt.strftime('%H.%M')

	text = property(getText)

