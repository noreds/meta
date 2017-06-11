import requests as rq
from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient('mongodb://hans:noooz@52.59.186.178:27017/')

imported_news = client['news']['imported']

export = imported_news.find({'item.syntaxnet':{ '$exists' : True}})
for item in export:
    oid = str(item['_id'])
    print(oid)
    url = 'https://api.ax-semantics.com/v2/collections/1208/document/'
    headers = {'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2F4LXNlbWFudGljcy5ldS5hdXRoMC5jb20vIiwiYXVkIjoiYnVmdzhQMUdTSGdPTzVnMVFWbjdVM2hxMkhvWkpTSFciLCJlbWFpbCI6Ik1CZXllcjJAZ21haWwuY29tIiwiZXhwIjoxNDk3MjE2ODEzLCJpYXQiOjE0OTcxMzA0MTN9.iTPcRrUAswyh3Qd39UzIzFQgjyou92hX5hJL6pxDOB8', 'Content-Type' : 'application/json'}
    r = rq.post(url, data=dumps(item), headers=headers)
