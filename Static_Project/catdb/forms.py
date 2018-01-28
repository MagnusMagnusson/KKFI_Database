from django import forms 
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import extras

genderChoices = ((True,'Male'),(False,'Female'))
ImportedChoices = (('Imported','Imported'),)

class SearchCat(forms.Form):
	now = datetime.datetime.now()
	name = forms.CharField(
		required = False,max_length = 30
		)
	reg_nr = forms.CharField(
		required = False,
		label = "Reg_Nr",
		max_length = 50
		)
	gender = forms.ChoiceField(
		label = "gender",
		required = False, 
		widget = forms.RadioSelect,
		choices = genderChoices
		)
	birth = forms.DateField(required = False, widget=extras.SelectDateWidget(years=range( now.year,1969,-1)))
	registered = forms.DateField(required = False, widget=extras.SelectDateWidget(years=range( now.year,1969,-1)))
	sire = forms.CharField(
		label = "sire",
		max_length = 30,
		required = False
		)
	dam = forms.CharField(
		label = "dam", 
		max_length = 30, 
		required = False
		)
	microchip = forms.CharField(
		label = "chip",
		required = False,
		max_length = 30
		)
#	imp = forms.BooleanField(
#		label = "imported",
#		required = False
#		)
	neut = forms.BooleanField(
		label = "neutered",
		required = False
		)


class AddCat(forms.Form):
	now = datetime.datetime.now()
	name = forms.CharField(
		required = True,
		max_length = 30
		)
	reg_nr = forms.CharField(
		required = True,
		label = "Reg_Nr",
		max_length = 50
		)
	gender = forms.ChoiceField(
		label = "gender",
		required = True, 
		widget = forms.RadioSelect,
		choices = genderChoices
		)
	birth = forms.DateField(required = False, widget=extras.SelectDateWidget(years=range( now.year,now.year-10,-1)))
	registered = forms.DateField(required = False, widget=extras.SelectDateWidget(years=range( now.year,now.year-10,-1)))
	neutered = forms.BooleanField(required = False)
	neutered_Date = forms.DateField(required = False, widget=extras.SelectDateWidget(years=range( now.year,now.year-10,-1)))
	sire = forms.CharField(
		label = "sire",
		max_length = 30,
		required = False,
		)
	dam = forms.CharField(
		label = "dam", 
		max_length = 30, 
		required = False
		)
	microchip = forms.CharField(
		label = "chip",
		required = False,
		max_length = 30
		)

class form_add_show(forms.Form):
	now = datetime.datetime.now()
	name = forms.CharField(
		required = True,
		max_length = 30
		)
	reg_nr = forms.CharField(
		required = True,
		label = "Reg_Nr",
		max_length = 50
		)
	gender = forms.ChoiceField(
		label = "gender",
		required = True, 
		widget = forms.RadioSelect,
		choices = genderChoices
		)
	birth = forms.DateField(required = False, widget=extras.SelectDateWidget(years=range( now.year,now.year-10,-1)))
	registered = forms.DateField(required = False, widget=extras.SelectDateWidget(years=range( now.year,now.year-10,-1)))
	neutered = forms.BooleanField(required = False)
	neutered_Date = forms.DateField(required = False, widget=extras.SelectDateWidget(years=range( now.year,now.year-10,-1)))
	sire = forms.CharField(
		label = "sire",
		max_length = 30,
		required = False,
		)
	dam = forms.CharField(
		label = "dam", 
		max_length = 30, 
		required = False
		)
	microchip = forms.CharField(
		label = "chip",
		required = False,
		max_length = 30
		)

	
	
