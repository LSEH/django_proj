from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.db.models import Count, Max
from .forms import CustomUserCreationForm, CustomUserChangeForm
from contents.models import Review
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta


def signup(request):
    if not request.user.is_authenticated:
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
    else:
        return HttpResponse(status=405)



def login(request):
    if request.user.is_authenticated:
        return redirect('contents:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            if relativedelta(datetime.now(timezone.utc), form.get_user().password_date).days > 15:
                return redirect('accounts:password_alarm')
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
                user_info = form.save(commit=False)
                if nickname != user_info.nickname:
                    user_info.nickname_date = datetime.now()
                user_info.save()
                return redirect('accounts:profile', user_info.nickname)
        else:
            form = CustomUserChangeForm(instance=request.user)
            date_period = 15 - relativedelta(datetime.now(timezone.utc), request.user.nickname_date).days
        
        context = {
            'form' : form,
            'date_period' : date_period,
        }
        return render(request, 'accounts/profile.html', context)
    else:
        return HttpResponse(status=405)


def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user_info = form.save(commit=False)
            user_info.password_date = datetime.now()
            user_info.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:profile', user_info.nickname)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form,
    }
    return render(request, 'accounts/password.html', context)


def mylike(request, nickname):
    if request.user.nickname == nickname:
        user = get_object_or_404(get_user_model(), nickname=nickname)
        like_contents = user.like_contents.all()
        like_reviews = user.like_reviews.all()
        context = {
            'like_contents' : like_contents,
            'like_reviews' : like_reviews,
        }
        return render(request, 'accounts/mydata.html', context)
    else:
        return HttpResponse(status=404)


def mylater(request, nickname):
    if request.user.nickname == nickname:
        user = get_object_or_404(get_user_model(), nickname=nickname)
        later_reviews = user.later_reviews.all()
        context = {
            'later_reviews' : later_reviews,
        }
        return render(request, 'accounts/mydata.html', context)
    else:
        return HttpResponse(status=404)


def mystats(request, nickname):
    if request.user.nickname == nickname:
        watched_reviews = request.user.watched_reviews.all()
        if not watched_reviews:
            max_genre = '데이터가 없습니다.'
            watched_reviews_num = 0
        else:
            max_genre = watched_reviews.values('genre').annotate(genre_count=Count('genre')).latest('genre_count').get('genre')
            watched_reviews_num = watched_reviews.count()
        total_reviews = Review.objects.all().count()
        comments = request.user.comment_set.order_by('-pk')
        context = {
            'max_genre' : max_genre,
            'total_reviews' : total_reviews,
            'watched_reviews_num' : watched_reviews_num,
            'comments' : comments,
        }
        return render(request, 'accounts/mydata.html', context)
    else:
        return HttpResponse(status=404)


def password_alarm(request):
    return render(request, 'accounts/password_alarm.html')