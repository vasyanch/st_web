from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage


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
