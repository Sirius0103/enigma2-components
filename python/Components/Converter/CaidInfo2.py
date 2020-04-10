# CaidInfo2
# Coded by bigroma & 2boom
# v.1.5
# 
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
# 20.02.2020 add BulCrypt, Cryptoguard, Verimatrix, Rosscrypt mod by Sirius
# 05.03.2020 add DigiCipher, AlphaCrypt, OmniCrypt, CodiCrypt, X-Crypt, Panaccess mod by Sirius

from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Tools.Directories import fileExists
from Components.Element import cached
from Poll import Poll
import os

info = {}
old_ecm_mtime = None

class CaidInfo2(Poll, Converter, object):
	CAID = 0
	CAID2 = 1
	CRYPT = 2
	CRYPT2 = 3
	PID = 4
	PROV = 5
	HOST = 6
	DELAY = 7
	IS_CRD = 8
	CRDTXT = 9
	IS_NET = 10
	IS_EMU = 11
	IS_FTA = 12
	IS_CRYPTED = 13
	SECA = 14
	SECA_C = 15
	VIA = 16
	VIA_C = 17
	IRD = 18
	IRD_C =19
	DIGI = 20
	DIGI_C = 21
	NDS = 22
	NDS_C = 23
	CONAX = 24
	CONAX_C = 25
	CRW = 26
	CRW_C = 27
	PWR = 28
	PWR_C = 29
	TAN = 30
	TAN_C = 31
	BETA = 32
	BETA_C = 33
	NAGRA = 34
	NAGRA_C = 35
	CODI = 36
	CODI_C = 37
	BISS = 38
	BISS_C = 39
	EXS = 40
	EXS_C = 41
	ACR = 42
	ACR_C = 43
	XCR = 44
	XCR_C = 45
	OCR = 46
	OCR_C = 47
	DRE = 48
	DRE_C = 49
	GUARD = 50
	GUARD_C = 51
	BUL = 52
	BUL_C = 53
	PANA = 54
	PANA_C = 55
	VRM = 56
	VRM_C = 57
	ROSS = 58
	ROSS_C = 59
	FORMAT = 60
	SHORT = 61
	ALL = 62
	my_interval = 1000

	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		if type == "CAID":
			self.type = self.CAID
		elif type == "CAID2":
			self.type = self.CAID2
		elif type == "PID":
			self.type = self.PID
		elif type == "ProvID":
			self.type = self.PROV
		elif type == "Delay":
			self.type = self.DELAY
		elif type == "Host":
			self.type = self.HOST
		elif type == "Net":
			self.type = self.IS_NET
		elif type == "Emu":
			self.type = self.IS_EMU
		elif type == "CryptInfo":
			self.type = self.CRYPT
		elif type == "CryptInfo2":
			self.type = self.CRYPT2
		elif type == "SecaCrypt":
			self.type = self.SECA
		elif type == "SecaEcm":
			self.type = self.SECA_C
		elif type == "ViaCrypt":
			self.type = self.VIA
		elif type == "ViaEcm":
			self.type = self.VIA_C
		elif type == "IrdCrypt":
			self.type = self.IRD
		elif type == "IrdEcm":
			self.type = self.IRD_C
		elif type == "DigiCrypt":
			self.type = self.DIGI
		elif type == "DigiEcm":
			self.type = self.DIGI_C
		elif type == "NdsCrypt":
			self.type = self.NDS
		elif type == "NdsEcm":
			self.type = self.NDS_C
		elif type == "ConaxCrypt":
			self.type = self.CONAX
		elif type == "ConaxEcm":
			self.type = self.CONAX_C
		elif type == "CrwCrypt":
			self.type = self.CRW
		elif type == "CrwEcm":
			self.type = self.CRW_C
		elif type == "PwuCrypt":
			self.type = self.PWR
		elif type == "PwuEcm":
			self.type = self.PWR_C
		elif type == "TanCrypt":
			self.type = self.TAN
		elif type == "TanEcm":
			self.type = self.TAN_C
		elif type == "BetaCrypt":
			self.type = self.BETA
		elif type == "BetaEcm":
			self.type = self.BETA_C
		elif type == "NagraCrypt":
			self.type = self.NAGRA
		elif type == "NagraEcm":
			self.type = self.NAGRA_C
		elif type == "CodiCrypt":
			self.type = self.CODI
		elif type == "CodiEcm":
			self.type = self.CODI_C
		elif type == "BisCrypt":
			self.type = self.BISS
		elif type == "BisEcm":
			self.type = self.BISS_C
		elif type == "ExsCrypt":
			self.type = self.EXS
		elif type == "ExsEcm":
			self.type = self.EXS_C
		elif type == "AcrCrypt":
			self.type = self.ACR
		elif type == "AcrEcm":
			self.type = self.ACR_C
		elif type == "XcrCrypt":
			self.type = self.XCR
		elif type == "XcrEcm":
			self.type = self.XCR_C
		elif type == "OcrCrypt":
			self.type = self.OCR
		elif type == "OcrEcm":
			self.type = self.OCR_C
		elif type == "DreamCrypt":
			self.type = self.DRE
		elif type == "DreamEcm":
			self.type = self.DRE_C
		elif type == "GuardCrypt":
			self.type = self.GUARD
		elif type == "GuardEcm":
			self.type = self.GUARD_C
		elif type == "BulCrypt":
			self.type = self.BUL
		elif type == "BulEcm":
			self.type = self.BUL_C
		elif type == "PanaCrypt":
			self.type = self.PANA
		elif type == "PanaEcm":
			self.type = self.PANA_C
		elif type == "VrmCrypt":
			self.type = self.VRM
		elif type == "VrmEcm":
			self.type = self.VRM_C
		elif type == "RossCrypt":
			self.type = self.ROSS
		elif type == "RossEcm":
			self.type = self.ROSS_C
		elif type == "Crd":
			self.type = self.IS_CRD
		elif type == "CrdTxt":
			self.type = self.CRDTXT
		elif  type == "IsFta":
			self.type = self.IS_FTA
		elif  type == "IsCrypted":
			self.type = self.IS_CRYPTED
		elif type == "Short":
			self.type = self.SHORT
		elif type == "Default" or type == "" or type == None or type == "%":
			self.type = self.ALL
		else:
			self.type = self.FORMAT
			self.sfmt = type[:]

#		self.systemCaids = {
#			"01" : "Mediaguard",
#			"05" : "Viaccess",
#			"06" : "Irdeto",
#			"09" : "Videoguard",
#			"0B" : "Conax",
#			"0D" : "Cryptoworks",
#			"17" : "BetaCrypt",
#			"18" : "Nagravision"}

		self.systemTxtCaids_a = {
			"01" : "Mediaguard",
			"05" : "Viaccess",
			"06" : "Irdeto",
			"07" : "DigiCipher",
			"09" : "Videoguard",
			"0B" : "Conax",
			"0D" : "Cryptoworks",
			"0E" : "PowerVu",
			"10" : "Tandberg",
			"18" : "Nagravision",
			"22" : "CodiCrypt",
			"26" : "BiSS",
			"27" : "ExSet",
			"4B" : "Topvell",
			"54" : "Gospell",
			"55" : "BulCrypt",
			"56" : "Verimatrix",
			"7B" : "DRE-Crypt",
			"A1" : "RossCrypt"}

		self.systemTxtCaids_b = {
			"02" : "BetaCrypt",
			"22" : "BetaCrypt",
			"62" : "BetaCrypt",
			"20" : "AlphaCrypt",
			"BF" : "Skypilot",
			"D0" : "X-Crypt",
			"D1" : "X-Crypt",
			"D4" : "OmniCrypt",
			"E0" : "DRE-Crypt",
			"E1" : "DRE-Crypt",
			"60" : "SkyCrypt",
			"61" : "SkyCrypt",
			"63" : "SkyCrypt",
			"70" : "DreamCrypt",
			"EA" : "Cryptoguard",
			"EE" : "BulCrypt",
			"FC" : "Panaccess"}

	@cached
	def getBoolean(self):

		service = self.source.service
		info = service and service.info()
		if not info:
			return False
		caids = info.getInfoObject(iServiceInformation.sCAIDs)
		if self.type is self.IS_FTA:
			if caids:
				return False
			return True
		if self.type is self.IS_CRYPTED:
			if caids:
				return True
			return False
		if caids:
			if self.type == self.SECA:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '01':
						return True
				return False
			if self.type == self.VIA:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '05':
						return True
				return False
			if self.type == self.IRD:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '06':
						return True
				return False
			if self.type == self.DIGI:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '07':
						return True
				return False
			if self.type == self.NDS:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '09':
						return True
				return False
			if self.type == self.CONAX:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '0B':
						return True
				return False
			if self.type == self.CRW:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '0D':
						return True
				return False
			if self.type == self.PWR:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '0E':
						return True
				return False
			if self.type == self.TAN:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '10':
						return True
				return False
			if self.type == self.BETA:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '17' and ("%0.4X" % int(caid))[2:] == '02'\
						or ("%0.4X" % int(caid))[:2] == '17' and ("%0.4X" % int(caid))[2:] == '22'\
						or ("%0.4X" % int(caid))[:2] == '17' and ("%0.4X" % int(caid))[2:] == '62':
						return True
				return False
			if self.type == self.NAGRA:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '18':
						return True
				return False
			if self.type == self.CODI:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '22':
						return True
				return False
			if self.type == self.BISS:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '26':
						return True
				return False
			if self.type == self.EXS:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '27':
						return True
				return False
			if self.type == self.ACR:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '4A' and ("%0.4X" % int(caid))[2:] == '20':
						return True
				return False
			if self.type == self.XCR:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '4A' and ("%0.4X" % int(caid))[2:] == 'D0'\
						or ("%0.4X" % int(caid))[:2] == '4A' and ("%0.4X" % int(caid))[2:] == 'D1':
						return True
				return False
			if self.type == self.OCR:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '4A' and ("%0.4X" % int(caid))[2:] == 'D4':
						return True
				return False
			if self.type == self.DRE:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '7B' and ("%0.4X" % int(caid))[2:] == 'E1'\
						or ("%0.4X" % int(caid))[:2] == '4A' and ("%0.4X" % int(caid))[2:] == 'E0'\
						or ("%0.4X" % int(caid))[:2] == '4A' and ("%0.4X" % int(caid))[2:] == 'E1'\
						or ("%0.4X" % int(caid))[:2] == '4A' and ("%0.4X" % int(caid))[2:] == '70':
						return True
				return False
			if self.type == self.GUARD:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '4A' and ("%0.4X" % int(caid))[2:] == 'EA':
						return True
				return False
			if self.type == self.BUL:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '55'\
						or ("%0.4X" % int(caid))[:2] == '4A' and ("%0.4X" % int(caid))[2:] == 'EE':
						return True
				return False
			if self.type == self.PANA:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '4A' and ("%0.4X" % int(caid))[2:] == 'FC':
						return True
				return False
			if self.type == self.VRM:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == '56'\
						or ("%0.4X" % int(caid))[:2] == '17' and not ("%0.4X" % int(caid))[2:] == '02'\
						or ("%0.4X" % int(caid))[:2] == '17' and not ("%0.4X" % int(caid))[2:] == '22'\
						or ("%0.4X" % int(caid))[:2] == '17' and not ("%0.4X" % int(caid))[2:] == '62':
						return True
				return False
			if self.type == self.ROSS:
				for caid in caids:
					if ("%0.4X" % int(caid))[:2] == 'A1':
						return True
				return False
			self.poll_interval = self.my_interval
			self.poll_enabled = True
			ecm_info = self.ecmfile()
			if ecm_info:
				caid_a = ("%0.4X" % int(ecm_info.get("caid", ""),16))[:2]
				caid_b = ("%0.4X" % int(ecm_info.get("caid", ""),16))[2:]
				if self.type == self.SECA_C:
					if caid_a == '01':
						return True
					return False
				if self.type == self.VIA_C:
					if caid_a == '05':
						return True
					return False
				if self.type == self.IRD_C:
					if caid_a == '06':
						return True
					return False
				if self.type == self.DIGI_C:
					if caid_a == '07':
						return True
					return False
				if self.type == self.NDS_C:
					if caid_a == '09':
						return True
					return False
				if self.type == self.CONAX_C:
					if caid_a == '0B':
						return True
					return False
				if self.type == self.CRW_C:
					if caid_a == '0D':
						return True
					return False
				if self.type == self.PWR_C:
					if caid_a == '0E':
						return True
					return False
				if self.type == self.TAN_C:
					if caid_a == '10':
						return True
					return False
				if self.type == self.BETA_C:
					if caid_a == '17' and caid_b == '02'\
						or caid_a == '17' and caid_b == '22'\
						or caid_a == '17' and caid_b == '62':
						return True
					return False
				if self.type == self.NAGRA_C:
					if caid_a == '18':
						return True
					return False
				if self.type == self.CODI_C:
					if caid_a == '22':
						return True
					return False
				if self.type == self.BISS_C:
					if caid_a == '26':
						return True
					return False
				if self.type == self.EXS_C:
					if caid_a == '27':
						return True
					return False
				if self.type == self.ACR_C:
					if caid_a == '4A' and caid_b == '20':
						return True
					return False
				if self.type == self.XCR_C:
					if caid_a == '4A' and caid_b == 'D0'\
						or caid_a == '4A' and caid_b == 'D1':
						return True
					return False
				if self.type == self.OCR_C:
					if caid_a == '4A' and caid_b == 'D4':
						return True
					return False
				if self.type == self.DRE_C:
					if caid_a == '7B' and caid_b == 'E1'\
						or caid_a == '4A' and caid_b == 'E0'\
						or caid_a == '4A' and caid_b == 'E1'\
						or caid_a == '4A' and caid_b == '70':
						return True
					return False
				if self.type == self.GUARD_C:
					if caid_a == '4A' and caid_b == 'EA':
						return True
					return False
				if self.type == self.BUL_C:
					if caid_a == '55'\
						or caid_a == '4A' and caid_b == 'EE':
						return True
					return False
				if self.type == self.PANA_C:
					if caid_a == '4A' and caid_b == 'FC':
						return True
					return False
				if self.type == self.VRM_C:
					if caid_a == '56'\
						or caid_a == '17' and not caid_b == '02'\
						or caid_a == '17' and not caid_b == '22'\
						or caid_a == '17' and not caid_b == '62':
						return True
					return False
				if self.type == self.ROSS_C:
					if caid_a == 'A1':
						return True
					return False
				# oscam
				reader = ecm_info.get("reader", None)
				# cccam
				using = ecm_info.get("using", "")
				# mgcamd
				source = ecm_info.get("source", "")
				if self.type == self.IS_CRD:
				# oscam
					if source == 'sci':
						return True
				# wicardd
					if source != 'cache' and source != 'net' and source.find('emu') == -1:
						return True
					return False
				source = ecm_info.get("source", "")
				if self.type == self.IS_EMU:
					return using == 'emu' or source == 'emu' or source == 'card' or reader == 'emu' or source.find('card') > -1 or source.find('emu') > -1 or source.find('biss') > -1 or source.find('cache') > -1
				source = ecm_info.get("source", "")
				if self.type == self.IS_NET:
					if using == 'CCcam':
						return 1
					else:
						if source != 'cache' and source == 'net' and source.find('emu') == -1:
							return True
				else:
					return False
		return False

	boolean = property(getBoolean)

	@cached
	def getText(self):
		textvalue = ''
		server = ''
		service = self.source.service
		if service:
			ecm_info = self.ecmfile()
			info = service and service.info()
			self.poll_interval = self.my_interval
			self.poll_enabled = True
			if info:
				if self.type == self.CAID2:
					if info.getInfoObject(iServiceInformation.sCAIDs):
				# caid
						value = info.getInfo(iServiceInformation.sCAIDs)
						if value == -3:
							caids = info.getInfoObject(iServiceInformation.sCAIDs)
							if caids and len(caids) > 0:
								caid_s = ""
								for caid in caids:
									caid_s += ("%0.4X " % int(caid))
								return "%s" % caid_s
							else:
								return ""
					else:
						return "fta"
				if self.type == self.CRYPT2:
					if info.getInfoObject(iServiceInformation.sCAIDs):
				# crypt
						if fileExists("/tmp/ecm.info"):
							try:
								caid_a = ("%0.4X" % int(ecm_info.get("caid", ""),16))[:2]
								caid_b = ("%0.4X" % int(ecm_info.get("caid", ""),16))[2:]
								if caid_a == '4A':
									return "%s" % self.systemTxtCaids_b.get(caid_b)
								elif caid_a == '17' and caid_b == '02' or caid_a == '17' and caid_b == '22' or caid_a == '17' and caid_b == '62':
									return "BetaCrypt"
								elif caid_a == '17' and not caid_b == '02' or caid_a == '17' and not caid_b == '22' or caid_a == '17' and not caid_b == '62':
									return "Verimatrix"
								return "%s" % self.systemTxtCaids_a.get(caid_a)
							except:
								return "nondecode"
						else:
							return "nondecode"
					else:
						return "fta"
			if info:
				if info.getInfoObject(iServiceInformation.sCAIDs):
					if ecm_info:
				# caid
						caid = "%0.4X" % int(ecm_info.get("caid", ""),16)
						if self.type == self.CAID:
							return caid
				# crypt
						if self.type == self.CRYPT:
							caid_a = ("%0.4X" % int(ecm_info.get("caid", ""),16))[:2]
							caid_b = ("%0.4X" % int(ecm_info.get("caid", ""),16))[2:]
							if caid_a == '4A':
								return "%s" % self.systemTxtCaids_b.get(caid_b).upper()
							elif caid_a == '17' and caid_b == '02' or caid_a == '17' and caid_b == '22' or caid_a == '17' and caid_b == '62':
								return "BETACRYPT"
							elif caid_a == '17' and not caid_b == '02' or caid_a == '17' and not caid_b == '22' or caid_a == '17' and not caid_b == '62':
								return "VERIMATRIX"
							return "%s" % self.systemTxtCaids_a.get(caid_a).upper()
				# pid
						try:
							pid = "%0.4X" % int(ecm_info.get("pid", ""),16)
						except:
							pid = ""
						if self.type == self.PID:
							return pid
				# oscam
						try:
							prov = "%0.6X" % int(ecm_info.get("prov", ""),16)
						except:
							prov = ecm_info.get("prov", "")
						if self.type == self.PROV:
							return prov
						if ecm_info.get("ecm time", "").find("msec") > -1:
							ecm_time = ecm_info.get("ecm time", "")
						else:
							ecm_time = ecm_info.get("ecm time", "").replace(".","").lstrip("0") + " msec"
						if self.type == self.DELAY:
							return ecm_time
				# protocol
						protocol = ecm_info.get("protocol", "")
				# port
						port = ecm_info.get("port", "")
				# source
						source = ecm_info.get("source", "")
				# server
						server = ecm_info.get("server", "")
				# hops
						hops = ecm_info.get("hops", "")
				# system
						system = ecm_info.get("system", "")
				# provider
						provider = ecm_info.get("provider", "")
				# reader
						reader = ecm_info.get("reader", "")
						if self.type == self.CRDTXT:
							info_card = 'False'
				# oscam
							if source == 'sci':
								info_card = 'True'
				# wicardd
							if source != 'cache' and source != 'net' and source.find('emu') == -1:
								info_card = 'True'
							return info_card
						if self.type == self.HOST:
							return server
						if self.type == self.FORMAT:
							textvalue = ''
							params = self.sfmt.split(" ")
							for param in params:
								if param != '':
									if param[0] != '%':
										textvalue+=param
				# server
									elif param == '%S':
										textvalue+=server
				# hops
									elif param == '%H':
										textvalue+=hops
				# system
									elif param == '%SY':
										textvalue+=system
				# provider
									elif param == '%PV':
										textvalue+=provider
				# port
									elif param == '%SP':
										textvalue+=port
				# protocol
									elif param == '%PR':
										textvalue+=protocol
				# caid
									elif param == '%C':
										textvalue+=caid
				# pid
									elif param == '%P':
										textvalue+=pid
				# prov
									elif param == '%p':
										textvalue+=prov
				# source
									elif param == '%O':
										textvalue+=source
				# reader
									elif param == '%R':
										textvalue+=reader
				# ecm time
									elif param == '%T':
										textvalue+=ecm_time
									elif param == '%t':
										textvalue+="\t"
									elif param == '%n':
										textvalue+="\n"
									elif param[1:].isdigit():
										textvalue=textvalue.ljust(len(textvalue)+int(param[1:]))
									if len(textvalue) > 0:
										if textvalue[-1] != "\t" and textvalue[-1] != "\n":
											textvalue+=" "
							return textvalue[:-1]
						if self.type == self.ALL:
							if source == 'emu':
								textvalue = "%s - %s (Prov: %s, Caid: %s)" % (source, self.systemTxtCaids_a.get(caid[:2]), prov, caid)
				# new oscam ecm.info with port parametr
							elif reader != '' and source == 'net' and port != '':
								textvalue = "%s - Prov: %s, Caid: %s, Reader: %s, %s (%s:%s) - %s" % (source, prov, caid, reader, protocol, server, port, ecm_time.replace('msec','ms'))
							elif reader != '' and source == 'net': 
								textvalue = "%s - Prov: %s, Caid: %s, Reader: %s, %s (%s) - %s" % (source, prov, caid, reader, protocol, server, ecm_time.replace('msec','ms'))
							elif reader != '' and source != 'net': 
								textvalue = "%s - Prov: %s, Caid: %s, Reader: %s, %s (local) - %s" % (source, prov, caid, reader, protocol, ecm_time.replace('msec','ms'))
							elif server == '' and port == '' and protocol != '':
								textvalue = "%s - Prov: %s, Caid: %s, %s - %s" % (source, prov, caid, protocol, ecm_time.replace('msec','ms'))
							elif server == '' and port == '' and protocol == '':
								textvalue = "%s - Prov: %s, Caid: %s - %s" % (source, prov, caid, ecm_time.replace('msec','ms'))
							else:
								try:
									textvalue = "%s - Prov: %s, Caid: %s, %s (%s:%s) - %s" % (source, prov, caid, protocol, server, port, ecm_time.replace('msec','ms'))
								except:
									pass
						if self.type == self.SHORT:
							if source == 'emu':
								textvalue = "%s - %s (Prov: %s, Caid: %s)" % (source, self.systemTxtCaids_a.get(caid[:2]), prov, caid)
							elif server == '' and port == '':
								textvalue = "%s - Prov: %s, Caid: %s - %s" % (source, prov, caid, ecm_time.replace('msec','ms'))
							else:
								try:
									textvalue = "%s - Prov: %s, Caid: %s, %s:%s - %s" % (source, prov, caid, server, port, ecm_time.replace('msec','ms'))
								except:
									pass
					else:
						if self.type == self.ALL or self.type == self.SHORT or (self.type == self.FORMAT and (self.sfmt.count("%") > 3 )):
							textvalue = _("No parse cannot emu")
				else:
					if self.type == self.ALL or self.type == self.SHORT or (self.type == self.FORMAT and (self.sfmt.count("%") > 3 )):
						textvalue = _("Free-to-air")
		return textvalue

	text = property(getText)

	def ecmfile(self):
		global info
		global old_ecm_mtime
		ecm = None
		service = self.source.service
		if service:
			try:
				ecm_mtime = os.stat("/tmp/ecm.info").st_mtime
				if not os.stat("/tmp/ecm.info").st_size > 0:
					info = {}
				if ecm_mtime == old_ecm_mtime:
					return info
				old_ecm_mtime = ecm_mtime
				ecmf = open("/tmp/ecm.info", "rb")
				ecm = ecmf.readlines()
			except:
				old_ecm_mtime = None
				info = {}
				return info

			if ecm:
				for line in ecm:
					x = line.lower().find("msec")
				# ecm time for mgcamd and oscam
					if x != -1:
						info['ecm time'] = line[0:x+4]
					else:
						item = line.split(":", 1)
						if len(item) > 1:
				# wicard block
							if item[0] == 'Provider':
								item[0] = 'prov'
								item[1] = item[1].strip()[2:]
							elif item[0] == 'ECM PID':
								item[0] = 'pid'
							elif item[0] == 'response time':
								info['source'] = "net"
								it_tmp = item[1].strip().split(" ")
								info['ecm time'] = "%s msec" % it_tmp[0]
								info['reader'] = it_tmp[-1].strip("R0[").strip("]")
								y = it_tmp[-1].find("[")
								if y !=-1:
									info['server'] = it_tmp[-1][:y]
									info['protocol'] = it_tmp[-1][y+1:-1]
								y = it_tmp[-1].find("(")
								if y !=-1:
									info['server'] = it_tmp[-1].split("(")[-1].split(":")[0]
									info['port'] = it_tmp[-1].split("(")[-1].split(":")[-1].rstrip(")")
									info['reader'] = it_tmp[-2]
								elif y == -1:
									item[0] = 'source'
									item[1] = 'sci'
								if it_tmp[-1].find("emu") >-1 or it_tmp[-1].find("EMU") >-1 or it_tmp[-1].find("cache") > -1 or it_tmp[-1].find("card") > -1 or it_tmp[-1].find("biss") > -1:
									item[0] = 'source'
									item[1] = 'emu'
							elif item[0] == 'hops':
								item[1] = item[1].strip("\n")
							elif item[0] == 'system':
								item[1] = item[1].strip("\n")
							elif item[0] == 'provider':
								item[1] = item[1].strip("\n")
							elif item[0][:2] == 'cw'or item[0] =='ChID' or item[0] == 'Service':
								pass
				# mgcamd new_oscam block
							elif item[0] == 'source':
								if item[1].strip()[:3] == 'net':
									it_tmp = item[1].strip().split(" ")
									info['protocol'] = it_tmp[1][1:]
									info['server'] = it_tmp[-1].split(":",1)[0]
									info['port'] = it_tmp[-1].split(":",1)[1][:-1]
									item[1] = 'net'
							elif item[0] == 'prov':
								y = item[1].find(",")
								if y != -1:
									item[1] = item[1][:y]
				# old oscam block
							elif item[0] == 'reader':
								if item[1].strip() == 'emu':
									item[0] = 'source'
							elif item[0] == 'from':
								if item[1].strip() == 'local':
									item[1] = 'sci'
									item[0] = 'source'
								else:
									info['source'] = 'net'
									item[0] = 'server'
				# cccam block
							elif item[0] == 'provid':
								item[0] = 'prov'
							elif item[0] == 'using':
								if item[1].strip() == 'emu' or item[1].strip() == 'sci':
									item[0] = 'source'
								else:
									info['source'] = 'net'
									item[0] = 'protocol'
							elif item[0] == 'address':
								tt = item[1].find(":")
								if tt != -1:
									info['server'] = item[1][:tt].strip()
									item[0] = 'port'
									item[1] = item[1][tt+1:]
							info[item[0].strip().lower()] = item[1].strip()
						else:
							if not info.has_key('caid'):
								x = line.lower().find('caid')
								if x != -1:
									y = line.find(",")
									if y != -1:
										info['caid'] = line[x+5:y]
							if not info.has_key('pid'):
								x = line.lower().find('pid')
								if x != -1:
									y = line.find(" =")
									z = line.find(" *")
									if y != -1:
										info['pid'] = line[x+4:y]
									elif z != -1:
										info['pid'] = line[x+4:z]
				ecmf.close()
		return info

	def changed(self, what):
		Converter.changed(self, (self.CHANGED_POLL,))
