from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from playball.views import (EntryListView, EntryCreateView)

urlpatterns = [
    url(r"^$", EntryCreateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^403/", TemplateView.as_view(template_name="403.html"), name="403"),
    url(r"^404/", TemplateView.as_view(template_name="403.html"), name="404"),
    url(r"^500/", TemplateView.as_view(template_name="403.html"), name="500"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^playball/", include("playball.urls")),
]
