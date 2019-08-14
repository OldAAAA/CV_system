# chat/routing.py
from django.conf.urls import url

from demo import consumer

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumer.ChatConsumer),
]