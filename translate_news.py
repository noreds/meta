from pymongo import MongoClient
from watson_developer_cloud import LanguageTranslatorV2
from os import getenv
import json

settings = json.load(open('settings.json'))
client = MongoClient('mongodb://'+settings['mongo']['url']+':27017/')

lt = LanguageTranslatorV2(
    username=getenv('WATSON_TRANSLATOR_USER', settings['Watson']['LanguageTranslator']['user']),
    password=getenv('WATSON_TRANSLATOR_PASSWORD', settings['Watson']['LanguageTranslator']['password']))


def get_english_news(text):
    return lt.translate(text, source='de', target='en',)


imported_news = client['news']['imported']
untranslated = imported_news.find({'item.text_en': { '$exists': False }})
for item in untranslated:
    oid = str(item['_id'])
    imported_news.update_one({'_id': oid},{'$set': { 'item.text_en':get_english_news(item['item']['fullText']) }},)
    print(oid)
