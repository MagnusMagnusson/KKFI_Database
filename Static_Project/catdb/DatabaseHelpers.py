from catdb.models import *
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
				D['ems'] =str(_ems.ems.breed) + " " + str(_ems.ems.ems)
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
	def getCatInfo(c):
		n = neutered.objects.filter(catId = c)
		neuter = False 
		neutered_date = None
		if(len(n) == 1):
			neuter = True
			neutered_date = n[0].date

		micro = None	
		m = microchip.objects.filter(cat = c)
		if(len(m) > 0):
			m = m.latest('id')
			micro = m.microchip_nr
		color = ""
		ems = cat_EMS.objects.filter(cat = c)
		if(ems > 0):
			ems = ems.latest('reg_date')
			color = ems.ems.breed + " " + ems.ems.ems

		certificate = None 
		NeuterCertificate = None
		normalCert = cert_judgement.objects.filter(cat = c, cert__neutered = False)
		if(len(normalCert) > 0):
			certificate = normalCert.latest('date').cert
		Ncert = cert_judgement.objects.filter(cat = c, cert__neutered = True)
		if(len(Ncert) > 0):
			NeuterCertificate = Ncert.latest('date').cert
		D = {
				'name':c.name,
				'gender':not c.gender,
				'birth':c.birth,
				'registered':c.registered,
				'sire':c.sire.cat.reg_nr if c.sire else None,
				'dam':c.dam.cat.reg_nr if c.dam else None,
				'reg_nr':c.reg_nr,
				'neutered':neuter,
				'neutered_Date':neutered_date,
				'microchip' : micro,
				'color' : color,
				'certificate' : certificate,
				'neutered_certificate' : NeuterCertificate
			}
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
		min_date = monthdelta(_show.date,-7)
		_kittenCats = _allCats.filter(entryId__catId__birth__gte = min_date)
		D['Kittens'] = _kittenCats

		#Younglings
		min_date = monthdelta(_show.date,-10)
		max_date = monthdelta(_show.date,-7)
		_youngCats = _allCats.filter(entryId__catId__birth__gt = min_date, entryId__catId__birth__lte = max_date)
		D['Younglings'] = _youngCats

		# adults
		max_date = monthdelta(_show.date,-10)
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
		D['Everyone'] = _allCats
		return D


def getClass(catEntry):
		kittenDelta = monthdelta(_show.date,-10)
		kittenDelta = monthdelta(_show.date,-7)
		_cat = catEntry.catId

def monthdelta(date, delta):
	m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
	if not m: m = 12
	d = min(date.day, [31,
		29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
	return date.replace(day=d,month=m, year=y)

def timeDelta(oldDate,newDate):
	m = newDate.month - oldDate.month
	y = oldDate.year - newDate.year 
	if m < 0:
		m += 12
		y -= 1
	return (y,m)

