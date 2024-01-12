import json 


import os 
import py_vncorenlp

import re
import sys

from model import Model
from elasticsearch import Elasticsearch
from indexMapping import indexMapping

from tqdm import tqdm

# sys.path.append('D:/airflow_tutorial/MMIR/BE/Datapipeline/')

# py_vncorenlp.download_model(save_dir='D:/airflow_tutorial/MMIR/BE/Datapipeline/VnCoreNLP')


es = Elasticsearch('http://localhost:9200',
                   basic_auth=('elastic', 'trongnt123'))
def create_index():
    es.indices.create(index='news', mappings=indexMapping)

def get_indices():
    print(es.indices.get_alias().keys())
    
def push_data(data):
    #using tqdm to show progress bar
    for idx, rec in tqdm(enumerate(data)):
        try:
            # print(idx)
            es.index(index='news', document=rec, id=idx)
        except Exception as e:
            print(e)
            print(idx)
            print(rec['title'], '\n', rec['link'], '\n', rec['date'] ,'\n', type(rec['author']) ,'\n', rec['description'] ,'\n', type(rec['paragraphs']))
            break
            # print(rec)
            
    print("done")


def removespec(text):
    text = str(''.join(text))
    n_text = re.sub("([\[\]'\-,])", '', text)

    return n_text

def tokenizer(sentence, rdrsegmenter):
    tokenizer = rdrsegmenter.word_segment(sentence)
    tokenizer = ''.join(tokenizer)
    return tokenizer


if __name__ == "__main__":
    es.indices.delete(index='news')
    create_index()
    with open('merge.jsonl', 'r', encoding='utf-8') as f:
        data = f.readlines()
    data = [json.loads(line.strip()) for line in data]

    rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='D:/airflow_tutorial/MMIR/BE/Datapipeline/VnCoreNLP')

    for rec in data:
        rec['paragraphs'] = removespec(rec['paragraphs'])
        rec['description'] = removespec(rec['description'])
        rec['tokenized'] = tokenizer(rec['description'], rdrsegmenter)
        
    os.chdir('..')
    model = Model()
    

    
    for rec in tqdm(data):
        # delete tokenized in rec before push to elastic
        
        rec['embedding'] = model.encoding(rec['tokenized'])
        del rec['tokenized']
        # break
    # print(data[0])
        
    push_data(data)
    
    # get_indices()
    
    
    
    # data = [removespec(rec['paragraphs']) for rec in data]
    # data = [removespec(rec['description']) for rec in data]
    
    # print(data[0])
    
    
    # file = os.listdir('D:/airflow_tutorial/Data')
    # with open('merge.jsonl', 'w', encoding='utf-8') as f:
    #     for fi in file:
    #         with open('D:/airflow_tutorial/Data/' + fi, 'r', encoding='utf-8') as f1:
    #             data = f1.readlines()
    #         data = [json.loads(line.strip()) for line in data]
    #         for rec in data:
    #             json.dump(rec, f, ensure_ascii=False)
    #             f.write('\n')

