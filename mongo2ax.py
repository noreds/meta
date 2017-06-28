import requests as rq
from pymongo import MongoClient
from bson.json_util import dumps
from os import getenv
import json

settings = json.load(open('settings.json'))
databaseName = getenv('MONGO_DATABASE', settings['mongo']['database'])
collectionName = getenv('MONGO_COLLECTION', settings['mongo']['collection'])
user = getenv('MONGO_USER', settings['mongo']['user'])
password = getenv('MONGO_PASSWORD', settings['mongo']['password'])

client = MongoClient(host=['mongo']['url'], port=['mongo']['port'])

if password != '' and user != '':
    client[databaseName].authenticate(user, password, mechanism='SCRAM-SHA-1')

imported_news = client[databaseName][collectionName]

apikey = getenv('AX_API_KEY', settings['AX']['API-Key'])

export = imported_news.find({'item.syntaxnet': {'$exists': True}})
for item in export:
    oid = str(item['_id'])
    print(oid)
    url = getenv('AX_COLLECTION_URL', settings['AX']['url'])

    headers = {'Authorization': apikey, 'Content-Type': 'application/json'}
    r = rq.post(url, data=dumps(item), headers=headers)
