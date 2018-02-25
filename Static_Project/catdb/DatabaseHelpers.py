from catdb.models import *


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

