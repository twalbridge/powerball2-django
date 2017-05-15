from django.conf.urls import url

from .views import (EntryCreateView, EntryListView, PopularEntryView)


app_name = 'playball'
urlpatterns = [

    url(r'^entry_list/$', EntryListView.as_view(), 
    	name="entry_list"),	
    url(r'^popular_entry/$', PopularEntryView.as_view(), 
    	name="popular_entry"),
    url(r'^entry/create/$', EntryCreateView.as_view(), 
    	name="entry_create"),	
]
