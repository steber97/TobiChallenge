import utils.luis
from .models import Message


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

def manage_chat(text_of_message, user):
    message = luis_connector(text_of_message)
    reply = create_reply(message)
    return reply
