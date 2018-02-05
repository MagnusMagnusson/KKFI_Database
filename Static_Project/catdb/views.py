# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.utils.encoding import *
from catdb.models import *
from .forms import *
import time
import datetime
from API import *


# Create your views here.

def index(request,self):
	template = loader.get_template('kkidb/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def search(request,isSafe = True,nom = ""):
	template = loader.get_template('kkidb/search.html')
	form = SearchCat()
	context = {
		'form': form,
		'isSafe':isSafe,
		'nom':nom
		}
	return HttpResponse(template.render(context, request))

def findcat(request):
	c = cat.objects.all()
	req = request.GET
	valid = False
	#****************** Name **************
	if(len(req.get('name')) >= 3):
		valid = True
		uniname = '%'+ req.get('name') + "%"
		nomc = cat.objects.raw("SELECT * from catdb_cat where name like %s",[uniname])
		qset = [row.id for row in nomc] 
		c = c.filter(id__in = qset)
	#****************** Registered number **************
	if(req.get('reg_nr') != ''):
		valid = True
		c = c.filter(reg_nr = req.get('reg_nr'))
	#****************** GENDER *********************
	if(req.get('gender') != None):
		valid = True
		c = c.filter(gender = eval(req.get('gender')))
	# ***************** Birth lookup *************
	if(req.get('birth_year') != '0'):
		valid = True
		c = c.filter(birth__year = req.get('birth_year'))
	if(req.get('birth_month') != '0'):
		valid = True
		c = c.filter(birth__month = req.get('birth_month'))
	if(req.get('birth_day') != '0'):
		valid = True
		c = c.filter(birth__day = req.get('birth_day'))
	# **************** Registered lookup *************
	if(req.get('registered_year') != '0'):
		valid = True
		c = c.filter(registered__year = req.get('registered_year'))
	if(req.get('registered_month') != '0'):
		valid = True
		c = c.filter(registered__month = req.get('registered_month'))
	if(req.get('registered_day') != '0'):
		valid = True
		c = c.filter(registered__day = req.get('registered_day'))	
	# *************** Dam and Sire ********************
	if(req.get('dam') != ''):
		valid = True
		for cats in c[:]:
			P = cats.dam
			if(P == None or P.cat == None or (not (req.get('dam') in P.cat.name))):
				c = c.exclude(name = cats.name)
	if(req.get('sire') != ''):
		valid = True
		for cats in c[:]:
			P = cats.sire
			if(P == None or P.cat == None or (not (req.get('sire') in P.cat.name))):
				c = c.exclude(name = cats.name)
	#**************** Roundup *****************
	if(len(c) > 0):
		template = loader.get_template('kkidb/results.html')
		context = {
			'cats': c,
		}
		return HttpResponse(template.render(context, request))
	else:
		return search(request,False,req.get('name'))

def kitty(request):
	C = cat.objects.all()
	template = loader.get_template('kkidb/testpage.html')
	context = {
		'cats': C,
	}
	return HttpResponse(template.render(context, request))

def catview(request):
	template = loader.get_template('kkidb/ViewCat.html')
	view = request.GET.get('view')
	if(view != ''):
		c = cat.objects.all()
		c = c.filter(id = view)
	if(len(c) != 1):
		context = {}
	else:
		n = neutered.objects.filter(catId = c[0])
		if(not n.exists()):
			n = None
		context ={
				'cat'  : c[0],
				'isNeutered': n != None,
				'neuterData' : n
			}

	return HttpResponse(template.render(context, request))

def addcat(request):
	form = AddCat()
	template = loader.get_template('kkidb/AddCat.html')
	context = {
		'form': form
		}

	return HttpResponse(template.render(context, request))


def findshow(request):
	s = show.objects.all()
	template = loader.get_template('kkidb/findShow.html')
	if(len(s) > 0):
		context = {
			'shows': s,
		}
	else:
		context = {
		}
	return HttpResponse(template.render(context, request))

def addshow(request):
	form = form_add_show()
	template = loader.get_template('kkidb/AddShow.html')
	context = {
		'form': form 
		}
	return HttpResponse(template.render(context,request))


def view_ShowRegisterEntry(request):
	form = form_show_entry_add()
	template = loader.get_template('kkidb/show/ShowAddEntry.html')
	context = {
		'form': form 
		}
	return HttpResponse(template.render(context,request))

def fourohfour(request):
	template = loader.get_template('kkidb/404.html')
	context = {}
	return HttpResponse(template.render(context, request))