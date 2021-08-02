from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile, Comment, Rating


class CustomerForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)
        exclude = ['user']


class CommentForm(ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'комментарий...', 'rows': '4', 'cols':'50'}))
    class Meta:
        model = Comment
        fields = ('content',)

class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ('vote',)
        widgets = { 'vote': forms.RadioSelect() }