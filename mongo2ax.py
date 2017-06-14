import requests as rq
from pymongo import MongoClient
from bson.json_util import dumps
from os import getenv
import json
settings = json.load('settings.json')

client = MongoClient('mongodb://'+settings['mongo']['url']+':27017/')
imported_news = client['news']['imported']
apikey = getenv('AX_API_KEY', settings['AX']['API-Key'])

export = imported_news.find({'item.syntaxnet':{ '$exists' : True}})
for item in export:
    oid = str(item['_id'])
    print(oid)
    url = getenv('AX_COLLECTION_URL', settings['AX']['url'])

    headers = {'Authorization': apikey, 'Content-Type' : 'application/json'}
    r = rq.post(url, data=dumps(item), headers=headers)
