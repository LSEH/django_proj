from .models import Content, Comment
from django import forms

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        exclude = ('user',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('content', 'user',)

        