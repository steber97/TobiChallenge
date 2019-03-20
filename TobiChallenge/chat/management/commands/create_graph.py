
from django.core.management.base import BaseCommand

import sys

from datetime import *

# sys.path.append("../../grafo")
from chat.grafo import Grafo

from chat.models import *

import pickle


class Command(BaseCommand):
    help = 'Create graph'

    def handle(self, *args, **kwargs):
        grafo = Grafo()

        list_messages = list(Message.objects.all().order_by("-timestamp"))

        for i, message in enumerate(list_messages):
            if i != len(list_messages) - 1:
                #print(datetime.strptime(list_messages[i].timestamp.isoformat(), '%H:%M:%S.%f')- datetime.strptime(list_messages[i+1].timestamp.isoformat(), '%H:%M:%S.%f'))
                if datetime.strptime(list_messages[i].timestamp.isoformat(), '%H:%M:%S.%f')- datetime.strptime(list_messages[i+1].timestamp.isoformat(), '%H:%M:%S.%f') < timedelta(seconds=60):
                    grafo.update_edge(list_messages[i].top_scoring_intent, list_messages[i+1].top_scoring_intent)
                #else:
                    #print("nisba")

        #for el in grafo.adj:
            #print(el)
            #print(grafo.adj[el])

        pickle.dump(grafo, open("graph.p", "wb"))



