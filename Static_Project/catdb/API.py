from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.utils.encoding import *
from catdb.models import *
from .forms import SearchCat
from .forms import AddCat
import time
from datetime import datetime
from datetime import date


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
		C.registered = datetime.date(reg_year, reg_month, reg_day)

		b_day = int(post['birth_day'])
		b_month = int(post['birth_month'])
		b_year = int(post['birth_year'])
		C.birth = datetime.date(b_year, b_month, b_day)
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
		S.date = datetime.date(year, month, day)

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


