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
import datetime


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
	return False