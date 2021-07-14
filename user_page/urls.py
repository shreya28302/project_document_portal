from django.conf.urls import url
from django.contrib.auth import views as auth_views
from user_page import views

app_name = 'user_page'

urlpatterns = [
    url(r'(?P<pk>\d+)/$', views.UserDashboard, name='userdashboard'),
    url(r'(?P<pk>\d+)/updateprofile/$', views.UpdateProfile, name='updateprofile'),
    url(r'(?P<pk>\d+)/myprofile/$', views.MyProfile, name='myprofile'),
    url(r'search/$',views.Search,name='search'),
    url(r'(?P<username>\w+)/followers$', views.FollowersListView, name='followers'),
    url(r'^(?P<username>[-\w]{5,30})/following/$', views.FollowingListView, name='following'),
    url( r'^(?P<username>[-\w]{5,30})/follow/$', views.follow_view, name='follow'),
    url( r'^(?P<username>[-\w]{5,30})/unfollow/$', views.unfollow_view, name='unfollow'),
]
