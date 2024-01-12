import numpy as np
import pandas as pd
import os
import glob
import py_vncorenlp
import json
import re

import sys
# sys.path.append(')
# sys.path.append('/DataPineLine/AIModel')

from crawler import crawler_main
# from utils.model import Model
# from AIModel.model import Model
# i want import Model in file model.py in folder AIModel
from model import Model


py_vncorenlp.download_model(save_dir='/DataPipeLine/VnCoreNLP')

rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='/DataPipeLine/VnCoreNLP')
# def load_data(path):
#     with open(path, 'r', encoding = 'utf-8') as f:
#         data = f.readlines()
        
#     data = [json.loads(line.strip()) for line in data]
    
#     df = pd.DataFrame(data)
#     return df

def removespec(text):
    text = str(''.join(text))
    n_text = re.sub("([\[\]'\-,])", '', text).lower()
    
    return n_text

def remove_stopword(text, stoplist):
    pass

def tokenizer(sentence, rdrsegmenter):
    tokenizer = rdrsegmenter.word_segment(sentence)
    tokenizer = ''.join(tokenizer)
    return tokenizer
   

def processing():
    # temp_data = crawler_main()
    temp_data = crawler_main()
     
    data = []
    for domain in temp_data:
        data.extend(domain)
        
    
    df = pd.DataFrame(data)
  
    
    df['description'] = df['description'].apply(removespec)
    
    df['tokenized'] = df['description'].apply(lambda x : tokenizer(x, rdrsegmenter))
    df = df.fillna('')
    
    # print(df.iloc[0])
    
    return df
            
        

if __name__ == "__main__":
    
    model = Model()
    df = processing()
    print('phobert embedding')
    df['vector_embedding'] = df['tokenized'].apply(lambda x : model.encoding(x))
    print(df.iloc[0])
    
    ### Convert data
    # data = processing()
    # df = pd.DataFrame(data)
    # # df.to_csv('./data.csv')
    
    # # df = pd.read_csv('./data.csv')
    # # df = df.drop(['Unnamed: 0'], axis=1)
    
    # df['description'] = df['description'].apply(removespec)
    
    # df['tokenized'] = df['description'].apply(lambda x : tokenizer(x, rdrsegmenter))
    
    # print(df.iloc[0])
    
  
