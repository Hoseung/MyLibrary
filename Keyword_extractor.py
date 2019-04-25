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
        
    def set_text(self, text):
        if text is not None:
            self._has_text = True
        self.text = text
            
    def extract_words(self, text=None):
        if text is not None:
            self.set_text(text)
            
        assert self._has_text
        
        try:
            self.text = re.sub('[^a-zA-Z]', ' ', self.text) #
            self.text = self.text.lower()
            self.text = re.sub("(\\d|\\W)+"," ",self.text) # Remove special characters
            self.text = re.sub("backslash\w*", " ", self.text) # Remove Latex equation commands
            self.text = re.sub("\s[a-zA-Z]{1,2}\s", ' ', self.text) # remove one or two-letter words (units: M, K, s, pc, km, ...)

            self.text = [self.wnl.lemmatize(word) for word in self.text.split() if not word in self.stop_words]
            self.text = " ".join(self.text)
        except:
            pass
        
    def get_top_n_words(self, n=20, ngram=None):
        if ngram is not None:
            self.set_vectorizer(ngram)
        
        self.vec.fit(self.text)    
        bag_of_words = vec.transform(self.text) # bag meaning not caring their order.
        sum_words = bag_of_words.sum(axis=0) # why?
        words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
        words_freq = sorted(words_freq, key = lambda x : x[1], reverse=True)
        return words_freq[:n]