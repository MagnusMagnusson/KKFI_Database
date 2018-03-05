from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.utils.encoding import *
from django.db import transaction
from catdb.models import *
from .forms import SearchCat
from .forms import AddCat
import time
from datetime import datetime
from datetime import date
from DatabaseHelpers import CatDbHelper
import re


def form_cat(request):
	if not request.is_ajax():
		D = {
			'success':False,
			'error':'Invalid request format. Please contact the site administrator if you believe this a mistake.'
			}
		return JsonResponse(D)

	post =  request.POST
	try:
		C = cat()
		C.name = post['name']
		C.reg_nr = post['reg_nr']
		C.gender = not bool(post['gender'])
		C.sire = None
		C.dam = None
		sire = post['sire']
		dam = post['dam']
		if(sire):
			sire = int(sire)
		if(dam):
			dam = int(dam)

		reg_day = int(post['registered_day'])
		reg_month = int(post['registered_month'])
		reg_year = int(post['registered_year'])
		C.registered = date(reg_year, reg_month, reg_day)

		b_day = int(post['birth_day'])
		b_month = int(post['birth_month'])
		b_year = int(post['birth_year'])
		C.birth = date(b_year, b_month, b_day)
		if(sire):
			Sire = cat.objects.filter(id = sire)
			if(Sire.exists()):
				P = parents.objects.filter(cat = Sire)
				if(P.exists()):
					C.sire = P[0]
				else:
					P = parents()
					P.is_ghost = False
					P.cat = Sire
					P.save()
					C.sire = P
		if(dam):
			Dam = cat.objects.filter(id = dam)
			if(Dam.exists()):
				P = parents.objects.filter(cat = Dam)
				if(P.exists()):
					C.dam = P[0]
				else:
					P = parents()
					P.is_ghost = False
					P.cat = Dam
					P.save()
					C.dam = P
		M = microchip.objects.filter(microchip_nr = post['microchip'])
		C.save()
		if(M.exists()):
			M.cat = C
		else:
			M = microchip()
			M.microchip_nr = post['microchip']
			M.cat = C
			M.save()
		D = {
			'success':True,
			'id':C.id
			}
		return JsonResponse(D)
	except Exception as ex:		
		D = {
			'success':False,
			'error':type(ex).__name__,
			'message':str(ex)
			}
		return JsonResponse(D)

	#finds the name of cats matching {name, gender}
def find_cat_names(request):
	if not request.is_ajax():
		D = {
			'success':False,
			'error':'Invalid request format. Please contact the site administrator if you believe this a mistake.'
			}
		return JsonResponse(D)

	try:
		name =  smart_text(request.GET['name'],encoding='utf-8',strings_only=False,errors='strict')
		C = cat.objects.filter(name__icontains = name)
		isDam = request.GET['gender'] == 'dam'
		C = C.filter(gender = isDam)
		if(C.exists()):			
			D = {
				'success':True,
				'count':C.count(),
				'cats':[kitty for kitty in C.values('id', 'name')],
				'type': request.GET['gender']
				}
			return JsonResponse(D)
		else:		
			D = {
				'success':False,
				'count':0,
				'error':'No Cat Found',
				'type': request.GET['gender']
				}
			return JsonResponse(D)
		
	except Exception as ex:		
		D = {
			'success':False,
			'error':type(ex).__name__,
			'type': request.GET['gender']
			}
		return JsonResponse(D)

def api_create_show(request):
	if not request.is_ajax():
		D = {
			'success':False,
			'error':'Invalid request format. Please contact the site administrator if you believe this a mistake.'
			}
		return JsonResponse(D)

	try:
		post =  request.POST
		orginizer = post['organizer']
		name =  smart_text(post['name'],encoding='utf-8',strings_only=False,errors='strict')
		S = show();
		S.name = name 
		S.show_orginizer = orginizer

		
		day = int(post['date_day'])
		month = int(post['date_month'])
		year = int(post['date_year'])
		S.date = date(year, month, day)

		S.save()
		D = {
			'success':True,
			'id':S.id
			}
		return JsonResponse(D)
	except Exception as ex:		
		D = {
			'success':False,
			'error':type(ex).__name__,
			'message':str(ex)
		}
		return JsonResponse(D)


	#{cat:ID, show:ID, entry Nr:INT}
	#Registers the specific cat to the specific show with the specific number. 
def api_show_entry_register(request):
	if not request.is_ajax():
		D = {
			'success':False,
			'error':'Invalid request format. Please contact the site administrator if you believe this a mistake.'
			}
		return JsonResponse(D)
	try:
		post =  request.POST
		catID = post['cat']
		showID = post['show']
		entryNr = post['entry_nr']
		_cat = cat.objects.get(id = catID)
		_show = show.objects.get(id = showID)
		_entry = show_entry()
		_entry.catId = _cat
		_entry.showId = _show
		_entry.cat_show_number = int(entryNr)
		_entry.save()
		D = {'success':True}
		return JsonResponse(D)
	except Exception as ex:		
		D = {
			'success':False,
			'error':type(ex).__name__,
			'message':str(ex)
		}

	return JsonResponse(D)

def api_show_judge_register(request):
	if not request.is_ajax():
			D = {
				'success':False,
				'error':'Invalid request format. Please contact the site administrator if you believe this a mistake.'
				}
			return JsonResponse(D)
	try:
		post =  request.POST
		judgeId = post['judge']
		showID = post['show']
		_judge = judge.objects.get(id = judgeId)
		_show = show.objects.get(id = showID)
		_entry = judge_show()
		_entry.judgeId = _judge
		_entry.showId = _show
		_entry.save()
		D = {'success':True}
		return JsonResponse(D)
	except Exception as ex:		
		D = {
			'success':False,
			'error':type(ex).__name__,
			'message':str(ex)
		}
		return JsonResponse(D)

def api_show_litter_entry_register(request):
	if not request.is_ajax():
			D = {
				'success':False,
				'error':'Invalid request format. Please contact the site administrator if you believe this a mistake.'
				}
			return JsonResponse(D)
	try:
		post =  request.POST
		entryId = post['litterCat']
		letterId = post['litterLetter']
		_entry = None
		try:
			_entry = show_entry.objects.get(id = entryId)
		except Exception as ex:
			D = {
			'success':False,
			'error':type(ex).__name__,
			'message':"inner " + str(ex)
			}
			return JsonResponse(D)
		_litter = litter()
		_litter.catId = _entry
		_litter.letterId = letterId
		_litter.save()
		D = {'success':True}
		return JsonResponse(D)
	except Exception as ex:		
		D = {
			'success':False,
			'error':type(ex).__name__,
			'message':"outer " + str(ex)
		}
		return JsonResponse(D)

def api_judge_search_name(request):
	if not request.is_ajax():
		D = {
			'success':False,
			'error':'Invalid request format. Please contact the site administrator if you believe this a mistake.'
			}
	name = request.GET['name']
	judges = judge.objects.all().filter(name__icontains = name)
	if(judges.exists()):			
		D = {
			'success':True,
			'count':judges.count(),
			'judges':[j for j in judges.values('id', 'name','country')]
			}
		return JsonResponse(D)
	else:		
		D = {
			'success':False,
			'count':0,
			'error':'No Judge Found'
			}
		return JsonResponse(D)
	
def api_entry_search_name(request):
	if not request.is_ajax():
		D = {
			'success':False,
			'error':'Invalid request format. Please contact the site administrator if you believe this a mistake.'
			}
	name = request.GET['name']
	show = request.GET['show']
	
	current = datetime.now().date()
	max_date = date(current.year - 25, current.month, current.day)

	entries = show_entry.objects.all().filter(catId__name__icontains = name, showId = show).exclude(catId__birth__lte = max_date)

	if(entries.exists()):	
		entr = []
		for e in entries:
			entr.append({
				'name':e.catId.name,
				'id':e.cat_show_number
				})		
		D = {
			'success':True,
			'count':entries.count(),
			'kitties': entr
			}
		return JsonResponse(D)
	else:		
		D = {
			'success':False,
			'count':0,
			'error':'No Judge Found'
			}
		return JsonResponse(D)

def api_entry_get_info(request):	
	if not request.is_ajax():
		D = {
			'success':False,
			'error':'Invalid request format. Please contact the site administrator if you believe this a mistake.'
			}
	try:
		entryNum = request.GET['entry']
		showNum = request.GET['show']
		D = CatDbHelper.getEntryInfo(entryNum,showNum)
		if(D['cert']):
			D['cert'] = D['cert'].cert.certName + str(D['cert'].cert.certRank)
		if(D['Ncert']):
			D['Ncert'] = D['Ncert'].cert.certName + str(D['Ncert'].cert.certRank)
		if(D['nextCert']):
			D['nextCert'] = D['nextCert'].certName + str(D['nextCert'].certRank)
	except Exception as ex:
		D = {
			'success':False,
			'error':type(ex).__name__,
			'message':str(ex)
			}
	return JsonResponse(D)

@transaction.atomic
def api_show_enter_judgement(request):
	if not request.is_ajax():
		D = {
			'success':False,
			'error':'Invalid request format. Please contact the site administrator if you believe this a mistake.'
			}
	try:		
		entryNum = request.POST['entryCatId']
		showNum = request.POST['show']
		C = CatDbHelper.getEntryInfo(entryNum,showNum)
		if int(C['Id']) != int(request.POST['CatId']):
			D = {
				'success':False,
				'error':"Integrety Error",
				'message':"The cat specified does not match the entry number [" + str(int(C['Id'])) +" vs " + str(int(request.POST['CatId'])) +" ]"
			}
			return JsonResponse(D)
		_cat = cat.objects.get(id = int(C['Id']))
		_judgement = judgement()
		_entry = show_entry.objects.get(showId = int(showNum), cat_show_number = int(entryNum), catId = _cat)
		_show = show.objects.get(id = int(showNum))
		_judge = judge.objects.get(id = request.POST['judge'])
		_judgement.showId = _show
		_judgement.entryId = _entry
		_judgement.judge = _judge
		_judgement.attendence = not (request.POST['abs'] == "true")
		_judgement.ex =  request.POST['ex']
		_judgement.cert =  request.POST['cert'] == "true"
		_judgement.biv =  request.POST['biv'] == "true"
		_judgement.nom =  request.POST['nom'] == "true"
		_judgement.comment = request.POST['comment']
		_newTitle = C['nextCert'].title.name if ( _judgement.cert and  C['nextCert'] and C['nextCert'].predecessor and C['nextCert'].title != C['nextCert'].predecessor.title) else None
		_ems = cat_EMS.objects.filter(cat_id = _cat.id)
		if(len(_ems) > 0):
			_ems = _ems.latest('reg_date')
		else:
			_ems = None
		_judgement.color = _ems
		_judgement.save()
		_cert = None
		if(_judgement.cert):
			_cert = cert_judgement()
			_cert.cat = _cat
			_cert.judgement = _judgement
			_cert.date = _show.date
			_cert.cert = C['nextCert']
			_cert.save()

		D = {
			'success': True,
			'Judgement' : _judgement.id,
			'Certificate' : _cert.id if _cert else None,
			'newTitle' : _newTitle != None,
			'newTitleName' : _newTitle
			}

	except Exception as ex:
		D = {
			'success':False,
			'error':type(ex).__name__,
			'message':str(ex)
			}
	return JsonResponse(D)


@transaction.atomic
def api_show_edit_judgement(request):
	if not request.is_ajax():
		D = {
			'success':False,
			'error':'Invalid request format. Please contact the site administrator if you believe this a mistake.'
			}
	try:		
		entryNum = request.POST['entryCatId']
		showNum = request.POST['show']
		C = CatDbHelper.getEntryInfo(entryNum,showNum)
		if int(C['Id']) != int(request.POST['CatId']):
			D = {
				'success':False,
				'error':"Integrety Error",
				'message':"The cat specified does not match the entry number [" + str(int(C['Id'])) +" vs " + str(int(request.POST['CatId'])) +" ]"
			}
			return JsonResponse(D)
		_cat = cat.objects.get(id = int(C['Id']))
		_show = show.objects.get(id = int(showNum))
		_judgement = judgement.objects.get(id = request.POST['judgement'])

		_judge = judge.objects.get(id = request.POST['judge'])
		_judgement.judge = _judge
		_judgement.attendence = not (request.POST['abs'] == "true")
		_judgement.ex =  request.POST['ex']
		_judgement.cert =  request.POST['cert'] == "true"
		_judgement.biv =  request.POST['biv'] == "true"
		_judgement.nom =  request.POST['nom'] == "true"
		_judgement.comment = request.POST['comment']
		_newTitle = C['nextCert'].title.name if ( _judgement.cert and  C['nextCert'] and C['nextCert'].predecessor and C['nextCert'].title != C['nextCert'].predecessor.title) else None
		_judgement.save()

		_cert = cert_judgement.objects.filter(judgement = _judgement)
		if(_judgement.cert):
			if(len(_cert) == 0):
				_cert = cert_judgement()
				_cert.cat = _cat
				_cert.judgement = _judgement
				_cert.date = _show.date
				_cert.cert = C['nextCert']
				_cert.save()
		else: 			
			if(len(_cert) > 0):
				_cert.delete()

		D = {
			'success': True,
			'Judgement' : _judgement.id,
			'Certificate' : _cert.id if _cert else None,
			'newTitle' : _newTitle != None,
			'newTitleName' : _newTitle
			}

	except Exception as ex:
		D = {
			'success':False,
			'error':type(ex).__name__,
			'message':str(ex)
			}
	return JsonResponse(D)


@transaction.atomic
def api_show_edit_cat(request):
	if not request.is_ajax():
		D = {
			'success':False,
			'error':'Invalid request format. Please contact the site administrator if you believe this a mistake.'
			}
	try:		

	#GetDefualts
		c = cat.objects.get(reg_nr = request.POST['reg_nr'])
		n = neutered.objects.filter(catId = c)
		neuter = False 
		neutered_date = None
		if(len(n) == 1):
			neuter = True
			neutered_date = n[0].date

		micro = None	
		m = microchip.objects.filter(cat = c)
		if(len(m) > 0):
			m = m.latest()
			micro = m.microchip_nr
		color = ""
		ems = cat_EMS.objects.filter(cat = c)
		if(ems > 0):
			ems = ems.latest('reg_date')
			color = ems.ems.breed + " " + ems.ems.ems

		certificate = None 
		NeuterCertificate = None
		cert = cert_judgement.objects.filter(cat = c, cert__neutered = False)
		if(len(cert) > 0):
			certificate = cert.latest('date').cert
		Ncert = cert_judgement.objects.filter(cat = c, cert__neutered = True)
		if(len(Ncert) > 0):
			NeuterCertificate = cert.latest('date').cert
		default = {
				'name':c.name,
				'gender':not c.gender,
				'birth':c.birth,
				'registered':c.registered,
				'dam':c.dam.cat.reg_nr,
				'reg_nr':c.reg_nr,
				'neutered':neuter,
				'neutered_Date':neutered_date,
				'microchip' : micro,
				'color' : color,
				'certificate' : certificate,
				'neutered_certificate' : NeuterCertificate
			}
		#Updates

		if(request.POST['name'] != default['name']):
			c.name = request.POST['name']
		c.gender = request.POST['gender'] == "true"
		if(c.sire != default['sire']):
			c.sire = parents.objects.get(cat__reg_nr = request.POST['sire'])
		if(c.dam !=  default['dam']):
			c.dam = parents.objects.get(cat__reg_nr = request.POST['dam'])
		if(request.POST['microchip'] !=  default['micro']):
			m = microchip.objects.filter(cat = c)
			if(len(m) > 0):
				m = m.latest()
				if(m.microchip_nr != request.POST['microchip']):
					m = microchip()
					m.cat = c
					m.microchip_nr = request.POST['microchip']
		if(request.POST['color'] != default['color']):
			emsString = request.POST['color']
			ems_breed = emsString[:3].strip().upper()
			ems_color = emsString[4:].strip().lower()
			ems = EMS.objects.get(breed = ems_breed, ems = ems_color)
			newEmsField = cat_EMS()
			newEmsField.cat = c
			newEmsField.ems = ems 
			newEmsField.reg_date = date.today()
			newEmsField.save()
		if (request.POST['neuter']  == "true")!= default["neutered"]:
			request.POST['neuter']  == "true"

		return JsonResponse(D)
	except Exception as ex:
		D = {
			'success':False,
			'error':type(ex).__name__,
			'message':str(ex)
			}
	return JsonResponse(D)



def api_show_enter_color_judgement(request):
	if not request.is_ajax():
		D = {
			'success':False,
			'error':'Invalid request format. Please contact the site administrator if you believe this a mistake.'
			}
		return JsonResponse(D)
	try:		
		emsString = request.POST['new_EMS']
		ems_breed = emsString[:3].strip().upper()
		ems_color = emsString[4:].strip().lower()
		ems = EMS.objects.get(breed = ems_breed, ems = ems_color)

		judgement = cat_EMS()
		judgement.cat = cat.objects.get(id = request.POST['colCatId'])
		judgement.ems = ems 
		judgement.reg_date = show.objects.get(id = request.POST['show']).date
		judgement.save()
		D = {
			'success': True
			}

	except Exception as ex:
		D = {
			'success':False,
			'error':type(ex).__name__,
			'message':str(ex)
			}
	return JsonResponse(D)

def api_show_enter_litter_judgement(request):
	if not request.is_ajax():
		D = {
			'success':False,
			'error':'Invalid request format. Please contact the site administrator if you believe this a mistake.'
			}
		return JsonResponse(D)
	try:		
		_litter = judgementLitter()
		_litter.showId = show.objects.get(id = request.POST['show'])
		_litter.judge = judge.objects.get(id = request.POST['judge'])
		_litter.attendence = request.POST['abs'] != 'true'
		_litter.nom = request.POST['nom'] == 'true'
		_litter.litter_nr = request.POST['litter']
		_litter.comment = request.POST['comment']
		_litter.rank = int(request.POST['rank'])
		_litter.save()
		D = {
			'success': True,
			'litter' : _litter.id
			}

	except Exception as ex:
		D = {
			'success':False,
			'error':type(ex).__name__,
			'message':str(ex)
			}
	return JsonResponse(D)

