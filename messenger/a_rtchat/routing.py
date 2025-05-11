from django.urls import path
from a_rtchat.consumers import ChatroomConsumer

websocket_urlpatterns = [
    path('ws/chatroom/<chatroom_name>/', ChatroomConsumer.as_asgi()),
]