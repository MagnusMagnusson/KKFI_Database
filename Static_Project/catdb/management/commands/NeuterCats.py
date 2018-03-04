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
	@transaction.atomic
	def handle(self, *args, **options):
		print("started better")
		Length = 1
		with open('KKIDB_exports/geldingar.csv', 'rb') as lengthfile:
			lengthreader =  unicode_csv_reader(lengthfile, quotechar='"')
			Length = sum(1 for row in lengthreader)
			print("Length recorded as " + str(Length))
		lengthfile.close()

		with open('KKIDB_exports/geldingar.csv', 'rb') as csvfile:
			spamreader = unicode_csv_reader(csvfile, quotechar='"')
			first = True
			print("loaded")
			done = 0
			colorless = 0
			lastpercent = 0.05
			for row in spamreader:
				regnr = int(row[0])
				C = cat.objects.filter(reg_nr = regnr)
				if(len(C) == 1):
					isneutered = neutered.objects.filter(catId__reg_nr = regnr)
					if(len(isneutered) == 0):
						N = neutered()
						N.catId = C[0]
						N.date = None
				done += 1
				if((100*done/Length) >= 100*lastpercent):
					print(str(lastpercent*100) + "% done ("+str(done) + " cats registered)")
					lastpercent += 0.05
			print("import done ("+str(done + 1)+"/"+str(Length) + " cats neutered!)")
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

