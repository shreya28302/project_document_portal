from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import DocumentPost, Comment, Like, Dislike, Download
from .forms import DocumentPostForm, CommentForm
from user_page.models import UserProfile

from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied

@login_required
def downloadlist_view(request):
    context ={}
    for pr in UserProfile.objects.all():
        if pr.user == request.user:
            context['profile'] = UserProfile.objects.get(user=request.user)
            break

    context["downloads"] = Download.objects.filter(user=request.user)
    return render(request, "files/download_list.html", context)

@login_required
def postdownload(request, pk):
    try:
        post = get_object_or_404(DocumentPost, id=pk)
        created = Download.objects.get_or_create(post=post, user=request.user)

        if not created:
            messages.warning(request, 'You\'ve already downloaded the post.')

    except DocumentPost.DoesNotExist:
        messages.warning(request, 'post does not exist')

    return redirect('files:post_detail', pk=pk)

@login_required
def postlist_view(request, uname):
    context ={}
    for pr in UserProfile.objects.all():
        if pr.user == request.user:
            context['profile'] = UserProfile.objects.get(user=request.user)
            break

    context["post_list"] = DocumentPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context["uname"] = uname
    return render(request, "files/post_list.html", context)

@login_required
def newpost(request, uname):
    context = {}
    for pr in UserProfile.objects.all():
        if pr.user == request.user:
            context['profile'] = UserProfile.objects.get(user=request.user)
            break

    if request.method == "POST":
        form = DocumentPostForm(request.POST, request.FILES)
        context['form'] = form
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect('user_page:userdashboard', pk=request.user.pk)

    else:
        form = DocumentPostForm()
        context['form'] = form

    return render(request, 'files/post_form.html', context)


@login_required
def postdetail_view(request, pk):
    context ={}
    for pr in UserProfile.objects.all():
        if pr.user == request.user:
            context['profile'] = UserProfile.objects.get(user=request.user)
            break

    context["post"] = DocumentPost.objects.get(id=pk)

    liked = Like.objects.filter(user__username=request.user.username).filter(post__pk=pk)
    disliked = Dislike.objects.filter(user__username=request.user.username).filter(post__pk=pk)

    context['liked'] = True if liked else False
    context['disliked'] = True if disliked else False

    context["likes_no"] = Like.objects.filter(post__pk=pk)
    context["dislikes_no"] = Dislike.objects.filter(post__pk=pk)

    downloaded = Download.objects.filter(user__username=request.user.username).filter(post__pk=pk)
    context["downloaded"] = True if downloaded else False

    return render(request, 'files/post_detail.html', context)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(DocumentPost, id=pk)
    post.publish()
    return redirect('files:post_detail', pk=pk)


@login_required
def postupdate_view(request, pk):
    context = {}
    for pr in UserProfile.objects.all():
        if pr.user == request.user:
            context['profile'] = UserProfile.objects.get(user=request.user)
            break

    obj = get_object_or_404(DocumentPost, id=pk)

    PostForm = DocumentPostForm(request.POST or None, instance = obj)
    context['form'] = PostForm

    if PostForm.is_valid():
        PostForm.save()
        return redirect('files:post_detail', pk=pk)

    return render(request, "files/post_form.html", context)


@login_required
def postdelete_view(request, pk):
    context = {}
    for pr in UserProfile.objects.all():
        if pr.user == request.user:
            context['profile'] = UserProfile.objects.get(user=request.user)
            break

    obj = get_object_or_404(DocumentPost, id = pk)
    context['object'] = obj.title

    if request.method =="POST":
        obj.delete()
        return redirect('files:post_list', uname=request.user.username)

    return render(request, "files/post_delete.html", context)


@login_required
def add_comment_to_post(request, pk):
    context = {}
    for pr in UserProfile.objects.all():
        if pr.user == request.user:
            context['profile'] = UserProfile.objects.get(user=request.user)
            break

    post = get_object_or_404(DocumentPost, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        context['form'] = form
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('files:post_detail', pk=post.pk)
    else:
        form = CommentForm()
        context['form'] = form

    return render(request, 'files/comment_form.html', context)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('files:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('files:post_detail', pk=post_pk)


@login_required
def draftlist_view(request, uname):
    context ={}
    for pr in UserProfile.objects.all():
        if pr.user == request.user:
            context["profile"] = UserProfile.objects.get(user=request.user)
            break

    context["post_list"] = DocumentPost.objects.filter(published_date__isnull=True).order_by('uploaded_at')
    context["uname"] = uname
    return render(request, "files/post_draft.html", context)


@login_required
def like_post_view(request, pk):
    try:
        post = get_object_or_404(DocumentPost, id=pk)
        created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            messages.warning(request, 'You\'ve already liked the post.')

    except DocumentPost.DoesNotExist:
        messages.warning(request, 'post does not exist')

    return redirect('files:post_detail', pk=pk)


@login_required
def unlike_post_view(request, pk):
    try:
        like = Like.objects.get(post__pk = pk, user=request.user)

    except Like.DoesNotExist:
        messages.warning(request, 'You didn\'t like the post.')
    else:
        like.delete()

    return redirect('files:post_detail', pk=pk)

@login_required
def dislike_post_view(request, pk):
    try:
        post = get_object_or_404(DocumentPost, id=pk)
        created = Dislike.objects.get_or_create(post=post, user=request.user)

        if not created:
            messages.warning(request, 'You\'ve already disliked the post.')

    except DocumentPost.DoesNotExist:
        messages.warning(request, 'post does not exist')

    return redirect('files:post_detail', pk=pk)


@login_required
def undislike_post_view(request, pk):
    try:
        dislike = Dislike.objects.get(post__pk = pk, user=request.user)

    except Dislike.DoesNotExist:
        messages.warning(request, 'You didn\'t dislike the post.')
    else:
        dislike.delete()

    return redirect('files:post_detail', pk=pk)

@login_required
def LikersListView(request, pk):
    context = {}
    for pr in UserProfile.objects.all():
        if pr.user == request.user:
            context["profile"] = UserProfile.objects.get(user=request.user)
            break

    post = get_object_or_404(DocumentPost, id=pk)
    context['likers'] = Like.objects.filter(post=post)
    context['title'] = post.title

    return render(request, 'files/likers.html', context)

@login_required
def DislikersListView(request, pk):
    context = {}
    for pr in UserProfile.objects.all():
        if pr.user == request.user:
            context["profile"] = UserProfile.objects.get(user=request.user)
            break

    post = get_object_or_404(DocumentPost, id=pk)
    context['dislikers'] = Dislike.objects.filter(post=post)
    context['title'] = post.title

    return render(request, 'files/dislikers.html', context)
