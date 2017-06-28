from pymongo import MongoClient
import pandas as pd
import numpy as np
from subprocess import call, PIPE, Popen, STDOUT


def generate_network(text):
    syntaxtext = Popen(
        ['echo %s | sudo docker run --rm -i  marcobeyer/german-syntaxnet-docker > /home/ubuntu/tmp.txt' % text],
        shell=True, stdout=PIPE).stdout.read().decode("utf-8")
    df = pd.read_csv("/home/ubuntu/tmp.txt", sep='\t', header=None)
    print(df.head())
    df_words = df[1]
    df_type1 = df[3]
    df_type2 = df[4]
    role = df[6]
    root = df[7]

    pos_dots = np.where(np.array(df_type1.str.find("PUNCT")) == 0)

    sentences = []
    last_dot_pos = -1
    for dot_pos in pos_dots[0]:
        words = []
        for i in range(last_dot_pos + 1, dot_pos + 1):
            words.append(
                {"name": df_words[i], "type1": df_type1[i], 'type2': df_type2[i], 'relations': {'role': role[i], 'root': root[i]}})
        last_dot_pos = dot_pos
        sentences.append({"words": words})

    data = {"sentences": sentences}
    return data


def add_networks_to_db():
    client = MongoClient('mongodb://mongodb:27017/')
    imported_news = client['news']['imported']
    nonetwork = imported_news.find({'item.syntaxnet': {'$exists': False}})

    for item in nonetwork:
        oid = str(item['_id'])
        imported_news.update_one({'_id': oid},
                                 {'$set': {'item.syntaxnet': generate_network(item['item']['fullText'])}}, )
        print(oid)


if __name__ == "__main__":
    add_networks_to_db()
