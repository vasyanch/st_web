from django.conf.urls import url
from django.contrib import admin

from qa.views import test, question_details

urlpatterns = [
    url(r'^login/$', test),
    url(r'^signup/$', test),
    url(r'^question/(?P<id>\w+)/$', question_details, name='question_details'),
    url(r'^ask/$', test),
    url(r'^popular/$', test),
    url(r'^new/$', test),
    url(r'^$', test),
]
