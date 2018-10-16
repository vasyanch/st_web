from qa.models import Session
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin


class CheckSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            sessionid = request.COOKIE.get('sessionid')
            session = Session.objects.get(
                key=sessionid,
                expires__gt=datetime.now(),
            )
            request.session = session
            request.user = session.user
        except (Session.DoesNotExist, AttributeError):
            request.session = None
            request.user = None
