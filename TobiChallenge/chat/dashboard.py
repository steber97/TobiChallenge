from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView


# Create your views here.
from django.views import View

from django.views.decorators.csrf import csrf_exempt

import utils.infer

from .models import *

import json


class Dashboard(APIView):
    def get(self, request):
        tipo = request.GET.get('tipo')
        if(tipo is None):
            text = request.GET.get('text')
            text_data = [text] #["vorrei cambiare piano di studi"]

            data = utils.infer.elaborate(text_data)

            text = json.dumps(data)
            return HttpResponse(text)
        else:
            elems = []
            for i in NewIntent.objects.all():
                elems.append(i)
            text = json.dumps(elems)
            return HttpResponse(text)
