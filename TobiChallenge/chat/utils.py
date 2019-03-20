import utils.luis
from .models import Message
import pickle
import random


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
    json_res = utils.luis.make_query(query)
    print(json_res)

    # Perform insertion of chat attributes (intent and entities)
    dict_of_entities = {}
    for el in json_res['entities']:
        dict_of_entities[el['type']] = el['resolution']['values']
    print(dict_of_entities)
    message = Message(
        text=json_res['query'],
        top_scoring_intent=json_res['topScoringIntent']['intent'],
        score_top_intent=json_res['topScoringIntent']['score'],
        sentiment_analysis=json_res['sentimentAnalysis']['score'],
        entities=dict_of_entities
    )
    message.save()

    return message

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
    if message.score_top_intent<0.5:
        top = "NONHOCAPITO"

    if top == "CallSupport":
        reply = "Certamente! Puoi contattare il supporto studenti al seguente indirizzo: supportostudentipovo@unitn.it"
    elif top == "CancelFromExam":
        en = get_exams(message)
        if len(en)>1 or len(en)==0:
            reply = "Quale esame?\n"
        else:
            reply = get_affirmative_answer() + ", ti ho rimosso dall'esame '" + en[0] + "'"
    elif top == "CancelPreviousIntent":
        reply = get_affirmative_answer()
    elif top == "GetExamInfo":
        en = get_exams(message)
        if len(en)>1 or len(en)==0:
            reply = "Quale esame?\n"
        else:
            reply = "Ecco le informazioni sull'esame: '" + en[0] + "'\nData: mai\nOra: mai\nAula: mai\nCFU: 9"
    elif top == "GetExamResult":
        en = get_exams(message)
        if len(en)>1 or len(en)==0:
            reply = "Quale esame?\n"
        else:
            reply = "Il voto dell'esame '" +  en[0] + "' è 28"
    elif top == "GetLectureTime":
        en = get_exams(message)
        if len(en)>1 or len(en)==0:
            reply = "Quale corso?\n"
        else:
            reply = "La prossima lezione di '"+ en[0] + "' sarà alle TODO in alua TODO"
    elif top == "RegisterToExam":
        en = get_exams(message)
        if len(en)>1 or len(en)==0:
            reply = "Quale esame?\n"
        else:
            reply = get_affirmative_answer() + ", ti ho iscritto all'esame '" + en[0] + "'"
    elif top == "GetMedia":
        reply = "La tua media è 30L"
    elif top == "GetTaxInfo":
        reply = "Non hai tasse da pagare!"
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

    message = luis_connector(text_of_message)

    message, error = calculate_intent(message)

    return create_reply(message)

