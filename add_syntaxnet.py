from pymongo import MongoClient
client = MongoClient('mongodb://hans:noooz@52.59.186.178:27017/')

def generate_network(text):
    return "";

imported_news = client['news']['imported']
nonetwork = imported_news.find({'item.syntaxnet': { '$exists': False }})

for item in nonetwork:
    oid = str(item['_id'])
    imported_news.update_one({'_id': oid},{'$set': { 'item.syntaxnet':generate_network(item['item']['fullText']) }},)
    print(oid)

