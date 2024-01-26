import numpy as np
import pandas as pd
import os
import glob
import py_vncorenlp
import json
import re
from tqdm import tqdm
import sys
# sys.path.append(')
# sys.path.append('/DataPineLine/AIModel')

from crawler import crawler_main
# from utils.model import Model
# from AIModel.model import Model
# i want import Model in file model.py in folder AIModel
from model import Model


# py_vncorenlp.download_model(save_dir='/DataPipeLine/VnCoreNLP')



def removespec(text):
    text = str(''.join(text))
    n_text = re.sub("([\[\]'\-,])", '', text)
    
    return n_text

def remove_stopword(text, stoplist):
    pass

def tokenizer(sentence, rdrsegmenter):
    tokenizer = rdrsegmenter.word_segment(sentence)
    tokenizer = ''.join(tokenizer)
    return tokenizer
   

# def processing(rdrsegmenter):
   
#     temp_data = crawler_main()
     
#     data = []
#     for domain in temp_data:
#         data.extend(domain)
        
    
#     # df = pd.DataFrame(data)
  
    
#     df['description'] = df['description'].apply(removespec)
#     df['description'] = df['paragraphs'].apply(removespec)
    
#     df['tokenized'] = df['description'].apply(lambda x : tokenizer(x, rdrsegmenter))
#     df = df.fillna('')
    
#     # print(df.iloc[0])
    
#     return df
            
        

async def embedding():
    
    temp_data = crawler_main()
    data = []
    for domain in temp_data:
        data.extend(domain)
    
    rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='D:/airflow_tutorial/MMIR/BE/Datapipeline/VnCoreNLP')
    
    for rec in data:
        rec['paragraphs'] = removespec(rec['paragraphs'])
        rec['description'] = removespec(rec['description'])
        rec['tokenized'] = tokenizer(rec['description'], rdrsegmenter)
        
    os.chdir('../..')
    model = Model()
    for rec in tqdm(data):
    # delete tokenized in rec before push to elastic
    
        rec['embedding'] = model.encoding(rec['tokenized'])
        del rec['tokenized']
        
    return data
    # df = processing(rdrsegmenter)
    # os.chdir('..')
   

    
    ### Convert data
    # data = processing()
    # df = pd.DataFrame(data)
    # # df.to_csv('./data.csv')
    
    # # df = pd.read_csv('./data.csv')
    # # df = df.drop(['Unnamed: 0'], axis=1)
    
    # df['description'] = df['description'].apply(removespec)
    
    # df['tokenized'] = df['description'].apply(lambda x : tokenizer(x, rdrsegmenter))
    
    # print(df.iloc[0])
    
  
