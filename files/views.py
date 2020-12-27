from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import DocumentPost, Comment, Like, Dislike
from .forms import DocumentPostForm, CommentForm

from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied

@login_required
def postlist_view(request, uname):
    context ={}
    context["post_list"] = DocumentPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context["uname"] = uname
    return render(request, "files/post_list.html", context)

@login_required
def newpost(request, uname):

    if request.method == "POST":
        form = DocumentPostForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect('files:post_list', uname=uname)

    else:
        form = DocumentPostForm()

    return render(request, 'files/post_form.html', { 'form': form, })


@login_required
def postdetail_view(request, pk):
    context ={}
    context["post"] = DocumentPost.objects.get(id=pk)
    return render(request, 'files/post_detail.html', context)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(DocumentPost, id=pk)
    post.publish()
    return redirect('files:post_detail', pk=pk)


@login_required
def postupdate_view(request, pk):

    obj = get_object_or_404(DocumentPost, id=pk)

    PostForm = DocumentPostForm(request.POST or None, instance = obj)

    if PostForm.is_valid():
        PostForm.save()
        return redirect('files:post_detail', pk=pk)

    return render(request, "files/post_form.html", {'form' : PostForm})


@login_required
def postdelete_view(request, pk):

    obj = get_object_or_404(DocumentPost, id = pk)
    object = obj.title

    if request.method =="POST":
        obj.delete()
        return redirect('files:post_list', uname=request.user.username)

    return render(request, "files/post_delete.html", {'object' : object})


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(DocumentPost, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('files:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'files/comment_form.html', {'form': form})


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


#@login_required
#def unlike_post_view(request, pk):
#    try:
#        like = Like.objects.get(post__pk = pk, user=request.user)

#    except Like.DoesNotExist:
#        messages.warning(request, 'You didn\'t like the post.')
#    else:
#        like.delete()

#    return redirect('files:post_detail', pk=pk)

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


#@login_required
#def undislike_post_view(request, pk):
#    try:
#        dislike = Dislike.objects.get(post__pk = pk, user=request.user)

#    except Dislike.DoesNotExist:
#        messages.warning(request, 'You didn\'t dislike the post.')
#    else:
#        dislike.delete()

#    return redirect('files:post_detail', pk=pk)


class LikersListView(LoginRequiredMixin, generic.ListView):
    model = Like
    template_name = 'files/likers.html'
    context_object_name = 'likers'

    def get_queryset(self):
        pk = self.kwargs['pk']
        post = get_object_or_404(DocumentPost, id=pk)
        return Like.objects.filter(user__username=post.author.username)

    def get_context_data(self):
        context = super(LikersListView, self).get_context_data()
        pk = self.kwargs['pk']
        post = get_object_or_404(DocumentPost, id=pk)
        context['title'] = post.title
        return context


class DislikersListView(LoginRequiredMixin, generic.ListView):
    model = Dislike
    template_name = 'files/dislikers.html'
    context_object_name = 'dislikers'

    def get_queryset(self):
        pk = self.kwargs['pk']
        post = get_object_or_404(DocumentPost, id=pk)
        return Dislike.objects.filter(user__username=post.author.username)

    def get_context_data(self):
        context = super(DislikersListView, self).get_context_data()
        pk = self.kwargs['pk']
        post = get_object_or_404(DocumentPost, id=pk)
        context['title'] = post.title
        return context
