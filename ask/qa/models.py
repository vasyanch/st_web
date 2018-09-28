# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def new(self):
        ans = self.order_by('-added_at')
        return ans[0:10]

    def popular(self):
        ans = self.order_by('rating')
        return ans[0:10]



class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User)
    likes = models.ManyToManyField(User, related_name='users_set')
    objects = QuestionManager()


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(blank=True)
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)
