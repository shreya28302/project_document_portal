from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from others import views

app_name = 'others'

urlpatterns = [
    url(r'^(?P<uname>\w+)/$',views.dashboard,name='dashboard'),
    url(r'^(?P<uname>\w+)/list/$',views.postlist_view,name='post_list'),
    url(r'^post/(?P<pk>\d+)$', views.postdetail_view, name='post_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
