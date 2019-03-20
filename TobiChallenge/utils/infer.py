import pickle
import spacy
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

def tokenize(text):
    parser = spacy.load('it_core_news_sm')
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

def estrai(item, ldamodel):
    def takeSecond(elem):
        return elem[1]
    s = list(sorted(item, key=takeSecond, reverse=True))
    idx = s[0][0]
    topics = ldamodel.print_topics(num_words=2)
    topic = topics[idx][1].split("\"")
    return [topic[1], topic[3]]

it_stop = set(nltk.corpus.stopwords.words('italian'))
preludio = ["ma", "mi", "spiego", "comunque", "dunque", "ti", "quindi", "allora", "ciao", "buon", "buonasera", "buongiorno", "dell\'", "dall\'", "vorrei", "voglio"]

for i in preludio:
    it_stop.add(i)

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in it_stop]
    tokens = [get_lemma2(token) for token in tokens]
    return tokens

import gensim   

def elaborate(text_data): 
    res = []
    dictionary = pickle.load(open('dictionary.p', 'rb'))
    ldamodel = gensim.models.ldamodel.LdaModel.load('model3.gensim')


    text_data = list(map(prepare_text_for_lda, text_data))
    text_data = [dictionary.doc2bow(text) for text in text_data]

    for i in ldamodel.get_document_topics(text_data):
        res.append(estrai(i, ldamodel))

    return res