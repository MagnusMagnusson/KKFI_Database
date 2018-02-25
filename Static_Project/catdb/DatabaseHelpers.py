﻿from catdb.models import *
from django.db import transaction
from datetime import datetime
from datetime import date

class CatDbHelper():
	#input(Entry number, SHow number)
	#Output: A dict with the cat object in question, the EMS entry, current points
	@staticmethod
	def getEntryInfo(entry,show):
		_cat = cat.objects.filter(show_entry__showId_id = int(show), show_entry__cat_show_number = int(entry))
		D = {'success':False}
		if(len(_cat) > 0):
			_cat = _cat[0]
			D['name'] = _cat.name
			D['Id'] = str(_cat.id)
			D['regId'] = str(_cat.reg_nr)
			D['ems'] = None
			D['cert'] = None
			D['Ncert'] = None 
			D['nextCert'] = None
			_neuter = neutered.objects.filter(catId = _cat)
			if(len(_neuter) > 0):
				_neuter = True
			else:
				_neuter = False 
			D['neutered'] = _neuter
			_ems = cat_EMS.objects.filter(cat_id = _cat.id)
			if(len(_ems) > 0):
				_ems = _ems.latest('reg_date')
				D['ems'] =str(_ems.ems.breed) + " " + str(_ems.ems.breed)
			_Npoint = cert_judgement.objects.filter(cat = _cat,cert__neutered = True)
			_point = cert_judgement.objects.filter(cat = _cat,cert__neutered = False)
			if(len(_point) > 0):
				D['cert'] = _point.latest('date')
			if(len(_Npoint) > 0):
				D['Ncert'] = _Npoint.latest('date')

			if(_neuter):
				D['nextCert'] = cert.objects.filter(predecessor =  D['Ncert'].cert if D['Ncert'] else None, neutered = True)[0]
			else:
				D['nextCert'] = cert.objects.filter(predecessor = D['cert'].cert if D['cert'] else None , neutered = False)[0]
			D['success'] = True
			return D

			
	@staticmethod
	@transaction.atomic
	def getNominations(showId):
		D = {}
		_show = show.objects.get(id = showId) 		
		_allCats = judgement.objects.filter(showId = _show, nom = True)

		#Litters
		litterNoms = judgementLitter.objects.filter(nom = True,showId = _show)
		D['litters'] = litterNoms

		#Kittens
		min_date = monthdelta(datetime.now().date(),-7)
		_kittenCats = _allCats.filter(entryId__catId__birth__gte = min_date)
		D['Kittens'] = _kittenCats

		#Younglings
		min_date = monthdelta(datetime.now().date(),-10)
		max_date = monthdelta(datetime.now().date(),-7)
		_youngCats = _allCats.filter(entryId__catId__birth__gt = min_date, entryId__catId__birth__lte = max_date)
		D['Younglings'] = _youngCats

		# adults
		max_date = monthdelta(datetime.now().date(),-10)
		_adults = _allCats.exclude(entryId__catId__birth__gt = max_date)
		_neutered = _adults.filter(entryId__catId__neutered__isnull=False)
		_nonNeutered = _adults.exclude(entryId__catId__neutered__isnull=False)
		_neuterMale = _neutered.filter(entryId__catId__gender = False)
		_neuterFemale = _neutered.filter(entryId__catId__gender = True)
		_NonneuterMale = _nonNeutered.filter(entryId__catId__gender = False)
		_NonneuterFemale = _nonNeutered.filter(entryId__catId__gender = True)

		D['Males'] = _NonneuterMale
		D['Females'] = _NonneuterFemale
		D['nMales'] = _neuterMale
		D['nFemales'] = _neuterFemale

		return D


def monthdelta(date, delta):
	m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
	if not m: m = 12
	d = min(date.day, [31,
		29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
	return date.replace(day=d,month=m, year=y)