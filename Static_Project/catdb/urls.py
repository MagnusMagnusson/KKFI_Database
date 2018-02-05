from django.conf.urls import url

from . import views

urlpatterns = [
	#HTML REQUESTS
    url(r'^(index)*$', views.index, name='index'),
    url(r'^search/.*', views.search, name='search'),
	url(r'^cat/.*',views.catview, name='catview'),
    url(r'^findcat/.*', views.findcat, name='findcat'),
    url(r'^addcat/.*', views.addcat, name='addcat'),
    url(r'^shows/new', views.addshow, name='addshow'),
    url(r'^shows/register', views.view_ShowRegisterEntry, name='view_ShowRegisterEntry'),
    url(r'^shows/.*', views.findshow, name='findshow'),

	#JSON REQUESTS
	url(r'^api/create_show/', views.api_create_show, name='api_create_show'),
	url(r'^api/shows/register', views.api_show_entry_register, name='api_show_entry_register'),
	url(r'^form_cat/', views.form_cat, name='form_cat'),
	url(r'^find_cat_name/', views.find_cat_names, name='find_cat_names'),
    
	#Uhhh... Idk.
	url(r'^kitty$', views.kitty, name='kitty'),
] 
