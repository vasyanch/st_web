# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def new(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute('''SELECT text 
                          FROM qa_question
                          ORDER BY added_at DESC''')
        return [i for i in cursor.fetchall()]

    def popular(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execue('''SELECT text 
                         FROM qa_question
                         ORDER BY rating ''')
        return [i for i in cursor.fetchall()]



class Question(models.Model):
    title = models.CharField(max_lenght=255)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True)
    rating = models.IntegerField(default=0)
    author = models.CharField(max_lenght=255)
    likes = models.ManyToManyField(User)


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(blank=True)
    author = models.CharField(max_length=255)
    question = models.ForeignKey(Question)

   
