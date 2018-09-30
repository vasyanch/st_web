# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from qa.models import Question, Answer, User


def test(request, *args, **kwargs):
    return HttpResponse('OK')


#def main(request):
 #   ans = Question.objects.new()


def question_details(request, id):
    #try:
    #   question = Question.objects.get(slug=slug)
    #except Question.DoesNotExist:
    #    raise Http404
    question = get_object_or_404(Question, id=id)
    try:
        answer = Answer.objects.filter(question_id=question.id)
    except Answer.DoesNotExist:
        answer = None
    return render(request, 'question_details.html', {
        'question': question,
        'answer' : answer,
    })
