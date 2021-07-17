from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from files.models import DocumentPost, Comment, Like, Dislike, Download
from files.forms import DocumentPostForm, CommentForm

from user_page.models import Connection, UserProfile

from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
# Create your views here.

@login_required
def dashboard(request, uname):
    context ={}
    context["uname"] = uname

    if uname is not request.user.username:
        result = Connection.objects.filter(follower__username=request.user.username).filter(following__username=uname)

    context['connected'] = True if result else False

    context["followed_by_uname"] = Connection.objects.filter(follower__username=uname)
    context["who_follows_uname"] = Connection.objects.filter(following__username=uname)
    context["files"] = DocumentPost.objects.filter(published_date__lte=timezone.now()).filter(author__username=uname)
    for pr in UserProfile.objects.all():
        if pr.user == request.user:
            context['profile'] = UserProfile.objects.get(user=request.user)
            break

    for pr in UserProfile.objects.all():
        if pr.user.username == uname:
            profile = UserProfile.objects.get(user__username=uname)
            context["profile_exist"] = True if profile else False
            context["pro"] = profile
            break

    return render(request, 'others/index.html', context)

@login_required
def postlist_view(request, uname):
    context ={}
    for pr in UserProfile.objects.all():
        if pr.user == request.user:
            context['profile'] = UserProfile.objects.get(user=request.user)
            break

    context["post_list"] = DocumentPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context["uname"] = uname
    return render(request, "others/post_list.html", context)

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

    return render(request, 'others/post_detail.html', context)

@login_required
def postdownload(request, pk):
    try:
        post = get_object_or_404(DocumentPost, id=pk)
        created = Download.objects.get_or_create(post=post, user=request.user)

        if not created:
            messages.warning(request, 'You have already downloaded the post.')

    except DocumentPost.DoesNotExist:
        messages.warning(request, 'post does not exist')

    return redirect('others:post_detail', pk=pk)

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
            return redirect('others:post_detail', pk=post.pk)
    else:
        form = CommentForm()
        context['form'] = form

    return render(request, 'others/comment_form.html', context)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('others:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('others:post_detail', pk=post_pk)


@login_required
def like_post_view(request, pk):
    try:
        post = get_object_or_404(DocumentPost, id=pk)
        created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            messages.warning(request, 'You have already liked the post.')

    except DocumentPost.DoesNotExist:
        messages.warning(request, 'post does not exist')

    return redirect('others:post_detail', pk=pk)


@login_required
def unlike_post_view(request, pk):
    try:
        like = Like.objects.get(post__pk = pk, user=request.user)

    except Like.DoesNotExist:
        messages.warning(request, 'You didn\'t like the post.')
    else:
        like.delete()

    return redirect('others:post_detail', pk=pk)

@login_required
def dislike_post_view(request, pk):
    try:
        post = get_object_or_404(DocumentPost, id=pk)
        created = Dislike.objects.get_or_create(post=post, user=request.user)

        if not created:
            messages.warning(request, 'You have already disliked the post.')

    except DocumentPost.DoesNotExist:
        messages.warning(request, 'post does not exist')

    return redirect('others:post_detail', pk=pk)


@login_required
def undislike_post_view(request, pk):
    try:
        dislike = Dislike.objects.get(post__pk = pk, user=request.user)

    except Dislike.DoesNotExist:
        messages.warning(request, 'You didn\'t dislike the post.')
    else:
        dislike.delete()

    return redirect('others:post_detail', pk=pk)


@login_required
def LikersListView(request, pk):
    context = {}
    for pr in UserProfile.objects.all():
        if pr.user == request.user:
            context['profile'] = UserProfile.objects.get(user=request.user)
            break

    post = get_object_or_404(DocumentPost, id=pk)
    context['likers'] = Like.objects.filter(post=post)
    context['title'] = post.title

    return render(request, 'others/likers.html', context)

@login_required
def DislikersListView(request, pk):
    context = {}
    for pr in UserProfile.objects.all():
        if pr.user == request.user:
            context['profile'] = UserProfile.objects.get(user=request.user)
            break

    post = get_object_or_404(DocumentPost, id=pk)
    context['dislikers'] = Dislike.objects.filter(post=post)
    context['title'] = post.title

    return render(request, 'others/dislikers.html', context)
