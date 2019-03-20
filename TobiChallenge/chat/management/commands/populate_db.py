from django.core.management.base import BaseCommand
from chat.models import *
import datetime
import time
import os

import pickle


map_name_intent = {
    "ciao\n": "Introduction",
    "quanto ho preso nell'esame di programmazione 1\n": "GetExamResult",
    "che media ho\n": "GetMedia",
    "dammi info sull'esame di asd\n": "GetExamInfo",
    "iscrivimi\n": "RegisterToExam",
    "anzi no, disiscrivimi\n": "CancelFromExam",
    "quali tasse devo pagare?\n": "GetTaxInfo",
    "chiedo il supporto della segreteria\n": "CallSupport"
}

class Command(BaseCommand):
    help = 'Populate DB'

    def handle(self, *args, **kwargs):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        infile = open(os.path.join(__location__, 'prova.txt'), "r")
        line = infile.readline()
        user = User.objects.get(username="stefano")

        my_time = datetime.datetime(year=2019, month=3, day=20, hour=10, minute=5, second=5, microsecond=0)

        while line is not None and line != '':

            if line == "#\n" or line == "#":
                my_time =  my_time + datetime.timedelta(minutes=3)
                time.sleep(35)
            else:
                text = line[:-1]
                message = Message(
                    text=text,
                    user = user,
                    top_scoring_intent=map_name_intent[line],
                    score_top_intent=0.8,
                    entities=[]
                )
                print(message.text)
                print(message.top_scoring_intent)
                print("\n")
                message.save()
                my_time = my_time + datetime.timedelta(seconds=10)
                time.sleep(5)
            line = infile.readline()