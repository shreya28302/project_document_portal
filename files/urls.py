from django.conf.urls import url
from django.contrib.auth import views as auth_views
from files import views

app_name = 'files'

urlpatterns = [
    url(r'^mydownloads/$',views.downloadlist_view,name='download'),
    url(r'^(?P<uname>\w+)/list/$',views.postlist_view,name='post_list'),
    url(r'^(?P<uname>\w+)/post/new/$',views.newpost,name='post_new'),
    url(r'^post/(?P<pk>\d+)$', views.postdetail_view, name='post_detail'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.postupdate_view, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.postdelete_view, name='post_remove'),
    url(r'^post/(?P<pk>\d+)/download/$', views.postdownload, name='downloadpost'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^(?P<uname>\w+)/drafts/$', views.draftlist_view, name='post_draft'),
    url(r'^post/(?P<pk>\d+)/like/$', views.like_post_view, name='like'),
    url(r'^post/(?P<pk>\d+)/unlike/$', views.unlike_post_view, name='unlike'),
    url(r'^post/(?P<pk>\d+)/dislike/$', views.dislike_post_view, name='dislike'),
    url(r'^post/(?P<pk>\d+)/undislike/$', views.undislike_post_view, name='undislike'),
    url(r'^post/(?P<pk>\d+)/likers/$', views.LikersListView, name='likers'),
    url(r'^post/(?P<pk>\d+)/dislikers/$', views.DislikersListView, name='dislikers'),
]
