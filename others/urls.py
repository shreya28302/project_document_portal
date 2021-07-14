from django.conf.urls import url
from django.contrib.auth import views as auth_views
from others import views

app_name = 'others'

urlpatterns = [
    url(r'^(?P<uname>\w+)/$',views.dashboard,name='dashboard'),
    url(r'^(?P<uname>\w+)/list/$',views.postlist_view,name='post_list'),
    url(r'^post/(?P<pk>\d+)$', views.postdetail_view, name='post_detail'),
    url(r'^post/(?P<pk>\d+)/download/$', views.postdownload, name='downloadpost'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^post/(?P<pk>\d+)/like/$', views.like_post_view, name='like'),
    url(r'^post/(?P<pk>\d+)/unlike/$', views.unlike_post_view, name='unlike'),
    url(r'^post/(?P<pk>\d+)/dislike/$', views.dislike_post_view, name='dislike'),
    url(r'^post/(?P<pk>\d+)/undislike/$', views.undislike_post_view, name='undislike'),
    url(r'^post/(?P<pk>\d+)/likers/$', views.LikersListView, name='likers'),
    url(r'^post/(?P<pk>\d+)/dislikers/$', views.DislikersListView, name='dislikers'),
]
