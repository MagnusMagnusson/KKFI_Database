from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^api/file/nomtag', views.api_file_nomtags, name='api_person_register'),
	url(r'^form_cat', views.form_cat, name='form_cat'),
	url(r'^find_cat_name', views.find_cat_names, name='find_cat_names'),
	#Uhhh... Idk.
	url(r'^kitty$', views.kitty, name='kitty'),
	url(r'^404', views.fourohfour, name='fourohfour'),
] 
