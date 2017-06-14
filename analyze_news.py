from pymongo import MongoClient
from watson_developer_cloud import ToneAnalyzerV3
from os import getenv
import json

settings = json.load(open('settings.json'))
client = MongoClient('mongodb://'+settings['mongo']['url']+':27017/')

ta = ToneAnalyzerV3(
    username=getenv('WATSON_TONEANALYSIS_USER', settings['Watson']['ToneAnalyzer']['user']),
    password=getenv('WATSON_TONEANALYSIS_PASSWORD', settings['Watson']['ToneAnalyzer']['password']),
    version='2017-06-10')


def get_analyzed_tone(text):
    return ta.tone(text=text)


def get_number_of_words(text):
    return len(text.split())

imported_news = client['news']['imported']

unanalyzed = imported_news.find({'item.text_en':{ '$exists' : True},'item.words_count':{'$gte':150}, 'item.sentiment': { '$exists': False }})
for item in unanalyzed:
    oid = str(item['_id'])
    print(oid)
    imported_news.update_one({'_id': oid}, {'$set': {'item.sentiment': get_analyzed_tone(item['item']['text_en'])}}, )

uncounted = imported_news.find({'item.words_count':{ '$exists' : False}})
for item in uncounted:
    oid = str(item['_id'])
    print(oid)
    imported_news.update_one({'_id': oid}, {'$set': {'item.words_count': get_number_of_words(item['item']['fullText'])}}, )
