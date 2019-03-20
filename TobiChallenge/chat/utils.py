import utils.luis
from .models import Message
import json
import pickle


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


def create_reply(message):
    """
    Basically a huge IF wall
    :param message:
    :return:
    """
    top = message.top_scoring_intent
    reply = ""
    if top == "CallSupport":
        reply = "Stanno tutti a dormire"
    elif top == "CancelFromExam":
        en = message.entities
        if len(en['Exams'])>1:
            reply = "Quale esame?\n"
        else:
            reply = "OK"
    return reply


def calculate_intent(session, message):

    try:
        session = pickle.load(open("session.p", "rb"))
    except Exception:
        session = {}

    print("enter calculate intent")
    for el in session.keys():
        print(el)

    error_var = False
    entities = session['entities']
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

    session = request.session

    message = luis_connector(text_of_message)

    message, error = calculate_intent(session, message)

    # A questo punto siamo sicuri che entities sono al massimo una per tipo.


    return str(text_of_message) + " " + str(user)

