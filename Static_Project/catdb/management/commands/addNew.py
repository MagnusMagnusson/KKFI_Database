# -*- coding: utf-8 -*-
import csv
import os
from sets import Set
from django.core.management.base import BaseCommand, CommandError
from catdb.models import *
from django.utils import timezone
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from datetime import date
from django.db import transaction


class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('File', nargs='+', type=str)
	@transaction.atomic
	def handle(self, *args, **options):
		print("started better")
		Length = 1
		with open(options['File'][0], 'rb') as lengthfile:
			lengthreader =  unicode_csv_reader(lengthfile, quotechar='"')
			Length = sum(1 for row in lengthreader)
			print("Length recorded as " + str(Length))
		lengthfile.close()

		with open(options['File'][0], 'rb') as csvfile:
			spamreader = unicode_csv_reader(csvfile, quotechar='"')
			first = True
			print("loaded")
			done = 0
			colorless = 0
			lastpercent = 0.05
			for row in spamreader:
				existingCat = cat.objects.filter(reg_nr=row[0])
				if len(existingCat) >= 1:
					continue
				C = cat()
				if(len(row[1]) > 50):
					print("TOO LONG NAME",row[1])
				C.name = row[1]
				C.reg_nr = row[0]
				C.gender = (row[2] != 'Fress')
				if(row[2] != ''):
					date_object = datetime.strptime(row[4], '%d.%m.%y')
					C.registered = date_object.date()
				else:
					date_object = datetime.strptime("1.1.1970 05:05", '%d.%m.%y')
					C.registered = date_object.date()

				if(row[3] != ''):
					date_object = datetime.strptime(row[3], '%d.%m.%y')
					C.birth = date_object.date()
				else:
					date_object = datetime.strptime("1.1.1970 05:05", '%d.%m.%y')
					C.birth = date_object.date()
					
				if(row[5] != ''):
					try:
						daddy = cat.objects.get(reg_nr = int(row[5]))
						daddy_clause = parents.objects.get(cat = daddy)
						C.sire = daddy_clause
					except ObjectDoesNotExist:
						C.sire = None

				if(row[6] != ''):
					try:
						mommy = cat.objects.get(reg_nr = int(row[6]))
						mommy_clause = parents.objects.get(cat = mommy)
						C.dam = mommy_clause
					except ObjectDoesNotExist:
						C.dam = None	
				C.save()
				
				if(row[7] != ''):
					emsString = row[7]
					ems_breed = emsString[:3].strip().upper()
					ems_color = emsString[4:].strip().lower()
					_ems = EMS.objects.filter(breed = ems_breed,ems = ems_color)
					if(len(_ems) == 0):
						colorless += 1
						newEms = EMS()
						newEms.breed = ems_breed
						newEms.ems = ems_color
						newEms.category = -1
						newEms.save()
						_ems = [newEms]
					else:
						if(len(_ems) > 1):
							print("'" + ems_breed + "' and '" + ems_color + "' appears often. cat '" + C.name + "' ("+str(C.reg_nr) + ") is colourless" )
					_ems = _ems[0]
					ems_field = cat_EMS()
					ems_field.cat = C 
					ems_field.ems = _ems
					ems_field.reg_date = datetime.strptime("1.1.1970", '%d.%m.%Y').date()
					ems_field.save()
						

					P = parents()
					P.is_ghost = False
					P.cat = C
					P.save()

					done += 1
					if((100*done/Length) >= 100*lastpercent):
						print(str(lastpercent*100) + "% done ("+str(done) + " cats registered)")
						lastpercent += 0.05
			print("import done ("+str(done + 1)+"/"+str(Length) + " cats registered)")
			print("Colourless : " + str(colorless))
			csvfile.close()

		#		C = cat();
		#		C.name = row[3]
		#		C.reg_nr = row[0]
		#		if(row[5] == 'Fress'):
		#			C.gender = True
		#		C.birth


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, delimiter = ';',**kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [str(cell) for cell in row]



def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.decode('latin_1').encode('utf-8')

