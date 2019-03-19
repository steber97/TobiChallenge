import utils.luis
from .models import Message


def luis_connector(query):
    json_res = utils.luis.make_query(query)
    print(json_res)

    # Perform insertion of chat attributes (intent and entities)
    list_of_entities = []
    for el in json_res['entities']:
        list_of_entities.append({'value': el['resolution']['values'][0],
                             'type': el['type']
                             })
    print(list_of_entities)
    message = Message(
        text=json_res['query'],
        top_scoring_intent=json_res['topScoringIntent']['intent'],
        score_top_intent=json_res['topScoringIntent']['score'],
        sentiment_analysis=json_res['sentimentAnalysis']['score'],
        entities=list_of_entities
    )
    message.save()

    print(message)


def manage_chat(text_of_message, user):
    luis_connector(text_of_message)
    return str(text_of_message) + " " + str(user)
