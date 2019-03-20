from django.urls import path
from django.views.generic import TemplateView

from .views import ChatApiMessage
from .dashboard import Dashboard

urlpatterns = [
    # ex: chat/
    path('api/messages', ChatApiMessage.as_view(), name='chat_post'),
    #dashboard

    path('dashboard', Dashboard.as_view(), name='dash_get'),
    path('', TemplateView.as_view(template_name='index.html'))
]