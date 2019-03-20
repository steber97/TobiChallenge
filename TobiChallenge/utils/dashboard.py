def estrai(item, ldamodel):
    def takeSecond(elem):
        return elem[1]
    s = list(sorted(item, key=takeSecond, reverse=True))
    idx = s[0][0]
    topics = ldamodel.print_topics(num_words=2)
    topic = topics[idx][1].split("\"")
    return [topic[1], topic[3]]

def process(text_data):
    import spacy

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


    import nltk
    nltk.download('wordnet')
    from nltk.corpus import wordnet as wn
    def get_lemma(word):
        lemma = wn.morphy(word)
        if lemma is None:
            return word
        else:
            return lemma

    from nltk.stem.wordnet import WordNetLemmatizer
    def get_lemma2(word):
        return WordNetLemmatizer().lemmatize(word)

    nltk.download('stopwords')
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

    text_data = list(map(prepare_text_for_lda, text_data))

    from gensim import corpora
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]

    import gensim
    NUM_TOPICS = 3
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=20)
    
    res = []
    for i in ldamodel.get_document_topics(corpus):
        res.append(estrai(i, ldamodel))

    ldamodel.save('model3.gensim')


with open("test.txt") as f:
    data = f.readlines()

data_s = []
for i in data:
    data_s.append(i.strip())

model = process(data_s)



