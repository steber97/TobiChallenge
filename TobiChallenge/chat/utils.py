import utils.luis
from .models import Message
import pickle
import random
from .models import *


class Grafo:
    def __init__(self):
        self.adj = {}

    def update_edge(self, a, b):
        if a is None:
            return
        if a not in self.adj:
            self.adj[a] = {}
            self.adj[a][b] = 1

        else:
            if b not in self.adj[a]:
                self.adj[a][b] = 1
            else:
                self.adj[a][b] += 1
        return

    def print_adj_list(self, node):
        if node in self.adj:
            print(self.adj[node])

    def get_most_prob(self, node):
        best_node = -1
        max_val = -1
        total = 0
        for el in self.adj[node]:
            total += self.adj[node][el]
            if self.adj[node][el] > max_val and el != node:
                max_val = self.adj[node][el]
                best_node = el
        return best_node, max_val/total


intent_entities_map = {
  "CallSupport": [
  ],
  "CancelFromExam": [
    "Exams"
  ],
  "CancelPreviousIntent": [

  ],
  "Continue": [

  ],
  "GetExamInfo": [
    "Exams"
  ],
  "GetExamResult": [
    "Exams"
  ],
  "GetLectureTime": [
    "Exams"
  ],
  "GetMedia": [

  ],
  "GetTaxInfo":[

  ] ,
  "Introduction": [

  ],
  "None": [

  ],
  "Preludio": [

  ],
  "RegisterToExam": [
    "Exams"
  ]
}

def luis_connector(query):

    # graph is of type Graph
    try:
        graph = pickle.load(open("graph.p", "rb"))
    except:
        graph = Grafo()
    json_res = utils.luis.make_query(query)
    print(json_res)

    # Perform insertion of chat attributes (intent and entities)
    dict_of_entities = {}
    for el in json_res['entities']:
        try:
            dict_of_entities[el['type']] = dict_of_entities[el['type']] + el['resolution']['values']
        except:
            dict_of_entities[el['type']] = el['resolution']['values']
    print(dict_of_entities)
    message = Message(
        text=json_res['query'],
        top_scoring_intent=json_res['topScoringIntent']['intent'],
        score_top_intent=json_res['topScoringIntent']['score'],
        sentiment_analysis=json_res['sentimentAnalysis']['score'],
        entities=dict_of_entities
    )

    try:
        last_message = Message.objects.order_by('-timestamp').first().top_scoring_intent
    except:
        print("except!")
        last_message = None

    message.save()

    print("last message")
    print(last_message)
    print("message")
    print(message)
    graph.update_edge(last_message, message.top_scoring_intent)
    print("adj list for top scoring message")
    graph.print_adj_list(last_message)
    pickle.dump(graph, open("graph.p", "wb"))

    prevision, prob = graph.get_most_prob(message.top_scoring_intent)
    if prob < 0.5:
        prevision = None

    prevision = Message(
        text=None,
        top_scoring_intent=prevision,
        score_top_intent=1,
        sentiment_analysis=0.5,
        entities=dict_of_entities
    )
    return message, prevision


def get_affirmative_answer():
    ans = ["OK","Va bene", "Fatto", "Certamente", "Nessun problema"]
    return random.choice(ans)

def get_greeting():
    ans = ["Ciao! Come posso aiutarti?"]
    return random.choice(ans)


def get_exams(message):
    try:
        aaaa= message.entities['Exams']
    except:
        aaaa= []
    return aaaa

def get_exam_props(message):
    try:
        aaaa= message.entities['Exam Properties']
    except:
        aaaa= []
    return aaaa

def create_reply(message):
    """
    Basically a huge IF wall
    :param message:
    :return:
    """
    top = message.top_scoring_intent
    reply = ""
    if top == "Continue":
        reply = "Informazione prima"
        return reply
    if message.score_top_intent<0.3:
        top = "NONHOCAPITO"

    if top == "CallSupport":
        reply = "Certamente! Puoi contattare il supporto studenti al seguente indirizzo: supportostudentipovo@unitn.it"
    elif top == "CancelFromExam":
        en = get_exams(message)
        if len(en)>1 or len(en)==0:
            reply = "Quale esame?\n"
        else:
            try:
                course = Course.objects.get(name=en[0])
                ExamSubscription.objects.get(exam=Exam.objects.get(course=course)).delete()
                reply = get_affirmative_answer() + ", ti ho rimosso dall'esame '" + en[0] + "'"
            except:
                reply = "Non eri iscritto all'esame '" + en[0] + "'"

    elif top == "CancelPreviousIntent":
        reply = get_affirmative_answer()
    elif top == "GetExamInfo":
        en = get_exams(message)
        if len(en)>1 or len(en)==0:
            reply = "Quale esame?\n"
        else:
            try:
                course = Course.objects.get(name=en[0])
                exam = Exam.objects.get(course=course)
                data = exam.date.strftime('%d/%m/%Y')
                ora = exam.date.strftime('%H:%M')
                props = get_exam_props(message)
                if 'quando' in props:
                    reply = "L'esame '" + en[0] + "' si svolgerà in data " + data + " alle ore " + ora
                elif 'chi' in props:
                    reply = "L'esame '" + en[0] + "' sarà tenuto dal professore " + exam.professor.name
                elif 'dove' in props:
                    reply = "L'esame '" + en[0] + "' si svolgerà in aula " + exam.room
                elif 'CFU' in props:
                    reply = "L'esame '" + en[0] + "' vale " + str(exam.course.cfu) + " CFU"
                if len(props) == 0 or len(props) > 1:
                    reply = "Ecco le informazioni sull'esame: '" + en[0] + "'\nData: " + data + "\nOra: " + ora + "\nAula: " + exam.room + "\nCFU: " + str(course.cfu)
            except:
                reply = "Non esiste l'esame: '" + en[0] + "'"
    elif top == "GetExamResult":
        en = get_exams(message)
        if len(en)>1 or len(en)==0:
            reply = "Quale esame?\n"
        else:
            try:
                voto = ExamGiven.objects.get(course=Course.objects.get(name=en[0])).mark
                reply = "Il voto dell'esame '" +  en[0] + "' è " + str(voto)
            except:
                reply = "Non hai ancora dato l'esame '" + en[0] + "'"
    elif top == "GetLectureTime":
        en = get_exams(message)
        if len(en)>1 or len(en)==0:
            reply = "Quale corso?\n"
        else:
            reply = "La prossima lezione di '"+ en[0] + "' sarà alle 17:30 in aula A105"
    elif top == "RegisterToExam":
        en = get_exams(message)
        if len(en)>1 or len(en)==0:
            reply = "Quale esame?\n"
        else:
            try:
                me = Student.objects.all()[0]
                exam = Exam.objects.get(course=Course.objects.get(name=en[0]))
                if(len(ExamSubscription.objects.filter(student=me, exam=exam)) >= 1):
                    reply = "Eri già iscritto all'esame '" + en[0] + "'"
                else:
                    ExamSubscription(student=me, exam=exam).save()
                    reply = get_affirmative_answer() + ", ti ho iscritto all'esame '" + en[0] + "'"
            except:
                reply = "Non c'è nessun appello per l'esame '" + en[0] + "'"
    elif top == "GetMedia":
        somma = 0
        for ex in ExamGiven.objects.all():
            somma += ex.mark
        reply = "La tua media è " + str(somma/len(ExamGiven.objects.all()))
    elif top == "GetTaxInfo":
        tasse = ""
        for tassa in TaxRecord.objects.all():
            tasse += str(tassa.amount) + "€\n"
        reply = "Devi pagare le seguenti tasse:\n" + tasse
    elif top == "Introduction":
        reply = get_greeting()
    elif top == "Preludio":
        pass
    elif top == "None":
        reply = "Come scusa?"
    else:
        reply = "Non ho capito"

    return reply


def calculate_intent(message):

    try:
        session = pickle.load(open("session.p", "rb"))
    except Exception:
        session = None

    if session is None:
        session = {
            'last_intent': None,
            'last_intent_score': None,
            'entities': None
        }
    print("enter calculate intent")
    for el in session.keys():
        print(el)

    error_var = False
    try:
        entities = session['entities']
    except:
        entities = None

    if entities is None:
        entities = {}
    
    if message.top_scoring_intent in ['None', 'Continue', 'Preludio', 'Introduction'] and session['last_intent'] is not None :
        print('useless top scoring intent')
        error_var = True
        last_intent = session['last_intent']
        last_intent_score = session['last_intent_score']
    elif message.score_top_intent < 0.5 and session['last_intent'] is not None:
        print('score of intent is too low')
        last_intent = session['last_intent']
        last_intent_score = session['last_intent_score']
    else:
        print('update')
        session['last_intent'] = message.top_scoring_intent
        last_intent = message.top_scoring_intent
        session['last_intent_score'] = message.score_top_intent
        last_intent_score = message.score_top_intent

    print(message.entities)
    for entity in message.entities:
        print(entity)
        entities[entity] = message.entities[entity]

    session['entities'] = entities
    session['last_intent'] = last_intent
    if last_intent is None:
        error_var = True
    else:
        for entity in intent_entities_map[last_intent]:
            if entities[entity] is None:
                error_var = True

    message.top_scoring_intent = last_intent
    message.score_top_intent = last_intent_score
    message.entities = entities

    print(message.top_scoring_intent)
    print(message.score_top_intent)
    print(message.entities)
    print(error_var)

    pickle.dump(session, open("session.p", "wb"))

    return message, error_var


def manage_chat(text_of_message, user, request):

    print(request)

    message, prevision = luis_connector(text_of_message)

    message, error = calculate_intent(message)

    return create_reply(message)

