from django.conf.urls import url

from qa.views import test, question_details, popular, home
from qa.views import question_add, login, signup

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^question/(?P<id>\w+)/$', question_details, name='question_details'),
    url(r'^ask/$', question_add, name='question_add'),
    url(r'^popular/$', popular, name='popular'),
    url(r'^new/$', test),
    url(r'^$', home, name='home'),
]
