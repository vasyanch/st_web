from django import forms
from qa.models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    #def __init__(self, user, *args, **kwargs):
     #   self._user = user
     #   super(AskForm, self).__init__(*args, **kwargs)

    def clean(self):
        #if self._user.is_banned:
         #   raise ValidationError(u'Доступ ограничен')            
        return self.cleaned_data
    
    def save(self):
        #self.cleaned_data['author'] = self._user
        question = Question(**self.cleaned_data)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

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
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer


class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=password)
