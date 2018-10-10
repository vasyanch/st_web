import datetime
from __future__ import unicode_literals
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


from qa.models import Question, Answer, User, paginate, do_login
from qa.forms import AskForm, AnswerForm


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
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': question.id})
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


# @login_required
def question_add(request):
    if request.method == 'POST':
        form = AskForm(request.POST)  # form = AskForm(request.user, request.POST)
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()    # form = AskForm('''request.user''')
    return render(request, 'question_add.html', {
        'form': form
    }) 


def login(request):
    error = ''
    if request.method == "POST":
        login = request.POST.get('login')
        password = request.POST.get('password')
        url = request.POST.get('continue', '/')
        sessionid = do_login(login, password)
        if sessionid:
            response = HttpResponseRedirect(url)
            response.set_cookie('sessionid', sessionid, httponly=True, expires=datetime.now()+datetime.timedelta(days=5))
            return response
        else:
            error = u'Неверный логин/пароль'
    return render(request, 'login.html', {'error': error})


def signup(request):
    if request.method == 'POST':

    else:

    return render(request, 'signup.html', {form: 'form'})