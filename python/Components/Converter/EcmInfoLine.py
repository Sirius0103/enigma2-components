# EcmInfoLine Converter
# Copyright (c) 2boom 2014-16
# v.0.6-r4
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

from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.Element import cached
from Poll import Poll
import time
import os

class EcmInfoLine(Poll, Converter, object):
	Auto = 0
	PreDefine = 1
	Format = 2
	Crypt = 3

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
			"4A" : "DRE-Crypt",
			"27" : "ExSet",
			"0E" : "PowerVu",
			"22" : "Codicrypt",
			"07" : "DigiCipher",
			"56" : "Verimatrix",
			"7B" : "DRE-Crypt",
			"A1" : "Rosscrypt",
			"0E" : "PowerVu"
			}

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return ''
		# %C - caid, %P - Provider, %T - time, %U -using, %R - Reader, %S - source, %H - hops, %O - port, %L - Protocol
		out_data = {'caid':'', 'prov':'', 'time':'', 'using':'', 'protocol':'', 'reader':'', 'port':'', 'source':'', 'hops':''}
		caid_data = ecm_time = prov_data = using_data = port_data = protocol_data = reader_data = hops_data = display_data = ''
		iscrypt = info.getInfo(iServiceInformation.sIsCrypted)
		if self.type is self.Auto or self.type is self.Format or self.type is self.PreDefine:
			if not iscrypt or iscrypt == -1:
				return _('Free-to-air')
			elif iscrypt and not os.path.isfile('/tmp/ecm.info'):
				return _('No parse cannot emu')
			elif iscrypt and os.path.isfile('/tmp/ecm.info'):
				try:
					if not os.stat('/tmp/ecm.info').st_size:
						return _('No parse cannot emu')
				except:
					return _('No parse cannot emu')
		if os.path.isfile('/tmp/ecm.info'):
			try:
				filedata = open('/tmp/ecm.info')
			except:
				filedata = False
			if filedata:
				for line in filedata.readlines():
				##### get caid
					if "caid:" in line:
						caid_data = line.strip("\n").split()[-1][2:].zfill(4)
					elif "CaID" in line or "CAID" in line:
						caid_data = line.split(',')[0].split()[-1][2:]
					if not caid_data is '':
						out_data['caid'] = caid_data.upper()
					##### get reader
					if 'reader:' in line:
						reader_data = line.split()[-1]
					elif 'response time:' in line and ' decode' in line and not '(' in line:
						reader_data = line.split()[-1]
						if 'R' and '[' and ']' in reader_data:
							reader_data = 'emu'
					elif 'response time:' in line and ' decode' in line and '(' in line:
						reader_data = line.split('(')[0].split()[-1]
					if not reader_data is '':
						out_data['reader'] = reader_data
					##### get port
					if 'port:' in line:
						port_data = line.split()[-1]
					if not port_data is '':
						out_data['port'] = ':%s' % port_data
					##### get prov
					if 'provid:' in line or 'PROVIDER' in line:
						prov_data = line.split()[-1].replace('0x', '').zfill(6)
						#prov_data = prov_mask[len(prov_data):] + prov_data
					elif ('prov:' in line or 'Provider:' in line) and 'pkey:' not in line:
						prov_data = line.split()[-1].replace('0x', '')
					elif 'prov:' in line and 'pkey:' in line:
						prov_data = line.split(',')[0].split()[-1]
					if not prov_data is '':
						out_data['prov'] = prov_data
					##### get ecm time
					if 'ecm time:' in line:
						ecm_time = line.split()[-1].replace('.', '').lstrip('0')
					elif 'msec' in line:
						ecm_time = line.split()[0]
					elif 'response time:' in line:
						ecm_time = line.split()[2]
					if not ecm_time is '':
						out_data['time'] = ecm_time
					if 'hops:' in line:
						hops_data = line.split()[-1]
					if not hops_data is '':
						out_data['hops'] = hops_data
					###### get using
					if 'address:' in line or 'from:' in line.lower():
						using_data =  line.split()[-1].split('/')[-1]
					elif 'source:' in line and 'card' in line:
						using_data =  line.split()[-1].strip('(').strip(')')
					elif 'source:' in line and 'net' in line:
						using_data =  line.split()[-1].strip('(').strip(')')
					elif 'using:' in line and 'at' in line:
						using_data = line.split()[-1].strip(')')
					elif 'using:' in line and 'at' not in line:
						using_data = line.split()[-1].strip('(').strip(')')
					elif 'response time:' in line and ' decode' in line and '(' in line:
						using_data = line.split()[-1].strip('(').strip(')')
					if not using_data is '':
						out_data['using'] = using_data
					###### get protocol
					if 'protocol:' in line:
						protocol_data =  line.split()[-1]
					elif 'source:' in line and 'net' in line:
						protocol_data = line.split()[-3].strip('(').strip(')')
					elif 'using:' in line and 'at' in line:
						protocol_data = line.split('at')[0].split()[-1].strip('(').strip(')')
					if not protocol_data is '':
						out_data['protocol'] = protocol_data
					#### get source
					if 'emu' in line:
						out_data['source'] = 'emu'
					elif 'response time:' in line and 'by EMU' in line:
						out_data['source'] = 'emu'
					elif 'response time:' in line and '[' in line and ']'in line:
						out_data['source'] = 'emu'
					elif 'response time:' in line and 'cache'in line:
						out_data['source'] = 'emu'
					elif 'source:' in line and 'card' in line and 'biss' in line:
						out_data['source'] = 'emu'
					elif 'protocol' in line and 'virtual' in line:
						out_data['source'] = 'emu'
					elif 'local' in line:
						out_data['source'] = 'sci'
					elif 'using:' in line and 'sci' in line:
						out_data['source'] = 'sci'
					elif 'source:' in line and 'card' in line and not 'biss' in line:
						out_data['source'] = 'sci'
					elif 'response time:' in line and not '(' in line and not ']'in line:
						out_data['source'] = 'sci'
					elif 'newcamd' in line or 'cs357x'  in line or 'cs378x'in line or 'camd35' in line:
						out_data['source'] = 'net'
					elif 'response time:' in line and '(' in line and ')'in line:
						out_data['source'] = 'net'
					elif 'using:' in line and 'CCcam' in line:
						out_data['source'] = 'net'
					elif 'CAID' in line and 'PID' in line and 'PROVIDER' in line:
						out_data['source'] = 'net'
					if not out_data['port'] is '':
						out_data['using'] = out_data['using'] + out_data['port']
				filedata.close()

		if not out_data.get('source', '') is 'emu' and os.path.isfile('/tmp/ecm.info'):
			try:
				if int((time.time() - os.stat("/tmp/ecm.info").st_mtime)) > 14:
					return _('No parse cannot emu')
			except:
				return _('No parse cannot emu')

		if self.type is self.PreDefine:
			if out_data.get('source', '') is 'emu':
				return 'emu - %s (Prov: %s, Caid: %s)' % (self.TxtCaids.get(out_data.get('caid')[:2]),out_data.get('prov', ''), out_data.get('caid', ''))
			if out_data.get('source', '') is 'sci':
				if not out_data.get('reader', '') is '':
					return '%s - Prov: %s, Caid: %s, Reader: %s - %s ms' %\
						(out_data.get('source', ''), out_data.get('prov', ''), out_data.get('caid', ''), out_data.get('reader', ''), out_data.get('time', ''))
				elif out_data.get('reader', '') is '':
					return '%s - Prov: %s, Caid: %s, Reader: %s - %s ms' %\
						(out_data.get('source', ''), out_data.get('prov', ''), out_data.get('caid', ''), out_data.get('using', ''), out_data.get('time', ''))

			elif out_data.get('source', '') is 'net':
				if not out_data.get('protocol', '') is '' and not out_data.get('time', '') is '':
					return ('%s - Prov: %s, Caid: %s, %s (%s) - %s ms') %\
						(out_data.get('source', ''),  out_data.get('prov', ''), out_data.get('caid', ''), out_data.get('protocol', ''), out_data.get('using', ''), out_data.get('time', ''))
				elif out_data.get('protocol', '') is '' and not out_data.get('time', '') is '':
					return ('%s - Prov: %s, Caid: %s (%s) - %s ms') %\
						(out_data.get('source'),  out_data.get('prov', ''), out_data.get('caid', ''), out_data.get('using', ''), out_data.get('time', ''))
				elif out_data.get('protocol', '') is '' and out_data.get('time', '') is '':
					return ('%s - Prov: %s, Caid: %s (%s)') %\
						(out_data.get('source', ''),  out_data.get('prov', ''), out_data.get('caid', ''), out_data.get('using', ''))

			for data in ('source', 'prov', 'caid', 'reader', 'protocol', 'using', 'hops', 'time'):
				if not out_data.get(data, '') is '':
					display_data += out_data.get(data, '') + '  '
			return display_data

		elif self.type is self.Auto:
			if not out_data.get('source', '') is '':
				display_data += out_data.get('source', '') + ' - '
			if not out_data.get('prov', '') is '':
				display_data += 'Prov: ' + out_data.get('prov', '') + ',  '
			if not out_data.get('caid', '') is '':
				display_data += 'Caid: ' + out_data.get('caid', '') + ',  '
			if not out_data.get('reader', '') is '':
				display_data += 'Reader: ' + out_data.get('reader', '') + ',  '
			if not out_data.get('protocol', '') is '':
				display_data += out_data.get('protocol', '') + '  '
			if not out_data.get('using', '') is '':
				display_data += '(' + out_data.get('using', '') + ')  '
			if not out_data.get('hops', '') is '':
				display_data += 'hops: ' + out_data.get('hops', '') + ' '
			if not out_data.get('time', '') is '':
				display_data += '- ' + out_data.get('time', '') + ' ms'
			return display_data

		elif self.type is self.Crypt:
			if out_data.get('caid', '') is not '':
				return self.TxtCaids.get(out_data.get('caid')[:2]).upper()
			else:
				return 'NONDECODE'

		elif self.type is self.Format:
			return self.paramert_str.replace('Format:', '').replace('%C', out_data.get('caid', '')).replace('%P', out_data.get('prov', '')).replace('%T', out_data.get('time', '')).replace('%U', out_data.get('using', ''))\
				.replace('%R', out_data.get('reader', '')).replace('%H', out_data.get('hops', '')).replace('%O', out_data.get('port', '')).replace('%L', out_data.get('protocol', '')).replace('%S', out_data.get('source', ''))

	text = property(getText)

	def changed(self, what):
		if what[0] is self.CHANGED_SPECIFIC:
			Converter.changed(self, what)
		elif what[0] is self.CHANGED_POLL:
			self.downstream_elements.changed(what)
