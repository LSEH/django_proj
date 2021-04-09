from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    SELECT_A = False
    SELECT_B = True
    SELECTS = [
        (SELECT_A, '남자'),
        (SELECT_B, '여자'),
    ]
    gender = forms.ChoiceField(choices=SELECTS, label='성별')
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('gender', 'email',)