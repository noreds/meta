from pymongo import MongoClient
from watson_developer_cloud import ToneAnalyzerV3

client = MongoClient('mongodb://hans:noooz@52.59.186.178:27017/')

ta = ToneAnalyzerV3(
    username='e7331108-319b-4594-a055-0b945418b38e',
    password='HE6psH8xRdfj',
    version='2017-06-10')

def get_analyzed_tone(text):
    return ta.tone(text=text)

def get_number_of_words(text):
    return len(text.split())

imported_news = client['news']['imported']

unanalyzed = imported_news.find({'item.text_en':{ '$exists' : True},'item.words_count':{'$gte':250}, 'item.sentiment': { '$exists': False }})
for item in unanalyzed:
    oid = str(item['_id'])
    print(oid)
    imported_news.update_one({'_id': oid}, {'$set': {'item.sentiment': get_analyzed_tone(item['item']['text_en'])}}, )

uncounted = imported_news.find({'item.words_count':{ '$exists' : False}})
for item in uncounted:
    oid = str(item['_id'])
    print(oid)
    imported_news.update_one({'_id': oid}, {'$set': {'item.words_count': get_number_of_words(item['item']['fullText'])}}, )
