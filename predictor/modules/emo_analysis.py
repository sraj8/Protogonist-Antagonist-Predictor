import json
import operator
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='43ae17d3-bbbc-4189-86a8-5ea495038924',
  password='P2QVUeioQlJR',
  version='2017-02-27')

def getSentAnalysis(text):
    response = natural_language_understanding.analyze(
      text=text,
      features=Features(
        emotion=EmotionOptions()))
    res = response['emotion']['document']['emotion']
    res_formatted = [(x, res[x]) for x in res]
    res_formatted.sort(key = operator.itemgetter(0))
    return res_formatted