from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from user_page import views

app_name = 'user_page'

urlpatterns = [
    url(r'(?P<pk>\d+)/$', views.UserDashboard, name='userdashboard'),
    url(r'(?P<pk>\d+)/updateprofile/$', views.UpdateProfile, name='updateprofile'),
    url(r'search/$',views.Search,name='search'),
    url(r'(?P<username>\w+)/followers$', views.FollowersListView.as_view(), name='followers'),
    url(r'^(?P<username>[-\w]{5,30})/following/$', views.FollowingListView.as_view(), name='following'),
    url( r'^(?P<username>[-\w]{5,30})/follow/$', views.follow_view, name='follow'),
    url( r'^(?P<username>[-\w]{5,30})/unfollow/$', views.unfollow_view, name='unfollow'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
