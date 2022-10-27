# EcmInfoLine Converter
# Copyright (c) 2boom 2014-22
# v.0.9-r5
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
# 01.01.2022 - seprate ip stream vs fta broadcast
# 06.05.2022 - add HDMI-In detect
# 28.05.2022 - py3 fix

from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Converter.Poll import Poll
import time
import os

class EcmInfoLine(Poll, Converter, object):
	Auto = 0
	PreDefine = 1
	Format = 2
	Crypt = 3
	EMU = 4
	NET = 5
	SCI = 6
	FTA = 7

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == 'Auto':
			self.type = self.Auto
		elif type.startswith('Format:'):
			self.type = self.Format
			self.paramert_str = type
		elif type == 'Crypt':
			self.type = self.Crypt
		elif type == 'EMU':
			self.type = self.EMU
		elif type == 'NET':
			self.type = self.NET
		elif type == 'SCI':
			self.type = self.SCI
		elif type == 'FTA':
			self.type = self.FTA
		else:
			self.type = self.PreDefine
		self.poll_interval = 1000
		self.poll_enabled = True
		self.TxtCaids = {
			"26" : "BiSS",
			"01" : "Seca-Mediaguard",
			"06" : "Irdeto",
			"17" : "BetaCrypt",
			"05" : "Viacces",
			"18" : "Nagravision",
			"09" : "NDS-Videoguard",
			"0B" : "Conax",
			"0D" : "Cryptoworks",
			#"4A" : "DRECrypt",
			"27" : "ExSet",
			"0E" : "PowerVu",
			"22" : "Codicrypt",
			"07" : "DigiCipher",
			"55" : "BulCrypt",
			"56" : "Verimatrix",
			"7B" : "DRECrypt",
			"A1" : "Rosscrypt",
			"0E" : "PowerVu"
			}
		self.txt_dre_caids = {
			'E0':'DRECrypt',
			'E1':'DRECrypt',
			'EE':'BulCrypt',
			'D0':'XCrypt',
			'D1':'XCrypt',
			'70':'DreamCrypt',
			'EA':'CryptoGuard',
			'20':'AlphaCrypt'
			}
		self.out_data = {'caid':'', 'prov':'', 'time':'', 'using':'', 'protocol':'', 'reader':'', 'port':'', 'source':'', 'hops':''}
		self.caid_data = self.ecm_time = self.prov_data = self.using_data = self.port_data = self.protocol_data = self.reader_data = self.hops_data = self.display_data = ''

	def	get_ecm_data(self):
		self.out_data = {'caid':'', 'prov':'', 'time':'', 'using':'', 'protocol':'', 'reader':'', 'port':'', 'source':'', 'hops':''}
		self.caid_data = self.ecm_time = self.prov_data = self.using_data = self.port_data = self.protocol_data = self.reader_data = self.hops_data = self.display_data = ''
		if os.path.isfile('/tmp/ecm.info'):
			try:
				filedata = open('/tmp/ecm.info')
			except:
				filedata = False
			if filedata:
				for line in filedata.readlines():
				##### get caid
					if "caid:" in line:
						self.caid_data = line.strip("\n").split()[-1][2:].zfill(4)
					elif "CaID" in line or "CAID" in line:
						self.caid_data = line.split(',')[0].split()[-1][2:]
					if not self.caid_data == '':
						self.out_data['caid'] = self.caid_data.upper()
					##### get reader
					if 'reader:' in line:
						self.reader_data = line.split()[-1]
					elif 'response time:' in line and ' decode' in line and not '(' in line:
						self.reader_data = line.split()[-1]
						if 'R' and '[' and ']' in self.reader_data:
							self.reader_data = 'emu'
					elif 'response time:' in line and ' decode' in line and '(' in line:
						self.reader_data = line.split('(')[0].split()[-1]
					if not self.reader_data == '':
						self.out_data['reader'] = self.reader_data
					##### get port
					if 'port:' in line:
						self.port_data = line.split()[-1]
					if not self.port_data == '':
						self.out_data['port'] = ':%s' % self.port_data
					##### get prov
					if 'provid:' in line or 'PROVIDER' in line:
						self.prov_data = line.split()[-1].replace('0x', '').zfill(6)
						#self.prov_data = prov_mask[len(self.prov_data):] + self.prov_data
					elif ('prov:' in line or 'Provider:' in line) and 'pkey:' not in line:
						self.prov_data = line.split()[-1].replace('0x', '')
					elif 'prov:' in line and 'pkey:' in line:
						self.prov_data = line.split(',')[0].split()[-1]
					if not self.prov_data == '':
						self.out_data['prov'] = self.prov_data
					##### get ecm time
					if 'ecm time:' in line:
						self.ecm_time = line.split()[-1].replace('.', '').lstrip('0')
					elif 'msec' in line:
						self.ecm_time = line.split()[0]
					elif 'response time:' in line:
						self.ecm_time = line.split()[2]
					if not self.ecm_time == '':
						self.out_data['time'] = self.ecm_time
					if 'hops:' in line:
						self.hops_data = line.split()[-1]
					if not self.hops_data == '':
						self.out_data['hops'] = self.hops_data
					###### get using
					if 'address:' in line or 'from:' in line.lower():
						self.using_data =  line.split()[-1].split('/')[-1]
					elif 'source:' in line and 'card' in line:
						self.using_data =  line.split()[-1].strip('(').strip(')')
					elif 'source:' in line and 'net' in line:
						self.using_data =  line.split()[-1].strip('(').strip(')')
					elif 'using:' in line and 'at' in line:
						self.using_data = line.split()[-1].strip(')')
					elif 'using:' in line and 'at' not in line:
						self.using_data = line.split()[-1].strip('(').strip(')')
					elif 'response time:' in line and ' decode' in line and '(' in line:
						self.using_data = line.split()[-1].strip('(').strip(')')
					if not self.using_data == '':
						self.out_data['using'] = self.using_data
					###### get protocol
					if 'protocol:' in line:
						self.protocol_data =  line.split()[-1]
					elif 'source:' in line and 'net' in line:
						self.protocol_data = line.split()[-3].strip('(').strip(')')
					elif 'using:' in line and 'at' in line:
						self.protocol_data = line.split('at')[0].split()[-1].strip('(').strip(')')
					if not self.protocol_data == '':
						self.out_data['protocol'] = self.protocol_data
					#### get source
					if 'emu' in line:
						self.out_data['source'] = 'emu'
					elif 'response time:' in line and 'by EMU' in line:
						self.out_data['source'] = 'emu'
					elif 'response time:' in line and '[' in line and ']'in line:
						self.out_data['source'] = 'emu'
					elif 'response time:' in line and 'cache'in line:
						self.out_data['source'] = 'emu'
					elif 'source:' in line and 'card' in line and 'biss' in line:
						self.out_data['source'] = 'emu'
					elif 'protocol' in line and 'virtual' in line:
						self.out_data['source'] = 'emu'
					elif 'local' in line:
						self.out_data['source'] = 'sci'
					elif 'using:' in line and 'sci' in line:
						self.out_data['source'] = 'sci'
					elif 'source:' in line and 'card' in line and not 'biss' in line:
						self.out_data['source'] = 'sci'
					elif 'response time:' in line and not '(' in line and not ']'in line:
						self.out_data['source'] = 'sci'
					elif 'newcamd' in line or 'cs357x'  in line or 'cs378x'in line or 'camd35' in line:
						self.out_data['source'] = 'net'
					elif 'response time:' in line and '(' in line and ')'in line:
						self.out_data['source'] = 'net'
					elif 'using:' in line and 'CCcam' in line:
						self.out_data['source'] = 'net'
					elif 'CAID' in line and 'PID' in line and 'PROVIDER' in line:
						self.out_data['source'] = 'net'
					if not self.out_data['port'] == '':
						self.out_data['using'] = self.out_data['using'] + self.out_data['port']
				filedata.close()

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return ''
		# %C - caid, %P - Provider, %T - time, %U -using, %R - Reader, %S - source, %H - hops, %O - port, %L - Protocol
		iscrypt = info.getInfo(iServiceInformation.sIsCrypted)
		serref = info.getInfo(iServiceInformation.sSID)
		if self.type == self.Auto or self.type == self.Format or self.type == self.PreDefine:
			if serref == -1:
				return _('HDMI-in')	
			if not iscrypt or iscrypt == -1:
				if service.streamed() != None:
					return  _('Internet broadcasting')
				return _('Free-to-air')
			elif iscrypt and not os.path.isfile('/tmp/ecm.info'):
				return _('No parse cannot emu')
			elif iscrypt and os.path.isfile('/tmp/ecm.info'):
				try:
					if not os.stat('/tmp/ecm.info').st_size:
						return _('No parse cannot emu')
				except:
					return _('No parse cannot emu')

		if not self.out_data.get('source', '') == 'emu' and os.path.isfile('/tmp/ecm.info'):
			try:
				if int((time.time() - os.stat("/tmp/ecm.info").st_mtime)) > 14:
					return _('No parse cannot emu')
			except:
				return _('No parse cannot emu')
		self.get_ecm_data()
		if self.type == self.PreDefine:
			if self.out_data.get('source', '') == 'emu':
				if self.out_data.get('caid').startswith('4A'):
					return 'emu - %s (Prov: %s, Caid: %s)' % (self.txt_dre_caids.get(self.out_data.get('caid')[2:]),self.out_data.get('prov', ''), self.out_data.get('caid', ''))
				else:
					return 'emu - %s (Prov: %s, Caid: %s)' % (self.TxtCaids.get(self.out_data.get('caid')[:2]),self.out_data.get('prov', ''), self.out_data.get('caid', ''))
			if self.out_data.get('source', '') == 'sci':
				if not self.out_data.get('reader', '') == '':
					return '%s - Prov: %s, Caid: %s, Reader: %s - %s ms' %\
						(self.out_data.get('source', ''), self.out_data.get('prov', ''), self.out_data.get('caid', ''), self.out_data.get('reader', ''), self.out_data.get('time', ''))
				elif self.out_data.get('reader', '') == '':
					return '%s - Prov: %s, Caid: %s, Reader: %s - %s ms' %\
						(self.out_data.get('source', ''), self.out_data.get('prov', ''), self.out_data.get('caid', ''), self.out_data.get('using', ''), self.out_data.get('time', ''))

			elif self.out_data.get('source', '') == 'net':
				if not self.out_data.get('protocol', '') == '' and not self.out_data.get('time', '') == '':
					return ('%s - Prov: %s, Caid: %s, %s (%s) - %s ms') %\
						(self.out_data.get('source', ''),  self.out_data.get('prov', ''), self.out_data.get('caid', ''), self.out_data.get('protocol', ''), self.out_data.get('using', ''), self.out_data.get('time', ''))
				elif self.out_data.get('protocol', '') == '' and not self.out_data.get('time', '') == '':
					return ('%s - Prov: %s, Caid: %s (%s) - %s ms') %\
						(self.out_data.get('source'),  self.out_data.get('prov', ''), self.out_data.get('caid', ''), self.out_data.get('using', ''), self.out_data.get('time', ''))
				elif self.out_data.get('protocol', '') == '' and self.out_data.get('time', '') == '':
					return ('%s - Prov: %s, Caid: %s (%s)') %\
						(self.out_data.get('source', ''),  self.out_data.get('prov', ''), self.out_data.get('caid', ''), self.out_data.get('using', ''))

			for data in ('source', 'prov', 'caid', 'reader', 'protocol', 'using', 'hops', 'time'):
				if not self.out_data.get(data, '') == '':
					self.display_data += self.out_data.get(data, '') + '  '
			return self.display_data

		elif self.type == self.Auto:
			if not self.out_data.get('source', '') == '':
				self.display_data += self.out_data.get('source', '') + ' - '
			if not self.out_data.get('prov', '') == '':
				self.display_data += 'Prov: ' + self.out_data.get('prov', '') + ',  '
			if not self.out_data.get('caid', '') == '':
				self.display_data += 'Caid: ' + self.out_data.get('caid', '') + ',  '
			if not self.out_data.get('reader', '') == '':
				self.display_data += 'Reader: ' + self.out_data.get('reader', '') + ',  '
			if not self.out_data.get('protocol', '') == '':
				self.display_data += self.out_data.get('protocol', '') + '  '
			if not self.out_data.get('using', '') == '':
				self.display_data += '(' + self.out_data.get('using', '') + ')  '
			if not self.out_data.get('hops', '') == '':
				self.display_data += 'hops: ' + self.out_data.get('hops', '') + ' '
			if not self.out_data.get('time', '') == '':
				self.display_data += '- ' + self.out_data.get('time', '') + ' ms'
			return self.display_data

		elif self.type == self.Crypt:
			if self.out_data.get('caid', '') != '':
				if self.out_data.get('caid', '').startswith('4A'):
					return self.txt_dre_caids.get(self.out_data.get('caid')[2:], '')
				else:
					return self.TxtCaids.get(self.out_data.get('caid')[:2], '')
			else:
				return 'NONDECODE'

		elif self.type == self.Format:
			return self.paramert_str.replace('Format:', '').replace('%C', self.out_data.get('caid', '')).replace('%P', self.out_data.get('prov', '')).replace('%T', self.out_data.get('time', '')).replace('%U', self.out_data.get('using', ''))\
				.replace('%R', self.out_data.get('reader', '')).replace('%H', self.out_data.get('hops', '')).replace('%O', self.out_data.get('port', '')).replace('%L', self.out_data.get('protocol', '')).replace('%S', self.out_data.get('source', ''))

	text = property(getText)

	@cached
	def getBoolean(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return False
		if self.type == self.EMU or self.type == self.NET or self.type == self.SCI or self.type == self.FTA:
			self.get_ecm_data()
			if self.type == self.EMU:
				if self.out_data.get('source', '') == 'emu':
					return True
				return False
			elif self.type == self.NET:
				if self.out_data.get('source', '') == 'net':
					return True
				return False
			elif self.type == self.SCI:
				if self.out_data.get('source', '') == 'sci':
					return True
				return False
			elif self.type == self.FTA:
				iscrypt = info.getInfo(iServiceInformation.sIsCrypted)
				if not iscrypt or iscrypt == -1:
					return True
				return False
		else: 
			return False
			
	boolean = property(getBoolean)

	def changed(self, what):
		if what[0] == self.CHANGED_SPECIFIC:
			Converter.changed(self, what)
		elif what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)
