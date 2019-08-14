from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    url('fall', views.fall),
    url('emotion', views.emotion),
    url('attack', views.attack),
    url('interact', views.interact),
    url('stranger', views.stranger),
    url('change_data', views.change_data),
    url('post_data',views.post_data),
]