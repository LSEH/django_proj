from .models import Content, Comment, Review
from django import forms

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        exclude = ('user', 'like_users',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('content', 'user', 'like_users',)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('content', 'later_users', 'user', 'like_users', 'watched_users', 'genre')