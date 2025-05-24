from django.urls import path
from a_rtchat.consumers import ChatroomConsumer, OnlineStatusConsumer

websocket_urlpatterns = [
    path('ws/chatroom/<chatroom_name>/', ChatroomConsumer.as_asgi()),
    path('ws/online-status/', OnlineStatusConsumer.as_asgi()),
]