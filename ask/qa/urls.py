from django.conf.urls import url
from django.contrib import admin

from qa.views import test

urlpatterns = [
    url(r'^login/', test),
    url(r'^signup/', test),
    url(r'^question/123/', test),
    url(r'^ask/', test),
    url(r'^popular/', test),
    url(r'^new/', test),
    url(r'^', test),
]
