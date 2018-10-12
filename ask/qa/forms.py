from __future__ import unicode_literals
from django import forms
from qa.models import Question, Answer, User
from hashlib import md5


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(AskForm, self).__init__(*args, **kwargs)

    def clean(self):
        #if self._user.is_banned:
         #   raise ValidationError(u'Доступ ограничен')            
        return self.cleaned_data
    
    def save(self):
        self.cleaned_data['author'] = self._user
        question = Question(**self.cleaned_data)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean_question(self):
        q_id = self.cleaned_data['question']
        try:
            question = Question.objects.get(id=q_id)
        except Question.DoesNotExist:
            question = None
        return question

    def clean(self):
        return self.cleaned_data

    def save(self):
        self.cleaned_data['author'] = self._user
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer


class SignupForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())

    def clean_password(self):
        p = self.cleaned_data['password']
        return md5(p.encode('utf-8')).hexdigest()

    def clean(self):
        return self.cleaned_data

    def save(self):
        user = User(**self.cleaned_data)
        user.save()
        return user


