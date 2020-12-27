from django.shortcuts import render,redirect
from django.contrib import messages
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.views import generic
from django.contrib.auth.models import User

from .models import UserProfile,Connection
from files.models import DocumentPost

from .forms import ProfileUpdateForm,SearchForm

from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied

# Create your views here.
@login_required
def UserDashboard(request, pk):
    context ={}
    there = 0
    for pr in UserProfile.objects.all():
        if pr.user_id == pk:
            there = 1
            break

    if there==1:
        context["pro"] = UserProfile.objects.get(user_id=pk)

    context["posts"] = DocumentPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context["followed_by_me"] = Connection.objects.filter(follower=request.user)

    return render(request, 'user_page/index.html', context)


@login_required
def UpdateProfile(request, pk):

    user = User.objects.get(pk=pk)

    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('phone_no', 'first_name', 'last_name', 'image'))

    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if formset.is_valid():
                formset.save()
                return redirect('user_page:userdashboard', pk=pk)

        else:
            formset = ProfileInlineFormset(instance=user)
        return render(request, 'user_page/updateprofile.html', { "formset": formset, })
    else:
        raise PermissionDenied


@login_required
def Search(request):
    if request.method=="POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            su=form.cleaned_data['searchuser']
            return redirect('others:dashboard', uname=su)

    else:
        form = SearchForm()

    return render(request, 'user_page/search_form.html',{'form': form})


class FollowersListView(LoginRequiredMixin, generic.ListView):
    model = Connection
    template_name = 'user_page/connections_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        username = self.kwargs['username']
        return Connection.objects.filter(following__username=username)

    def get_context_data(self):
        context = super(FollowersListView, self).get_context_data()
        context['stat'] = 'FOLLOWERS'
        return context


class FollowingListView(LoginRequiredMixin, generic.ListView):
    model = Connection
    template_name = 'user_page/connections_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        username = self.kwargs['username']
        return Connection.objects.filter(follower__username=username)

    def get_context_data(self):
        context = super(FollowingListView, self).get_context_data()
        context['stat'] = 'FOLLOWING'
        return context


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
            messages.success(request, 'You\'ve successfully followed {}.'.format(following.username))

        else:
            messages.warning(request, 'You\'ve already followed {}.'.format(following.username))

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
            messages.success(request, 'You\'ve just unfollowed {}.'.format(following.username))

    except User.DoesNotExist:
        messages.warning(request, '{} is not a registered user.'.format(kwargs['username']))
        return redirect('user_page:userdashboard', pk=request.user.id)
    except Connection.DoesNotExist:
        messages.warning(request, 'You didn\'t follow {0}.'.format(following.username))

    return redirect('others:dashboard', uname=following.username)
