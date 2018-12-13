# -*- coding: UTF-8 -*-
# Coders by Sirius
# v1.3
# code otimization
# add support TMBD

from Components.Converter.Converter import Converter
from Components.Element import cached, ElementError
from Components.config import config
from enigma import iServiceInformation, iPlayableService, iPlayableServicePtr, eServiceReference
from ServiceReference import ServiceReference
from Tools.Directories import fileExists
import os, sys

class MovieInfo2(Converter, object):
	MOVIE_FULL_DESCRIPTION = 0
	MOVIE_SHORT_DESCRIPTION = 1 # meta description when available.. when not .eit short description
	MOVIE_META_DESCRIPTION = 2 # just meta description when available
	MOVIE_REC_FILESIZE = 3 # filesize of recording
	MOVIE_SERVICE_NAME = 4 # name of recording service
	MOVIE_FILE_NAME = 5 # name of recording file
	MOVIE_ORIG_NAME = 6
	MOVIE_COVER_NAME = 7
	MOVIE_DESCRIPTION = 8
	MOVIE_DIRECTOR = 9
	MOVIE_ACTORS = 10
	MOVIE_COUNTRY = 11
	MOVIE_GENRE = 12
	MOVIE_YEAR = 13
	MOVIE_RATING = 14
	MOVIE_INFO = 15

	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "ShortDescription":
			self.type = self.MOVIE_SHORT_DESCRIPTION
		elif type == "MetaDescription":
			self.type = self.MOVIE_META_DESCRIPTION
		elif type == "FullDescription":
			self.type = self.MOVIE_FULL_DESCRIPTION
		elif type == "Description":
			self.type = self.MOVIE_DESCRIPTION
		elif type == "Director":
			self.type = self.MOVIE_DIRECTOR
		elif type == "Actors":
			self.type = self.MOVIE_ACTORS
		elif type == "Coutry":
			self.type = self.MOVIE_COUNTRY
		elif type == "Genre":
			self.type = self.MOVIE_GENRE
		elif type == "Year":
			self.type = self.MOVIE_YEAR
		elif type == "Rating":
			self.type = self.MOVIE_RATING
		elif type == "MovieInfo":
			self.type = self.MOVIE_INFO
		elif type == "OrigName":
			self.type = self.MOVIE_ORIG_NAME
		elif type == "CoverName":
			self.type = self.MOVIE_COVER_NAME
		elif type == "FileName":
			self.type = self.MOVIE_FILE_NAME
		elif type == "ServiceName":
			self.type = self.MOVIE_SERVICE_NAME
		elif type == "FileSize":
			self.type = self.MOVIE_REC_FILESIZE
		else:
			raise ElementError("'%s' is not <ShortDescription|MetaDescription|RecordServiceName|FileSize> for MovieInfo converter" % type)

	@cached

	def getText(self):
		name = ''
		name2 = ''
		filename = ''
		filetext = ''
		fulldescription = ''
		description = ''
		director = ''
		actors = ''
		coutry = ''
		genre = ''
		year = ''
		rating = ''
		movieinfo = ''
		moviename = ''
		recname = ''
		covername = ''
		service = self.source.service
#		info = self.source.info
		event = self.source.event

		if service:
			if isinstance(service, iPlayableServicePtr):
				info = service and service.info()
				name = info.getName()
				name2 = config.movielist.last_videodir.value
				filename = '%s%s' % (name2, name)
				filetext = filename.split('.')[0].strip() + '.txt'
			else: # selection
				info = service and self.source.info
				if (service.flags & eServiceReference.flagDirectory) == eServiceReference.flagDirectory:
					name = service.getPath()
					filename = '%s' % (name)
					filetext = filename + filename.split('/')[-2].strip() + '.txt'
				else:
					name = service.getPath()
					filename = '%s' % (name)
					filetext = filename.split('.')[0].strip() + '.txt'
			try:
#ShortDescription
				if self.type == self.MOVIE_SHORT_DESCRIPTION:
					return (info.getInfoString(service, iServiceInformation.sDescription)
						or (event and event.getShortDescription())
						or service.getPath())
#MetaDescription
				elif self.type == self.MOVIE_META_DESCRIPTION:
					return ((event and (event.getExtendedDescription() or event.getShortDescription()))
						or info.getInfoString(service, iServiceInformation.sDescription)
						or service.getPath())
#FullDescription
				elif self.type == self.MOVIE_FULL_DESCRIPTION:
					if fileExists(filetext):
						fulldescription = open("%s" % filetext, "r").readlines()[2]\
							+ open("%s" % filetext, "r").readlines()[3]\
							+"\n"+ open("%s" % filetext, "r").readlines()[4]\
							+"\n"+ open("%s" % filetext, "r").readlines()[6]\
							+ open("%s" % filetext, "r").readlines()[1]\
							+ open("%s" % filetext, "r").readlines()[5]
						return fulldescription
					elif fileExists(filename[:-2] + 'txt'):
						fulldescription = open("%s" % filename[:-2] + 'txt', "r").readlines()[5]\
							+ open("%s" % filename[:-2] + 'txt', "r").readlines()[4]\
							+"\n"+ open("%s" % filename[:-2] + 'txt', "r").readlines()[2]\
							+"\n"+ open("%s" % filename[:-2] + 'txt', "r").readlines()[6]\
							+ open("%s" % filename[:-2] + 'txt', "r").readlines()[0]\
							+ open("%s" % filename[:-2] + 'txt', "r").readlines()[1]
						return fulldescription
						
					else:
						return ((event and (event.getExtendedDescription() or event.getShortDescription()))
							or info.getInfoString(service, iServiceInformation.sDescription)
							or service.getPath())
#Description
				elif self.type == self.MOVIE_DESCRIPTION:
					if fileExists(filetext):
						description = open("%s" % filetext, "r").readlines()[4]
						return description
					elif fileExists(filename[:-2] + 'txt'):
						description = open("%s" % filename[:-2] + 'txt', "r").readlines()[2]
						return description
					else:
						return ((event and (event.getExtendedDescription() or event.getShortDescription()))
							or info.getInfoString(service, iServiceInformation.sDescription)
							or service.getPath())
#Director
				elif self.type == self.MOVIE_DIRECTOR:
					if fileExists(filetext):
						director = open("%s" % filetext, "r").readlines()[2]
					elif fileExists(filename[:-2] + 'txt'):
						director = open("%s" % filename[:-2] + 'txt', "r").readlines()[5]
					else:
						director = _("No director")
					return director
#Actors
				elif self.type == self.MOVIE_ACTORS:
					if fileExists(filetext):
						actors = open("%s" % filetext, "r").readlines()[3]
					elif fileExists(filename[:-2] + 'txt'):
						actors = open("%s" % filename[:-2] + 'txt', "r").readlines()[4]
					else:
						actors = _("No actors")
					return actors
#Coutry
				elif self.type == self.MOVIE_COUNTRY:
					if fileExists(filetext):
						coutry = open("%s" % filetext, "r").readlines()[1]
					elif fileExists(filename[:-2] + 'txt'):
						coutry = open("%s" % filename[:-2] + 'txt', "r").readlines()[0]
					else:
						coutry = _("No coutry")
					return coutry
#Genre
				elif self.type == self.MOVIE_GENRE:
					if fileExists(filetext):
						genre = open("%s" % filetext, "r").readlines()[5]
					elif fileExists(filename[:-2] + 'txt'):
						genre = open("%s" % filename[:-2] + 'txt', "r").readlines()[1]
					else:
						genre = _("No genre")
					return genre
#Year
				elif self.type == self.MOVIE_YEAR:
					if fileExists(filetext):
						year = open("%s" % filetext, "r").readlines()[6]
					elif fileExists(filename[:-2] + 'txt'):
						year = open("%s" % filename[:-2] + 'txt', "r").readlines()[6]
					else:
						year =  _("No year")
					return year
#Rating
				elif self.type == self.MOVIE_RATING:
					if fileExists(filetext):
						ratingall = open("%s" % filetext, "r").readlines()[7]
						rating = ratingall.split('Рейтинг:')[1].split('.')[0].strip()
					elif fileExists(filename[:-2] + 'txt'):
						ratingall = open("%s" % filename[:-2] + 'txt', "r").readlines()[3]
						rating = ratingall.split('Рейтинг:')[1].split('.')[0].strip()
					else:
						rating = ""
					return rating
#MovieInfo
				elif self.type == self.MOVIE_INFO:
					if fileExists(filetext):
						movieinfo = open("%s" % filetext, "r").readlines()[7]
					elif fileExists(filename[:-2] + 'txt'):
						movieinfo = open("%s" % filename[:-2] + 'txt', "r").readlines()[3]
					else:
						movieinfo = _("No info")
					return movieinfo
#MovieOrigName
				elif self.type == self.MOVIE_ORIG_NAME:
					if fileExists(filetext):
						nameall = open("%s" % filetext, "r").readlines()[0]
						moviename = nameall.split('Оригинальное название:')[1].strip()
					elif fileExists(filename[:-2] + 'txt'):
						nameall = open("%s" % filename[:-2] + 'txt', "r").readlines()[7]
						moviename = nameall.split('Оригинальное название:')[1].strip()
					else:
						moviename = _("No name")
					return moviename
#MovieCoverName
				elif self.type == self.MOVIE_COVER_NAME:
					path1 = '/media/usb/covers/' + filetext.split('/')[-1].split('.')[0].strip() + '.jpg'
					path2 = '/media/hdd/covers/' + filetext.split('/')[-1].split('.')[0].strip() + '.jpg'
					path3 = '/media/sdb1/covers/' + filetext.split('/')[-1].split('.')[0].strip() + '.jpg'
					path4 = '/media/sdb2/covers/' + filetext.split('/')[-1].split('.')[0].strip() + '.jpg'
					if fileExists(path1) or fileExists(path2) or fileExists(path3) or fileExists(path4):
						covername = filetext.split('/')[-1].split('.')[0].strip()
					else:
						covername = filetext.split('/')[-2].strip()
					return covername
#MovieFileName
				elif self.type == self.MOVIE_FILE_NAME:
					if filetext is not None:
						recname = filetext.split('/')[-1].split('.')[0].strip()
					else:
						recname = _("No name")
					return recname
#MovieServiceName
				elif self.type == self.MOVIE_SERVICE_NAME:
					rec_ref_str = info.getInfoString(service, iServiceInformation.sServiceref)
					return ServiceReference(rec_ref_str).getServiceName()
#FileSize
				elif self.type == self.MOVIE_REC_FILESIZE:
					if (service.flags & eServiceReference.flagDirectory) == eServiceReference.flagDirectory:
						return _("Directory")
					filesize = info.getInfoObject(service, iServiceInformation.sFileSize)
					if filesize is not None:
						if filesize >= 104857600000: #100000*1024*1024
							return _("%.0f GB") % (filesize / 1073741824.0)
						elif filesize >= 1073741824: #1024*1024*1024
							return _("%.2f GB") % (filesize / 1073741824.0)
						elif filesize >= 1048576:
							return _("%.0f MB") % (filesize / 1048576.0)
						elif filesize >= 1024:
							return _("%.0f kB") % (filesize / 1024.0)
						return _("%d B") % filesize
#End
			except:
				return _("No text")
		return ""

	text = property(getText)
