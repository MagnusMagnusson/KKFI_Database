# -*- coding: utf-8 -*- 

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kkidb.settings")
django.setup()

import csv
from sets import Set
from catdb.models import *
from django.utils import timezone
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]



def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.decode('latin_1').encode('utf-8')

print("LOL");
print("started")
with open('KKIDB_EXPORTS/Adallisti.csv', 'rb') as csvfile:
	spamreader = unicode_csv_reader(csvfile, delimiter=';', quotechar='"')
	first = True
	print("loaded")
	for row in spamreader:
		print("Cat read")
		if(first):
			first = False
		else:
			C = cat()
			C.name = row[3]
			C.reg_nr = row[0]
			C.gender = (row[5] == 'Fress')
			if(row[2] != ''):
				date_object = datetime.strptime(row[2], '%d.%m.%Y %H:%M:%S')
				c.registered = date_object.date()
			else:
				c.registered = datetime.now()
			if(row[4] != ''):
				date_object = datetime.strptime(row[2], '%d.%m.%Y %H:%M:%S')
				c.birth = date_object.date()			
			else:
				c.birth = datetime.now()
			C.save()
			print("Cat saved")
#		C = cat();
#		C.name = row[3]
#		C.reg_nr = row[0]
#		if(row[5] == 'Fress'):
#			C.gender = True
#		C.birth
