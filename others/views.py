from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from files.models import DocumentPost, Comment

from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
# Create your views here.

@login_required
def dashboard(request, uname):
    context ={}
    context["uname"] = uname
    return render(request, 'others/index.html', context)

@login_required
def postlist_view(request, uname):
    context ={}
    context["post_list"] = DocumentPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context["uname"] = uname
    return render(request, "others/post_list.html", context)

@login_required
def postdetail_view(request, pk):
    context ={}
    context["post"] = DocumentPost.objects.get(id=pk)
    return render(request, 'others/post_detail.html', context)
