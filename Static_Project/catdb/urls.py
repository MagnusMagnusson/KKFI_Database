from django.conf.urls import url

from . import views

urlpatterns = [
	#HTML REQUESTS
    url(r'^(index)*$', views.index, name='index'),

	url(r'^cats/cat/?$',views.catview, name='catview'),
    url(r'^cats/search/?$', views.search, name='search'),
    url(r'^cats/find/?$', views.findcat, name='findcat'),
    url(r'^cats/register/?$', views.addcat, name='addcat'),
    url(r'^cats/edit/?$', views.editCat, name='editCat'),

    url(r'^person/register/?$', views.addPerson, name='addPerson'),

    url(r'^cattery/register/?$', views.addCattery, name='addCattery'),

    url(r'^shows/new/?$', views.addshow, name='addshow'),
    url(r'^shows/setup/?$', views.view_ShowSetup, name='view_ShowSetup'),
    url(r'^shows/manage/?$', views.view_ShowManage, name='view_ShowManage'),
    url(r'^shows/judgements/delete/?$', views.view_DeleteJudgements, name='view_DeleteJudgements'),
    url(r'^shows/judgements/edit/?$', views.view_EditJudgements, name='view_EditJudgements'),
    url(r'^shows/judgements/?$', views.view_ShowJudgements, name='view_ShowJudgements'),
    url(r'^shows/nominations/view/?$', views.view_ShowNominations, name='view_ShowNominations'),
    url(r'^shows/nominations/cvs/?$', views.view_ShowNominations, name='view_ShowNominations'),
    url(r'^shows/contestants/?$', views.view_ShowViewEntries, name='view_ShowViewEntries'),
	url(r'^shows/?$', views.findshow, name='findshow'),

	#JSON REQUESTS
	url(r'^api/create_show', views.api_create_show, name='api_create_show'),
	url(r'^api/cats/edit', views.api_cat_edit, name='api_cat_edit'),
	url(r'^api/cattery/register', views.api_cattery_register, name='api_cattery_register'),
	url(r'^api/shows/register', views.api_show_entry_register, name='api_show_entry_register'),
	url(r'^api/shows/find_entry_name', views.api_entry_search_name, name='api_entry_search_name'),
	url(r'^api/shows/litter_register', views.api_show_litter_entry_register, name='api_show_litter_entry_register'),
	url(r'^api/shows/judge_register', views.api_show_judge_register, name='api_show_judge_register'),
	url(r'^api/shows/enterColorJudgement', views.api_show_enter_color_judgement, name='api_show_enter_color_judgement'),
	url(r'^api/shows/getEntryInfo', views.api_entry_get_info, name='api_entry_get_info'),
	url(r'^api/shows/enterJudgement', views.api_show_enter_judgement, name='api_show_enter_judgement'),
	url(r'^api/shows/editJudgement', views.api_show_edit_judgement, name='api_show_edit_judgement'),
	url(r'^api/shows/enterLitterJudgement', views.api_show_enter_litter_judgement, name='api_show_enter_litter_judgement'),
	url(r'^api/judge/find_judge_name', views.api_judge_search_name, name='api_judge_search_name'),
	url(r'^api/persons/register', views.api_person_register, name='api_person_register'),
	url(r'^api/file/nomtag', views.api_file_nomtags, name='api_person_register'),

	url(r'^form_cat', views.form_cat, name='form_cat'),
	url(r'^find_cat_name', views.find_cat_names, name='find_cat_names'),
    
	#Uhhh... Idk.
	url(r'^kitty$', views.kitty, name='kitty'),
	url(r'^404', views.fourohfour, name='fourohfour'),
] 
