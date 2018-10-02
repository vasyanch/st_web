from django import forms


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)






class AddPostForm(forms.Form):
title = forms.CharField(max_length=100)
message = forms.CharField(widget=forms.Textarea)
def clean_message(self):
message = self.cleaned_data['message']
if not is_ethic(message):
raise forms.ValidationError(
u'Сообщение не корректно', code=12)
return message + \
"\nThank you for your attention."
def save(self):
post = Post(**self.