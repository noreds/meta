from pymongo import MongoClient
from watson_developer_cloud import LanguageTranslatorV2

client = MongoClient('mongodb://hans:noooz@52.59.186.178:27017/')

lt = LanguageTranslatorV2(
    username='4b5a619f-245a-49d0-abfd-f72442c90818',
    password='3e4s3rliFWmO')


def get_english_news(text):
    return lt.translate(text, source='de', target='en',)


imported_news = client['news']['imported']
untranslated = imported_news.find({'item.text_en': { '$exists': False }})
for item in untranslated:
    oid = str(item['_id'])
    imported_news.update_one({'_id': oid},{'$set': { 'item.text_en':get_english_news(item['item']['fullText']) }},)
    print(oid)
