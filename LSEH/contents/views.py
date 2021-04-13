from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContentForm, CommentForm
from .models import Content
from django.views.decorators.http import require_POST


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
    comments = content.comment_set.all()
    context = {
        'content' : content,
        'form' : form,
        'comments' : comments,
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