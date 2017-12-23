import collections, re
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

def getBagOfWords(text):
    bagsofwords = [ collections.Counter(re.findall(r'\w+', t.lower())) for t in [text] if t not in stop_words ]
    sumbags = sum(bagsofwords, collections.Counter())
    return [list(x) for x in sumbags.most_common(200)]