import requests as rq
from pymongo import MongoClient
from watson_developer_cloud import ToneAnalyzerV3

client = MongoClient('mongodb://hans:noooz@52.59.186.178:27017/')

ta = ToneAnalyzerV3(
    username='e7331108-319b-4594-a055-0b945418b38e',
    password='HE6psH8xRdfj',
    version='2017-06-10')

def get_analyzed_tone():
    return ta.tone(text='I am very happy')


imported_news = client['news']['imported']
untranslated = imported_news.find({'text_en': { 'exists': False }})

