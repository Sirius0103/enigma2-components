# CaidBar Converter
# Copyright (c) 2boom 2014-16
# v.0.5
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
# 04.03.2020 add Short, Full mod by MegAndretH
# 05.03.2020 fix crypt mod by Sirius
# 27.10.2022 fix

from Components.Converter.Converter import Converter
from Components.Converter.Poll import Poll
from Components.Element import cached
from enigma import iServiceInformation
import os

class CaidBar(Poll, Converter, object):

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.caid_default = []
		self.type = type.split(',')
		self.maincolor = self.convert_color(self.type[0].strip())
		self.emmcolor = self.convert_color(self.type[1].strip())
		self.ecmcolor = self.convert_color(self.type[2].strip())
		if len(self.type) > 4:
			self.caid_default = self.type[-1].split()
		if len(self.type) == 3:
			self.caid_default = ['S', 'V', 'I', 'ND', 'CO', 'PV', 'N', 'EX', 'VM', 'BI']
			self.txt_caids_a = {
				'01' : 'S',
				'05' : 'V',
				'06' : 'I',
				'07' : 'DC',
				'09' : 'ND',
				'0B' : 'CO',
				'0D' : 'CW',
				'0E' : 'PV',
				'10' : 'TA',
				'18' : 'N',
				'22' : 'CC',
				'26' : 'BI',
				'27' : 'EX',
				'4B' : 'T',
				'54' : 'G',
				'55' : 'BC',
				'56' : 'VM',
				'7B' : 'D',
				'A1' : 'RC'}
			self.txt_caids_b = {
				'17' : 'VM'}
			self.txt_caids_c = {
				'02' : 'BE',
				'22' : 'BE',
				'62' : 'BE'}
			self.txt_caids_d = {
				'20' : 'AC',
				'BF' : 'SP',
				'D0' : 'XC',
				'D1' : 'XC',
				'D4' : 'OC',
				'E0' : 'D',
				'E1' : 'D',
				'60' : 'SC',
				'61' : 'SC',
				'63' : 'SC',
				'70' : 'DC',
				'EA' : 'CG',
				'EE' : 'BC',
				'FC' : 'P'}
		elif self.type[3].strip() == "Short":
			self.caid_default = ['SEC', 'VIA', 'IRD', 'NDS', 'CON', 'PVU', 'NAG', 'EXS', 'VRM', 'BiSS']
			self.txt_caids_a = {
				'01' : 'SEC',
				'05' : 'VIA',
				'06' : 'IRD',
				'07' : 'DIC',
				'09' : 'NDS',
				'0B' : 'CON',
				'0D' : 'CRW',
				'0E' : 'PVU',
				'10' : 'TAN',
				'18' : 'NAG',
				'22' : 'COD',
				'26' : 'BiSS',
				'27' : 'EXS',
				'4B' : 'TOP',
				'54' : 'GOS',
				'55' : 'BUL',
				'56' : 'VRM',
				'7B' : 'DRE',
				'A1' : 'ROS'}
			self.txt_caids_b = {
				'17' : 'VRM'}
			self.txt_caids_c = {
				'02' : 'BET',
				'22' : 'BET',
				'62' : 'BET'}
			self.txt_caids_d = {
				'20' : 'ACR',
				'BF' : 'SKY',
				'D0' : 'XCR',
				'D1' : 'XCR',
				'D4' : 'OCR',
				'E0' : 'DRE',
				'E1' : 'DRE',
				'60' : 'SCR',
				'61' : 'SCR',
				'63' : 'SCR',
				'70' : 'DCR',
				'EA' : 'CGU',
				'EE' : 'BUL',
				'FC' : 'PAN'}
		elif self.type[3].strip() == "Full":
			self.caid_default = ['SECA', 'VIACCESS', 'IRDETO', 'VIDEOGUARD', 'CONAX', 'POWERVU', 'NAGRAVISION', 'EXSET', 'VERIMATRIX', 'BiSS']
			self.txt_caids_a = {
				'01' : 'MEDIAGUARD',
				'05' : 'VIACCESS',
				'06' : 'IRDETO',
				'07' : 'DIGICIPHER',
				'09' : 'VIDEOGUARD',
				'0B' : 'CONAX',
				'0D' : 'CRYPTOWORKS',
				'0E' : 'POWERVU',
				'10' : 'TANDBERG',
				'18' : 'NAGRAVISION',
				'22' : 'CODICRYPT',
				'26' : 'BiSS',
				'27' : 'EXSET',
				'4B' : 'TOPVELL',
				'54' : 'GOSPELL',
				'55' : 'BULCRYPT',
				'56' : 'VERIMATRIX',
				'7B' : 'DRE-CRYPT',
				'A1' : 'ROSSCRYPT'}
			self.txt_caids_b = {
				'17' : 'VERIMATRIX'}
			self.txt_caids_c = {
				'02' : 'BETACRYPT',
				'22' : 'BETACRYPT',
				'62' : 'BETACRYPT'}
			self.txt_caids_d = {
				'20' : 'ALPHACRYPT',
				'BF' : 'SKYPILOT',
				'D0' : 'X-CRYPT',
				'D1' : 'X-CRYPT',
				'D4' : 'OMNICRYPT',
				'E0' : 'DRE-CRYPT',
				'E1' : 'DRE-CRYPT',
				'60' : 'SKYCRYPT',
				'61' : 'SKYCRYPT',
				'63' : 'SKYCRYPT',
				'70' : 'DREAMCRYPT',
				'EA' : 'CRYPTOGUARD',
				'EE' : 'BULCRYPT',
				'FC' : 'PANACCESS'}
		self.poll_interval = 1000
		self.poll_enabled = True

	def convert_color(self, color_in):
		hex_color = {'0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9',\
			'a':':', 'b':';', 'c':'<', 'd':'=', 'e':'>', 'f':'?', 'A':':', 'B':';', 'C':'<', 'D':'=', 'E':'>', 'F':'?'}
		color_out = '\c'
		for i in range(1, len(color_in)):
			color_out += hex_color.get(color_in[i])
		return color_out

	def getCaidInEcmFile(self):
		caidvalue = return_line = ""
		ecm_files = ["/tmp/ecm.info", "/tmp/ecm1.info"] # Tuner A,B
		for ecm_file in ecm_files:
			if os.path.exists(ecm_file):
				try:
					filedata = open(ecm_file)
				except:
					filedata = False
				if filedata:
					for line in filedata.readlines():
						if "caid:" in line:
							caidvalue = line.strip("\n").split()[-1][2:].zfill(4)
						elif "CaID" in line or "CAID" in line:
							caidvalue = line.split(',')[0].split()[-1][2:]
					if caidvalue.upper().startswith('4A'):
						return_line += " %s " % self.txt_caids_d.get(caidvalue[2:].upper(), " ")
					elif caidvalue.upper().startswith('17') and caidvalue.upper().startswith('02')\
						or caidvalue.upper().startswith('17') and caidvalue.upper().startswith('22')\
						or caidvalue.upper().startswith('17') and caidvalue.upper().startswith('62'):
						return_line += " %s " % self.txt_caids_c.get(caidvalue[2:].upper(), " ")
					elif caidvalue.upper().startswith('17') and not caidvalue.upper().startswith('02')\
						or caidvalue.upper().startswith('17') and not caidvalue.upper().startswith('22')\
						or caidvalue.upper().startswith('17') and not caidvalue.upper().startswith('62'):
						return_line += " %s " % self.txt_caids_b.get(caidvalue[:2].upper(), " ")
					else:
						return_line += " %s " % self.txt_caids_a.get(caidvalue[:2].upper(), " ")
					filedata.close()
		return return_line

	def getServiceInfoString(self, info, what):
		value = info.getInfo(what)
		if value == -3:
			line_caids = info.getInfoObject(what)
			if line_caids and len(line_caids) > 0:
				return_value = ""
				for caid in line_caids:
					return_value += "%0.4X " % caid
				return return_value[:-1]
			else:
				return ""
		return "%d" % value
		
	def addspaces(self, what):
		return " %s " % what

	@cached
	def getText(self):
		string = ecmcaid = line_caids = ""
		service = self.source.service
		info = service and service.info()
		self.caid_current = []
		if not info:
			for i in range(len(self.caid_default)):
				string += self.maincolor + self.caid_default[i] + " "
			return string
		caidinfo = self.getServiceInfoString(info, iServiceInformation.sCAIDs)
		if caidinfo:
			ecmcaid = self.getCaidInEcmFile()
		if ecmcaid != None:
			for caid in caidinfo.split():
				if caid.upper().startswith('4A'):
					if self.txt_caids_d.get(caid[2:]) not in self.caid_default:
						if self.txt_caids_d.get(caid[2:]) not in self.caid_current:
							self.caid_current.append(self.txt_caids_d.get(caid[2:]))
				elif caid.upper().startswith('17') and caid.upper().startswith('02')\
					or caid.upper().startswith('17') and caid.upper().startswith('22')\
					or caid.upper().startswith('17') and caid.upper().startswith('62'):
					if self.txt_caids_c.get(caid[2:]) not in self.caid_default:
						if self.txt_caids_c.get(caid[2:]) not in self.caid_current:
							self.caid_current.append(self.txt_caids_c.get(caid[2:]))
				elif caid.upper().startswith('17') and not caid.upper().startswith('02')\
					or caid.upper().startswith('17') and not caid.upper().startswith('22')\
					or caid.upper().startswith('17') and not caid.upper().startswith('62'):
					if self.txt_caids_b.get(caid[:2]) not in self.caid_default:
						if self.txt_caids_b.get(caid[:2]) not in self.caid_current:
							self.caid_current.append(self.txt_caids_b.get(caid[:2]))
				else:
					if self.txt_caids_a.get(caid[:2]) not in self.caid_default:
						if self.txt_caids_a.get(caid[:2]) not in self.caid_current:
							self.caid_current.append(self.txt_caids_a.get(caid[:2]))
				self.caid_current.sort()
				if caid.upper().startswith('4A'):
					line_caids += self.addspaces(self.txt_caids_d.get(caid[2:]))
				elif caid.upper().startswith('17') and caid.upper().startswith('02')\
					or caid.upper().startswith('17') and caid.upper().startswith('22')\
					or caid.upper().startswith('17') and caid.upper().startswith('62'):
					line_caids += self.addspaces(self.txt_caids_c.get(caid[2:]))
				elif caid.upper().startswith('17') and not caid.upper().startswith('02')\
					or caid.upper().startswith('17') and not caid.upper().startswith('22')\
					or caid.upper().startswith('17') and not caid.upper().startswith('62'):
					line_caids +=  self.addspaces(self.txt_caids_b.get(caid[:2]))
				else:
					line_caids += self.addspaces(self.txt_caids_a.get(caid[:2]))
			for i in range(len(self.caid_default)):
				if self.addspaces(self.caid_default[i]) in ecmcaid:
					string += self.ecmcolor
				elif self.addspaces(self.caid_default[i]) in line_caids:
					string += self.emmcolor
				else:
					string += self.maincolor
				string += self.caid_default[i] + " "
			for i in range(len(self.caid_current)):
				if self.caid_current[i] != None:
					if self.addspaces(self.caid_current[i]) in ecmcaid:
						string += self.ecmcolor
					elif self.addspaces(self.caid_current[i]) in line_caids:
						string += self.emmcolor
					string += self.caid_current[i] + " "
				else:
					string += self.emmcolor + "UNKNOWN" + " "
			return string.strip()

	text = property(getText)

	def changed(self, what):
		if what[0] == self.CHANGED_SPECIFIC:
			Converter.changed(self, what)
		elif what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)
