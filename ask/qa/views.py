from __future__ import unicode_literals
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, AnonymousUser

from qa.models import Question, Answer, paginate
from qa.forms import AskForm, AnswerForm, SignupForm


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def home(request):
    new_questions = Question.objects.new()
    paginator, page = paginate(request, new_questions)
    paginator.baseurl = '/?page='
    if request.user is not AnonymousUser:
        username = request.user.username
    else:
        username = None
    return render(request, 'list_questions.html', {
        'list_questions': page.object_list,
        'paginator': paginator,
        'page': page,
        'username': username,
    })


def question_details(request, id_):
    # try:
    #    question = Question.objects.get(id=id)
    # except Question.DoesNotExist:
    #     raise Http404
    question = get_object_or_404(Question, id=id_)
    try:
        answer = Answer.objects.filter(question_id=question.id)
    except Answer.DoesNotExist:
        answer = None
    if request.method == 'POST':
        form = AnswerForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(request.user, initial={'question': question.id})
    return render(request, 'question_details.html', {
        'question': question,
        'answer': answer,
        'form': form,
    })


def popular(request):
    popular_questions = Question.objects.popular()
    paginator, page = paginate(request, popular_questions)
    paginator.baseurl = '/popular/?page='
    return render(request, 'list_questions.html', {
        'list_questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })


def question_add(request):
    if request.method == 'POST':
        form = AskForm(request.user, request.POST)
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm(request.user)
    return render(request, 'question_add.html', {
        'form': form
    }) 


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            url = request.POST.get('continue', '/')
            return HttpResponseRedirect(url)

    else:
        form = SignupForm()
    return render(request, 'signup.html', {
        'form': form
    })


def login_(request):
    error = ''
    form = SignupForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            url = request.POST.get('continue', '/')
            return HttpResponseRedirect(url)
        else:
            error = u'Неправильный пользователь или пароль'.encode('utf-8')
    return render(request, 'login.html', {
        'form': form,
        'error': error,
    })