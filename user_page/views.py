from django.shortcuts import render,redirect
from django.contrib import messages
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.views import generic
from django.contrib.auth.models import User

from .forms import ProfileUpdateForm,SearchForm
from .models import UserProfile,Connection
from files.models import DocumentPost, Download


# Create your views here.
@login_required
def UserDashboard(request, pk):
    context ={}

    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        pass
    else:
        context['profile'] = profile

    context["posts"] = DocumentPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context["followed_by_me"] = Connection.objects.filter(follower=request.user)
    context["who_follows_me"] = Connection.objects.filter(following=request.user)
    context["files"] = DocumentPost.objects.filter(published_date__lte=timezone.now()).filter(author=request.user)
    context["downloads"] = Download.objects.filter(user=request.user)

    return render(request, 'user_page/index.html', context)

@login_required
def MyProfile(request, pk):
    context ={}
    profile_exist = False

    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile:
            profile_exist = True
    except UserProfile.DoesNotExist:
        pass
    else:
        context['profile'] = profile

    user = request.user
    context["user"] = user

    context["followed_by_me"] = Connection.objects.filter(follower=user)
    context["who_follows_me"] = Connection.objects.filter(following=user)
    context["files"] = DocumentPost.objects.filter(published_date__lte=timezone.now()).filter(author=user)
    context["downloads"] = Download.objects.filter(user=user)



    context["profile_exist"] = profile_exist
    if profile_exist:
        context["pro"] = UserProfile.objects.get(user=user)

    return render(request, 'user_page/myprofile.html', context)

@login_required
def UpdateProfile(request, pk):

    profile = False

    if request.method == "POST":
        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass
        else:
            userprofile.delete()

        form = ProfileUpdateForm(request.POST, request.FILES)

        if form.is_valid():

            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('user_page:userdashboard', pk=pk)

    else:
        form = ProfileUpdateForm()

    return render(request, 'user_page/updateprofile.html', { 'formset' : form})


@login_required
def Search(request):
    context = {}
    if request.method=="POST":
        form = SearchForm(request.POST)
        context['form'] = form

        if form.is_valid():
            su=form.cleaned_data['searchuser']

            if su==request.user.username:
                return render(request, 'user_page/search_form.html',{'form': form})

            return redirect('others:dashboard', uname=su)

    else:
        form = SearchForm()
        context['form'] = form

    context['users'] = User.objects.filter()
    context['profiles'] = UserProfile.objects.filter()

    return render(request, 'user_page/search_form.html', context)


@login_required
def FollowersListView(request, username):
    context = {}

    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        pass
    else:
        context['profile'] = profile

    context["users"] = Connection.objects.filter(following__username=username)
    context['stat'] = 'FOLLOWERS'
    return render(request, 'user_page/connections_list.html', context )


@login_required
def FollowingListView(request, username):
    context = {}

    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        pass
    else:
        context['profile'] = profile

    context["users"] = Connection.objects.filter(follower__username=username)
    context['stat'] = 'FOLLOWING'
    return render(request, 'user_page/connections_list.html', context )


@login_required
def follow_view(request, *args, **kwargs):

    try:
        follower = User.objects.get(username=request.user)
        following = User.objects.get(username=kwargs['username'])

    except User.DoesNotExist:
        messages.warning(request, '{} is not a registered user.'.format(kwargs['username']))
        return redirect('user_page:userdashboard', pk=request.user.id)

    if follower == following:
        messages.warning(request, 'You cannot follow yourself.')

    else:
        created = Connection.objects.get_or_create(follower=follower, following=following)

        if (created):
            messages.success(request, 'You have successfully followed {}.'.format(following.username))

        else:
            messages.warning(request, 'You have already followed {}.'.format(following.username))

    return redirect('others:dashboard', uname=following.username)


@login_required
def unfollow_view(request, *args, **kwargs):
    try:
        follower = User.objects.get(username=request.user)
        following = User.objects.get(username=kwargs['username'])

        if follower == following:
            messages.warning(request, 'You cannot unfollow yourself.')

        else:
            unfollow = Connection.objects.get(follower=follower, following=following)
            unfollow.delete()
            messages.success(request, 'You have just unfollowed {}.'.format(following.username))

    except User.DoesNotExist:
        messages.warning(request, '{} is not a registered user.'.format(kwargs['username']))
        return redirect('user_page:userdashboard', pk=request.user.id)
    except Connection.DoesNotExist:
        messages.warning(request, 'You didn\'t follow {0}.'.format(following.username))

    return redirect('others:dashboard', uname=following.username)
