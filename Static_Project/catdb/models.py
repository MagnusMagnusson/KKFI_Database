from __future__ import unicode_literals

from django.db import models

# Create your models here.

#People (part 1)

class people(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	id_num = models.CharField(max_length = 30, null = False)
	ssn = models.CharField(max_length = 10)
	address = models.CharField(max_length = 40)
	postal = models.CharField(max_length = 3)
	phone = models.CharField(max_length = 10)
	member_id = models.IntegerField()
	comment = models.CharField(max_length = 144)

class cat_owners(models.Model):
	id = models.AutoField(primary_key = True)
	cat_id = models.ForeignKey('cat', on_delete=models.CASCADE)
	owner_id = models.ForeignKey('people', on_delete=models.CASCADE)
	regdate = models.DateField()

# Cats (part 2)
class cat(models.Model):
	id = models.AutoField(primary_key = True)
	reg_nr = models.CharField(max_length = 5)
	name = models.CharField(max_length = 35)
	gender = models.BooleanField()
	birth = models.DateField()
	registered = models.DateField()
	dam = models.ForeignKey('parents',on_delete=models.CASCADE, related_name = 'dam',null=True,blank = True)
	sire = models.ForeignKey('parents',on_delete=models.CASCADE, related_name = 'sire',null = True,blank = True)
	comments = models.CharField(max_length = 144)
	type = models.CharField(max_length = 3)

class parents(models.Model):
	id = models.AutoField(primary_key = True)
	is_ghost = models.BooleanField()
	cat = models.ForeignKey('cat',on_delete = models.CASCADE,related_name = 'cat_id',null = True,blank = True)
	ghost = models.ForeignKey('ghost_cat',on_delete = models.CASCADE,related_name = 'ghost_id',null=True,blank = True)
	
class ghost_cat(models.Model):
	id = models.AutoField(primary_key = True)
	reg_nr = models.CharField(max_length = 30)
	name = models.CharField(max_length = 50)
	birth = models.DateField()
	microchip = models.CharField(max_length = 30)
	dam = models.ForeignKey('parents',on_delete = models.CASCADE,related_name='ghost_dam')
	sire = models.ForeignKey('parents',on_delete = models.CASCADE,related_name = 'ghost_sire')
	
class imp_cat(models.Model):
    id = models.AutoField(primary_key = True)
    cat = models.ForeignKey('cat',on_delete = models.CASCADE)
    org_country = models.CharField(max_length = 3,null = True)
    org_organization = models.CharField(max_length = 10,null = True)
    org_reg_nr = models.CharField(max_length = 20,null = True)

class EMS(models.Model):
	id = models.AutoField(primary_key = True)
	breed = models.CharField(max_length = 3)
	ems = models.CharField(max_length = 15)
	
class ghost_EMS(models.Model):
	id = models.AutoField(primary_key = True)
	ghost_cat = models.ForeignKey('ghost_cat',on_delete = models.CASCADE)
	ems = models.ForeignKey('EMS',on_delete = models.CASCADE)

class cat_EMS(models.Model):
	id = models.AutoField(primary_key = True)
	cat = models.ForeignKey('cat',on_delete = models.CASCADE)
	ems = models.ForeignKey('EMS',on_delete = models.CASCADE)
	reg_date = models.DateField(null = False)
	
class neutered(models.Model):
	catId = models.OneToOneField('cat')
	date = models.DateField()
	
class microchip(models.Model):
	id = models.AutoField(primary_key = True)
	cat = models.ForeignKey('cat',on_delete = models.CASCADE)
	microchip_nr = models.CharField(max_length = 30)

# PART 3: JUDGES AND SHOWS	
class show(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 30,default=None)
	date = models.DateField(null = False)
	show_orginizer = models.CharField(max_length = 30)

class show_entry(models.Model):   
	class Meta:
		unique_together = (('showId', 'catId'),)
	id = models.AutoField(primary_key = True)
	showId =  models.ForeignKey('show',on_delete = models.CASCADE)
	catId = models.ForeignKey('cat',on_delete = models.CASCADE) 
	cat_show_number = models.IntegerField(null = False) # what number this cat is on the show. 

class litter:
	catId = models.ForeignKey('show_entry',on_delete = models.CASCADE) 
	letterId = models.CharField(max_length = 2)

class judge(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	country = models.CharField(max_length = 3)

class category_judge(models.Model):
	judgeId = models.ForeignKey('judge',on_delete = models.CASCADE) 
	categoryId = models.ForeignKey('category',on_delete = models.CASCADE) 
	
class category(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 10)

class judgement(models.Model):
	id = models.AutoField(primary_key = True)
	entryId = models.ForeignKey('show_entry',on_delete = models.CASCADE)
	showId = models.ForeignKey('show',on_delete = models.CASCADE)
	judge = models.ForeignKey('judge',on_delete = models.CASCADE)
	attendence = models.BooleanField()
	ex = models.IntegerField()
	cert = models.BooleanField()
	biv = models.BooleanField()
	color =  models.ForeignKey('cat_EMS',on_delete = models.CASCADE)
	comment = models.CharField(max_length = 2048)

		
class cert(models.Model):
	id = models.AutoField(primary_key = True)
	certName = models.CharField(max_length = 6, null = False)
	certRank =  models.IntegerField(null = False)
	predecessor = models.ForeignKey('cert',on_delete = models.CASCADE)
	neutered = models.BooleanField()

class judgementLitter(models.Model):
	id = models.AutoField(primary_key = True)
	showId = models.ForeignKey('show',on_delete = models.CASCADE)
	judge = models.ForeignKey('judge',on_delete = models.CASCADE)
	attendence = models.BooleanField()
	rank = models.IntegerField()
	comment = models.CharField(max_length = 2048)
	litter_nr = models.CharField(max_length = 2)
	
class cert_judgement(models.Model):
	id = models.AutoField(primary_key = True)
	cat = models.ForeignKey('cat',on_delete = models.CASCADE)
	judgement = models.ForeignKey('judgement',on_delete = models.CASCADE)
	cert = models.ForeignKey('cert',on_delete = models.CASCADE) 
	date = models.DateField(null = False)
