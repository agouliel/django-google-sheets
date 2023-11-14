from django import forms
from .models import *

class NameForm(forms.Form):
  your_name = forms.CharField(label="Your name", max_length=100)
  descr = forms.CharField(label='Description', max_length=1000)
  pic_url = forms.CharField(label='Photo URL', max_length=1000)

class PostForm(forms.ModelForm):
  class Meta:
    model = Photos
    fields = ['title', 'description', 'url']