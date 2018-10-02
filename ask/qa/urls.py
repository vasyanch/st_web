from django.conf.urls import url

from qa.views import test, question_details, popular, home

urlpatterns = [
    url(r'^login/$', test),
    url(r'^signup/$', test),
    url(r'^question/(?P<id>\w+)/$', question_details, name='question_details'),
    url(r'^ask/$', test),
    url(r'^popular/$', popular, name='popular'),
    url(r'^new/$', test),
    url(r'^$', home, name='home'),
]
