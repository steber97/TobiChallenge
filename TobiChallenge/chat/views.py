from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from django.views.generic.base import View
from rest_framework.decorators import api_view

from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.
from django.views import View

from django.views.decorators.csrf import csrf_exempt

class ChatApiMessage(APIView):
    def get(self, *args, **kwargs):
        pass

    def post(self, request):
        data = {
            "pippo": "Paperino"
        }
        return JsonResponse(data)
