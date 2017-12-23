from empath import Empath

lexicon = Empath()

def getEmpathAnalysis(text):
    empath_dict = lexicon.analyze(text, normalize=True)
    empath_formatted = [(i, empath_dict[i]) for i in empath_dict]
    empath_formatted.sort(key=lambda tup: tup[0])
    return empath_formatted