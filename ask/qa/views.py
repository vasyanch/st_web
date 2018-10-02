# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from qa.models import Question, Answer, User, paginate


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def home(request):
    new_questions = Question.objects.new()
    paginator, page = paginate(request, new_questions)
    paginator.baseurl = '/?page='
    return render(request, 'list_questions.html', {
        'list_questions' : page.object_list,
        'paginator' : paginator,
        'page' : page,
    })

def question_details(request, id):
    #try:
    #   question = Question.objects.get(id=id)
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


def popular_questions(request):
    popular_questions = Question.objects.popular()
    paginator, page = paginate(request, popular_questions)
    paginator.baseurl = '/popular/?page='
    return render(request, 'list_questions.html', {
        'list_questions' : page.object_list,
        'paginator' : paginator,
        'page' : page,
    })
