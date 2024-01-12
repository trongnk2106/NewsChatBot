import sys

sys.path.append('../../MMIR/BE')
sys.path.append('../../MMIR/BE/Datapipeline')

import json
import pandas as pd

from elasticsearch import Elasticsearch
from MMIR.BE.Datapipeline.indexMapping import indexMapping
import os
# use tdqm to show progress bar
from tqdm import tqdm




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
   
            
def merge(list_path):
    store_data = []
    for fi in list_path:
        with open('./encoding_out/' + fi, 'r', encoding='utf-8') as f:
            data = f.readlines()
          
        data = [json.loads(line.strip()) for line in data]
        store_data.extend(data)
    
    with open('./data.jsonl', 'w', encoding='utf-8') as f:
        for rec in store_data:
            json.dump(rec, f, ensure_ascii=False)
            f.write('\n')
        
    return store_data

def load_data(path):
    
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    data = [json.loads(line.strip()) for line in data]
    
    # for rec in data:
        
    
    
    return data
    

if __name__ == '__main__':
    # create_index()
    # get_indices()
    
    data = load_data('D:/airflow_tutorial/SomeThing/merge.jsonl')
    print(data[0]['paragraphs'])
    # data_ = list(data[0]['paragraphs'])
    data_ = data[0]['paragraphs'][1:-1].replace(",'", '').replace("'","").split('. ')
    
    print(data_)
    print(type(data_))

    # es.indices.delete(index='news')
    
