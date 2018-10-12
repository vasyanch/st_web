import datetime
from hashlib import md5
# from __future__ import unicode_literals
from django.db import models
# from django.contrib.auth.models import User
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage


class User(models.Model):
    username = models.CharField(max_length = 20, unique=True)
    password = models.CharField(max_length = 20)
    name = models.CharField(max_length = 20)
    email = models.CharField(max_length = 20, unique=True)

    def __str__(self):
        return self.username


class Session(models.Model):
    key = models.CharField(max_length = 200, unique=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    expires = models.DateTimeField(blank=True, auto_now_add=True)


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    likes = models.ManyToManyField(User, related_name='Users')
    objects = QuestionManager()

    def __str__(self):
        return self.text

    def get_url(self):
        return '/question/' + str(self.id) +'/'


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return paginator, page


def do_login(username, password):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    hashed_pass = md5(password.encode('utf-8')).hexdigest()
    if user.password != hashed_pass:
        return None
    session = Session()
    session.key = generate_long_random_key()
    session.user = user
    session.expires = datetime.datetime.now() + datetime.timedelta(days=5)
    session.save()
    return session.key


def generate_long_random_key():
    import random
    ans = []
    z = [chr(i) for i in range(65, 123)]
    while len(ans) < 40:
        f = random.randint(0, 4)
        if f > 3:
            ans.append(str(random.randint(0, 9)))
        else:
            ans.append(random.choice(z))
    return ''.join(ans)