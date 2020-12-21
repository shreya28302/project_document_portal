from django.conf.urls import url
from django.contrib.auth import views as auth_views
from portal import views

app_name = 'portal'

urlpatterns = [
    url(r'^login/$', views.Login, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name ='index.html'), name='logout'),
    url(r'^register/$', views.register, name ='register'),
]
