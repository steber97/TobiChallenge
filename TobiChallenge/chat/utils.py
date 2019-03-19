import utils.luis

def luis_connector(query):
    json_res = utils.luis.make_query(query)
    print(json_res)


def manage_chat(text_of_message, user):
    luis_connector(text_of_message)
    return str(text_of_message) + " " + str(user)
