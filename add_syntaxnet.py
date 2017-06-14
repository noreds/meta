from pymongo import MongoClient
import json
import pandas as pd
import numpy as np



client = MongoClient('mongodb://mongodb:27017/')

def generate_network(text):
    fname_in = "example_output.txt"
    fname_out = "example_output.json"

    df = pd.read_csv(fname_in, sep='\t', header=None)

    df_words = df[1]
    df_type1 = df[3]
    df_type2 = df[4]

    pos_dots = np.where(np.array(df_type1.str.find(".")) == 0)

    sentences = []
    last_dot_pos = -1
    for dot_pos in pos_dots[0]:
        words = []
        for i in range(last_dot_pos + 1, dot_pos + 1):
            words.append({"name": df_words[i], "type1": df_type1[i], "type2": df_type2[i]})
        last_dot_pos = dot_pos
        sentences.append({"words": words})

    data = {"output": {"sentences": sentences}}

    with open(fname_out, 'w') as f:
        return json.dump(data, f)

imported_news = client['news']['imported']
nonetwork = imported_news.find({'item.syntaxnet': {'$exists': False}})

for item in nonetwork:
    oid = str(item['_id'])
    imported_news.update_one({'_id': oid}, {'$set': {'item.syntaxnet': generate_network(item['item']['fullText'])}}, )
    print(oid)
