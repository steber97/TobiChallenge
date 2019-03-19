from django.urls import path

from .views import ChatApiMessage

urlpatterns = [
    # ex: chat/
    path('api/messages/', ChatApiMessage.as_view(), name='chat_post')
]