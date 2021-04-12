from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.views.decorators.http import require_POST


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('contents:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/signup.html', context)
    

def login(request):
    if request.user.is_authenticated:
        return redirect('contents:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('contents:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('contents:index')


def profile(request, nickname):
    user = get_user_model()
    if request.user == user.objects.get(nickname=nickname):
        if request.method == 'POST':
            form = CustomUserChangeForm(data=request.POST, instance=request.user)
            if form.is_valid():
                user_info = form.save()
                return redirect('accounts:profile', user_info.nickname)
        else:
            form = CustomUserChangeForm(instance=request.user)
        context = {
            'form' : form,
        }
        return render(request, 'accounts/profile.html', context)


def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user_info = form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:profile', user_info.nickname)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form,
    }
    return render(request, 'accounts/password.html', context)

