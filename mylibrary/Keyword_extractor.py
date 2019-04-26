from nltk.stem import WordNetLemmatizer
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer


## self.text is a term used in linguistics meaning a large set of text body.
stop_words = set(stopwords.words("english"))

class Keyword_extractor():
    def __init__(self, text=None):
        self.set_text(text)
        self.wnl = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))
        
    def set_vectorizer(self, ngram, max_features = 2000, **kwargs):
        self.vec = CountVectorizer(ngram_range=(ngram, ngram),
                                   max_features = max_features,
                                   **kwargs)
        
    def add_stop_words(self, word_list):
        self.stop_words = self.stop_words.union(word_list)
        
    def set_text(self, corpus):
        """
        corpus is an iterable (list of strings, ... )
        """
        if corpus is not None:
            self._has_corpus = True
        self.corpus = corpus
            
    def extract_words(self, corpus=None):
        if corpus is not None:
            self.set_text(corpus)
            
        assert self._has_corpus
        
        for text in self.corpus:
            try:
                text = re.sub('[^a-zA-Z]', ' ', text) #
                text = text.lower()
                text = re.sub("(\\d|\\W)+"," ",text) # Remove special characters
                text = re.sub("backslash\w*", " ", text) # Remove Latex equation commands
                text = re.sub("\s[a-zA-Z]{1,2}\s", ' ', text) # remove one or two-letter words (units: M, K, s, pc, km, ...)

                text = [self.wnl.lemmatize(word) for word in text.split() if not word in self.stop_words]
                text = " ".join(text)
            except:
                pass
        self.corpus = [text]
        
    def get_top_n_words(self, n=20, ngram=None):
        if ngram is not None:
            self.set_vectorizer(ngram)
        
        self.vec.fit(self.corpus)
        bag_of_words = self.vec.transform(self.corpus) # bag meaning not caring their order.
        sum_words = bag_of_words.sum(axis=0) # why?
        words_freq = [(word, sum_words[0, idx]) for word, idx in self.vec.vocabulary_.items()]
        words_freq = sorted(words_freq, key = lambda x : x[1], reverse=True)
        return words_freq[:n]