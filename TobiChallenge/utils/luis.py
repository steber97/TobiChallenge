import requests

base_url = "https://westus.api.cognitive.microsoft.com/luis/api/v2.0/apps/9db929ee-1665-4b5a-8fdf-24d5aa80b074"

key = "5e286759209b4505b12431fd69597f69"


def make_query(query):
    """
    Esegue una richiesta semplice
    :param query:
    :return:
    """
    url = base_url + "?verbose=true&timezoneOffset=-360&subscription-key={key}&q={query}"
    url = url.replace("{key}",key).replace("{query}", query)
    r = requests.get(url)
    return r.json()


def get_app_info():
    url = "https://westus.api.cognitive.microsoft.com/luis/api/v2.0/apps/9db929ee-1665-4b5a-8fdf-24d5aa80b074"
    r = requests.get(url,headers={"Ocp-Apim-Subscription-Key":key})
    return r.json()


def add_intent(intent):
    url = "https://westus.api.cognitive.microsoft.com/luis/api/v2.0/apps/9db929ee-1665-4b5a-8fdf-24d5aa80b074/versions/0.1/intents"
    r = requests.post(url, headers={"Ocp-Apim-Subscription-Key":key}, data={"name":intent})
    return r.status_code


def add_example(intent, example):
    url = "https://westus.api.cognitive.microsoft.com/luis/api/v2.0/apps/9db929ee-1665-4b5a-8fdf-24d5aa80b074/versions/0.1/example"
    r = requests.post(url, headers={"Ocp-Apim-Subscription-Key": key}, data={"intentName": intent, "text":example})
    return r.status_code


def train():
    url = "https://westus.api.cognitive.microsoft.com/luis/api/v2.0/apps/9db929ee-1665-4b5a-8fdf-24d5aa80b074/versions/0.1/train"
    r = requests.post(url, headers={"Ocp-Apim-Subscription-Key": key})
    return r.status_code


def publish():
    url = "https://westus.api.cognitive.microsoft.com/luis/api/v2.0/apps/9db929ee-1665-4b5a-8fdf-24d5aa80b074/versions/0.1/train"
    r = requests.post(url, headers={"Ocp-Apim-Subscription-Key": key}, data={"versionId": "0.1","isStaging": False})
    return r.status_code


def train_and_publish():
    st = train()
    if st == 202:
        return publish()
    else:
        return st
