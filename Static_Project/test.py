
from sets import Set
from catdb.models import *
from django.utils import timezone
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
# Create your tests here.



def setUp(self): #Sets up this unit test, populating the database. 
	print("STARTING SETUP")
	Clast = None
	Cprev = None
	for i in xrange(30):
		C = cat()
		C.name = "kisi_nr_"+ str(i)
		C.birth = timezone.now()
		C.reg_nr = str(i * 100 + i * 23 + i*17 + i*5 + i)
		C.registered = C.birth
		C.gender = (i % 2) == 0
		if(Clast != None):
			C.sire = Clast
		if(Cprev != None):
			C.dam = Cprev
		C.save()
			# ADD PARENT ENTRY
		P = parents()
		P.is_ghost = False
		P.cat = C
		P.save()
			# ADD MICROCHIP ENTRY
		M = microchip()
		M.cat = C
		M.microchip_nr = str(int(C.reg_nr) + 5)
		M.save()
			#ADD NEUTERED ENTRY (only every third cat is neutered)
		if((i%3) == 0):
			N = neutered()
			N.cat = C
			N.date = timezone.now()
			#Create imported cats
		if(i%4 == 0):
			IC = cat()
			IC.name = "Imported_cat_"+str(i/4)
			IC.birth = timezone.now()
			IC.registered = IC.birth
			IC.gender = (i%2)
			IC.reg_nr = 12*(i * 100 + i * 23 + i*17 + i*5 + i)
			IC.save()
			I = imp_cat() 
			I.cat = IC
			I.org_country = "ICE"
			I.org_organization = "Orginization"
			j = i/4
			I.org_reg_nr = str(10*(j * 100 + j * 23 + j*17 + j*5 + j))
			I.save()
                
		if((i % 2) != 0):
			Clast = P
		else:
			Cprev = P
	Pdam = parents.objects.get(cat = cat.objects.get(name = "kisi_nr_18").id )
	Psire = parents.objects.get(cat = cat.objects.get(name = "kisi_nr_17").id )
        
	#Brother
	C = cat()
	C.name = "Brother"
	C.gender = True
	C.reg_nr = "12394"
	C.birth = timezone.now()
	C.registered = timezone.now()
	C.dam = Pdam
	C.save()
	M = microchip()
	M.cat = C
	M.microchip_nr = str(int(C.reg_nr) + 5)
	M.save()
	#sister
	C = cat()
	C.name = "Sister"
	C.gender = False
	C.reg_nr = "13234"
	C.birth = timezone.now()
	C.registered = timezone.now()
	C.sire = Psire
	C.save()           
	M = microchip()
	M.cat = C
	M.microchip_nr = str(int(C.reg_nr) + 5)
	M.save()
	#EvilTwin
	C = cat()
	C.name = "EvilTwin"
	C.gender = False
	C.reg_nr = "99999"
	C.birth = timezone.now()
	C.registered = timezone.now()
	C.sire = Psire
	C.dam = Pdam
	C.save()            
	M = microchip()
	M.cat = C
	M.microchip_nr = str(int(C.reg_nr) + 5)
	M.save()
setUp()