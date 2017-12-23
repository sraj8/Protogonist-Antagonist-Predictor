import gensim
import os
from modules.common_func import readFile, cleanSplitScript
from nltk.corpus import stopwords

class LinesInDir(object):
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        for path, subdirs, files in os.walk(self.dirname):
            for fname in files:
                script = readFile(os.path.join(path, fname))
                split_script = cleanSplitScript(script);
                lower_split_script = [x.lower() for x in split_script if not x.isupper()]
                #for line in open(os.path.join(path, fname)):
                validLetters = "abcdefghijklmnopqrstuvwxyz "
                clearScript = [(''.join([char for char in x if char in validLetters])) for x in lower_split_script]
                for line in clearScript:
                    yield line.strip().split()

def doc2ClusterVec(doc, cluster, w2v):
    stop_words = set(stopwords.words("english"))
    doc = doc.lower()
    validLetters = "abcdefghijklmnopqrstuvwxyz "
    clearScript = ''.join([char for char in doc if char in validLetters])
    words = [x for x in clearScript.strip().split() if x not in stop_words]
    vec = [0] * 200
    for w in words:
        try:
            wv = w2v[w]
            vec[cluster.predict([wv])[0]] += 1
        except:
            pass
    return vec

def modelW2V(fname, dataDir):
    model = gensim.models.Word2Vec(LinesInDir(dataDir), size=100, window=5, min_count=5, workers=4)
    model.save(fname)
    return model