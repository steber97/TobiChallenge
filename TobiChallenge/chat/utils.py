import utils.luis
from .models import Message
import random


def luis_connector(query):
    json_res = utils.luis.make_query(query)
    print(json_res)

    # Perform insertion of chat attributes (intent and entities)
    dict_of_entities = {}
    for el in json_res['entities']:
        dict_of_entities[el['type']] =  el['resolution']['values']
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
            reply = get_affirmative_answer() + ", ti ho rimosso dall'esame '" + en['Exams'][0] + "'"
    elif top == "CancelPreviousIntent":
        reply = get_affirmative_answer()
    elif top == "GetExamInfo":
        en = get_exams(message)
        if len(en)>1 or len(en)==0:
            reply = "Quale esame?\n"
        else:
            reply = "Ecco le informazioni sull'esame: '" + en['Exams'][0] + "'\nData: mai\nOra: mai\nAula: mai\nCFU: 9"
    elif top == "GetExamResult":
        en = get_exams(message)
        if len(en)>1 or len(en)==0:
            reply = "Quale esame?\n"
        else:
            reply = "Il voto dell'esame '" +  en['Exams'][0] + "' è 28"
    elif top == "GetLectureTime":
        en = get_exams(message)
        if len(en)>1 or len(en)==0:
            reply = "Quale corso?\n"
        else:
            reply = "La prossima lezione di '"+ en['Exams'][0] + "' sarà alle TODO in alua TODO"
    elif top == "RegisterToExam":
        en = get_exams(message)
        if len(en)>1 or len(en)==0:
            reply = "Quale esame?\n"
        else:
            reply = get_affirmative_answer() + ", ti ho iscritto all'esame '" + en['Exams'][0] + "'"
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

'''
def manage_reply():
    top = message.top_scoring_intent
    reply = ""
    good = True
    ex = message.entities['Exams']
    if len(ex)>1 or len(ex)==0:
'''


def manage_chat(text_of_message, user):
    message = luis_connector(text_of_message)
    reply = create_reply(message)
    return reply
