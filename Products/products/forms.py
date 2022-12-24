from django import forms
from django.forms import ModelForm
from .models import *

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']

class Crowd_Form(forms.ModelForm):
    class Meta:
        model = Crowd_Funding
        fields = '__all__'

class Edit_Crowd_Form(forms.ModelForm):
    class Meta:
        model = Crowd_Funding
        fields = '__all__'