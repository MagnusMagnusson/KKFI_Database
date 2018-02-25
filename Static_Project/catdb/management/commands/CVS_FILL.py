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
		with open('KKIDB_exports/Adallisti.csv', 'rb') as lengthfile:
			lengthreader =  unicode_csv_reader(lengthfile, quotechar='"')
			Length = sum(1 for row in lengthreader)
			print("Length recorded as " + str(Length))
		lengthfile.close()

		with open('KKIDB_exports/Adallisti.csv', 'rb') as csvfile:
			spamreader = unicode_csv_reader(csvfile, quotechar='"')
			first = True
			print("loaded")
			done = 0
			lastpercent = 0.05
			for row in spamreader:
				if(first):
					first = False
				else:
					C = cat()
					if(len(row[3]) > 50):
						print("TOO LONG NAME",row[3])
					C.name = row[3]
					C.reg_nr = row[0]
					C.gender = (row[5] != 'Fress')
					if(row[2] != ''):
						date_object = datetime.strptime(row[2], '%d.%m.%Y %H:%M:%S')
						C.registered = date_object.date()
					else:
						date_object = datetime.strptime("1.1.1970 05:05:05", '%d.%m.%Y %H:%M:%S')
						C.registered = date_object.date()

					if(row[4] != ''):
						date_object = datetime.strptime(row[4], '%d.%m.%Y %H:%M:%S')
						C.birth = date_object.date()
					else:
						date_object = datetime.strptime("1.1.1970 05:05:05", '%d.%m.%Y %H:%M:%S')
						C.birth = date_object.date()

					if(row[10] != ''):
						try:
							daddy = cat.objects.get(reg_nr = int(row[10]))
							daddy_clause = parents.objects.get(cat = daddy)
							C.sire = daddy_clause
						except ObjectDoesNotExist:
							C.sire = None

					if(row[11] != ''):
						try:
							mommy = cat.objects.get(reg_nr = int(row[11]))
							mommy_clause = parents.objects.get(cat = mommy)
							C.dam = mommy_clause
						except ObjectDoesNotExist:
							C.dam = None	

					if(int(row[22]) != 0):
						N = neutered()
						N.catId = C 
						if(len(row[21]) > 5):
							N.date = datetime.strptime(row[21], '%d.%m.%Y %H:%M:%S')
					C.save()
					try:
						Point = cert.objects.get(certName = "CAC",certRank = 1)
					except: 
						print("Master detected")
					for i in range(38,63):
						row[i] = int(row[i])
						if(row[i] == 0):
							break
						
						givenPoint = cert_judgement()
						givenPoint.cat = C
						givenPoint.judgement = None
						givenPoint.cert = Point
						givenPoint.date = date.today()
						givenPoint.save()					
						try:
							Point = cert.objects.get(predecessor = Point)
						except cert.DoesNotExist:
							print("Master detected")
							break;
						
					try:
						Point = cert.objects.get(certName = "CAP",certRank = 1)
					except:
						contineu
					for i in range(63,88):
						row[i] = int(row[i])
						if(row[i] == 0):
							break
						
						givenPoint = cert_judgement()
						givenPoint.cat = C
						givenPoint.judgement = None
						givenPoint.cert = Point
						givenPoint.date = date.today()
						givenPoint.save()
						try:
							Point = cert.objects.get(predecessor = Point)
						except cert.DoesNotExist:
							break;

					P = parents()
					P.is_ghost = False
					P.cat = C
					P.save()

					done += 1
					if((100*done/Length) >= 100*lastpercent):
						print(str(lastpercent*100) + "% done ("+str(done) + " cats registered)")
						lastpercent += 0.05
			print("import done ("+str(done + 1)+"/"+str(Length) + " cats registered)")
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

