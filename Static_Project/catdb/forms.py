from django import forms 
from catdb.models import judge
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
	organizer = forms.CharField(
		required = False,
		max_length = 30
		)
	date = forms.DateField(required = True, widget=extras.SelectDateWidget(years=range( now.year+2,now.year-2,-1)))
	

class form_show_entry_add(forms.Form):
	cat = forms.CharField(
		required = True,
		max_length = 30
		)
	entry_nr = forms.IntegerField();

class form_show_judge_add(forms.Form):
	judge = forms.CharField(max_length = 50)

class form_show_litter_add(forms.Form):
		litterCat = forms.CharField(
		required = True,
		max_length = 50
		)
		litterLetter = forms.CharField(
		required = True,
		max_length = 2
		)

class form_show_judgement_enter(forms.Form):
	def __init__(self,*args,**kwargs):
		self.show_id = kwargs.pop('show_id')
		super(form_show_judgement_enter,self).__init__(*args,**kwargs)
		self.fields['judge'].queryset = judge.objects.filter(judge_show__showId = self.show_id)


	entryCatId = forms.CharField(
		required = True,
		max_length = 50
		)		

	CatId = forms.CharField(
		max_length = 50,
		label="",
		widget=forms.HiddenInput()
		)	

	entryCatName = forms.CharField(
		disabled = True,
		max_length = 50
		)
	color = forms.CharField(
		disabled = True,
		max_length = 10)
	neutered = forms.BooleanField(disabled = True)
	current_point  = forms.CharField(
		disabled = True,
		max_length = 10)
	next_point  = forms.CharField(
		disabled = True,
		max_length = 10)
	judge = forms.ModelChoiceField(queryset=None)
	abs = forms.BooleanField(initial = False, required = False)
	ex = forms.BooleanField(initial = False, required = False)
	cert = forms.BooleanField(initial = False,  required = False)
	biv = forms.BooleanField(initial = False,  required = False)
	comment = forms.CharField(max_length = 2048,required = False)

	
class form_show_color_judgement_enter(forms.Form):
	entryCatId = forms.CharField(
		required = True,
		max_length = 50
		)		
		
	entryCatName = forms.CharField(
		disabled = True,
		max_length = 50
		)
	color = forms.CharField(
		disabled = True,
		max_length = 10)
	neutered = forms.BooleanField(disabled = True)
	new_EMS = forms.CharField(
		max_length = 10)