from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContentForm, CommentForm, ReviewForm
from .models import Content, Comment, Review
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta
import requests


def index(request):
    contents = Content.objects.all()
    context = {
        'contents' : contents,
    }
    return render(request, 'contents/index.html', context)


def create(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, files=request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.user = request.user
            form.save()
            return redirect('contents:detail', content.pk)
    else:
        form = ContentForm()
    context = {
        'form' : form,
    }
    return render(request, 'contents/form.html', context)


def detail(request, content_id):
    content = get_object_or_404(Content, pk=content_id)
    form = CommentForm()
    reviews = content.review_set.all()
    comments = content.comment_set.all()
    context = {
        'content' : content,
        'form' : form,
        'comments' : comments,
        'reviews' : reviews,
    }
    return render(request, 'contents/detail.html', context)


def update(request, content_id):
    content = get_object_or_404(Content, pk=content_id)
    if request.user == content.user:
        if request.method == 'POST':
            form = ContentForm(request.POST, instance=content, files=request.FILES)
            if form.is_valid():
                content = form.save()
                return redirect('contents:detail', content_id)
        else:
            form = ContentForm(instance=content)
        context = {
            'form' : form,
        }
        return render(request, 'contents/form.html', context)
    else:
        return redirect('contents:detail', content_id)


@require_POST
def delete(request, content_id):
    content = get_object_or_404(Content, pk=content_id)
    if request.user == content.user:
        content.delete()
        return redirect('contents:index')
    else:
        return redirect('contents:detail', content_id)


@require_POST
def create_comment(request, content_id):
    content = get_object_or_404(Content, pk=content_id)
    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content = content
            comment.save()
            return redirect("contents:detail", content_id)
        # context = {
        #     'form' : form,
        # }
        # return render(request, 'contents/detail.html', context)
    return redirect("contents:detail", content_id)


@require_POST
def delete_comment(request, content_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('contents:detail', content_id)


@require_POST
def like_contents(request, content_id):
    if request.user.is_authenticated:
        content = get_object_or_404(Content, pk=content_id)
        if content.like_users.filter(pk=request.user.pk).exists():
            content.like_users.remove(request.user)
        else:
            content.like_users.add(request.user)
        return redirect('contents:detail', content_id)
    else:
        return redirect('accounts:login')


@require_POST
def see_later(request, content_id, review_id):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_id)
        if review.later_users.filter(pk=request.user.pk).exists():
            review.later_users.remove(request.user)
        else:
            review.later_users.add(request.user)
        return redirect('contents:detail', content_id)
    else:
        return redirect('accounts:login')


@require_POST
def like_comments(request, content_id, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_id)
        if comment.like_users.filter(pk=request.user.pk).exists():
            comment.like_users.remove(request.user)
        else:
            comment.like_users.add(request.user)
        return redirect('contents:detail', content_id)
    else:
        return redirect('accounts:login')


def create_review(request, content_id):
    if request.method == 'POST':
        content = Content.objects.get(pk=content_id)
        form = ReviewForm(request.POST, files=request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.content = content
            review.genre = content.genre
            form.save()
            return redirect('contents:detail', content.pk)
    else:
        form = ReviewForm()
    context = {
        'form' : form,
        'content_id' : content_id
    }
    return render(request, 'contents/reviewform.html', context)


@require_POST
def delete_review(request, content_id, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user == review.user:
        review.delete()
    return redirect('contents:detail', content_id)


def update_review(request, content_id, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review, files=request.FILES)
            if form.is_valid():
                review = form.save()
                return redirect('contents:detail', content_id)
        else:
            form = ReviewForm(instance=review)
        context = {
            'form' : form,
        }
        return render(request, 'contents/reviewform.html', context)
    else:
        return redirect('contents:detail', content_id)


@require_POST
def like_reviews(request, content_id, review_id):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_id)
        if review.like_users.filter(pk=request.user.pk).exists():
            review.like_users.remove(request.user)
        else:
            review.like_users.add(request.user)
        return redirect('contents:detail', content_id)
    else:
        return redirect('accounts:login')


def watch_reviews(request, content_id, review_id):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_id)
        review.watched_users.add(request.user)
        return redirect("contents:detail", content_id)
    else:
        return redirect('accounts:login')


def comment_alarm(request):
    contents = request.user.content_set.all()
    today = datetime.now()
    comments = []
    for content in contents:
        data = content.comment_set.filter(created_at__gte=(today - timedelta(days=7)))
        for comment in data:
            comments.append(comment)
    comments.sort(key= lambda x : x.created_at, reverse=True)
    context = {
        'comments' : comments,
    }
    return render(request, 'nav.html', context)


# def youtube():
#     url = ' https://www.googleapis.com/youtube/v3/search'
#     params = {
#         'key': 'AIzaSyDMRR_ZEVgEtxz5rP_dOj-wptDYqqEywdU',
#         'part': 'snippet',
#         'type': 'video',
#         'maxResults': '10',
#         'q': '아이유',
#     }
#     response = requests.get(url, params)
#     response_dict = response.json()

#     print(response_dict['items'])
#     context = {
#         'youtube_items': response_dict['items']
#     }
#     return render(request, 'youtube.html', context)

# youtube()