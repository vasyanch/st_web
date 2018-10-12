from __future__ import unicode_literals
import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


from qa.models import Question, Answer, User, Session, paginate, do_login
from qa.forms import AskForm, AnswerForm, SignupForm


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def home(request):
    new_questions = Question.objects.new()
    paginator, page = paginate(request, new_questions)
    paginator.baseurl = '/?page='
    return render(request, 'list_questions.html', {
        'list_questions': page.object_list,
        'paginator': paginator,
        'page': page,
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


def question_details(request, id):
    # try:
    #    question = Question.objects.get(id=id)
    # except Question.DoesNotExist:
    #     raise Http404
    question = get_object_or_404(Question, id=id)
    try:
        answer = Answer.objects.filter(question_id=question.id)
    except Answer.DoesNotExist:
        answer = None
    sessionid = request.COOKIES.get('sessionid')
    user = Session.objects.get(key=sessionid).user
    if request.method == 'POST':
        form = AnswerForm(user, request.POST)
        if form.is_valid():
            form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(user, initial={'question': question.id})
    return render(request, 'question_details.html', {
        'question': question,
        'answer': answer,
        'form': form,
    })





# @login_required
def question_add(request):
    sessionid = request.COOKIES.get('sessionid')
    user = Session.objects.get(key=sessionid).user
    if request.method == 'POST':
        form = AskForm(user, request.POST)
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm(user)
    return render(request, 'question_add.html', {
        'form': form
    }) 


def login(request):
    error = ''
    form = SignupForm()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        url = request.POST.get('continue', '/')
        sessionid = do_login(username, password)
        if sessionid:
            response = HttpResponseRedirect(url)
            response.set_cookie('sessionid', sessionid, httponly=True,
                    expires=datetime.datetime.now()+datetime.timedelta(days=5))
            return response
        else:
            error = u'Неверный логин/пароль'
    return render(request, 'login.html', {
        'form': form,
        'error': error
    })


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            sessionid = do_login(request.POST.get('username'), request.POST.get('password'))
            response = HttpResponseRedirect('/')
            response.set_cookie('sessionid', sessionid, httponly=True,
                                expires=datetime.datetime.now()+datetime.timedelta(days=5))
            return response
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
