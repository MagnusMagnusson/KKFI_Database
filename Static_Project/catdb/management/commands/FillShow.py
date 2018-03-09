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
		parser.add_argument('Show', nargs='+', type=str)
		parser.add_argument('Orginizer', nargs='+', type=str)
		parser.add_argument('Date', nargs='+', type=str)
		parser.add_argument('File', nargs='+', type=str)
	@transaction.atomic
	def handle(self, *args, **options):
		_show = show()
		_show.name = options['Show'][0]
		_show.show_orginizer = options['Orginizer'][0]
		_show.date = datetime.strptime(options['Date'][0], "%d.%m.%Y").date()
		_show.save()

		with open(options['File'][0], 'rb') as lengthfile:
			lengthreader =  unicode_csv_reader(lengthfile, quotechar='"')
			Length = sum(1 for row in lengthreader)
			print("Length recorded as " + str(Length))
		lengthfile.close()

		with open(options['File'][0], 'rb') as csvfile:
			spamreader = unicode_csv_reader(csvfile, quotechar='"')
			print("loaded")
			done = 0
			for row in spamreader:
				entry = show_entry()
				entry.showId = _show
				entry.catId = cat.objects.get(reg_nr = row[0])
				entry.cat_show_number = done + 1
				done += 1
				entry.save()


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

