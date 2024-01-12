import torch
from transformers import AutoModel, AutoTokenizer
import py_vncorenlp
import os
import numpy as np
# import json
# import glob
# import pandas as pd
# from sklearn.decomposition import PCA
# import py_vncorenlp
# from elasticsearch import Elasticsearch 

# from DataPineLine.preprocessing import load_data

# es = Elasticsearch('http://localhost:9200',
#                    basic_auth=('elastic', 'trongnt123'))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Model:
    def __init__(self):
        cache_dir = './models'
        self.phobert = AutoModel.from_pretrained('./Datapipeline/models/models--vinai--phobert-base/snapshots/weight', cache_dir=cache_dir)
        self.tokenizer = AutoTokenizer.from_pretrained('./Datapipeline/models/models--vinai--phobert-base/snapshots/weight', cache_dir=cache_dir)

    # @staticmethod
    def encoding(self, text, maxlen = 239):

        self.phobert.to(device)

        encoding = self.tokenizer.encode_plus(text,
                    truncation=True,
                    add_special_tokens=True,
                    max_length= maxlen,
                    padding='max_length',
                    return_attention_mask=True,
                    return_token_type_ids=False,
                    return_tensors='pt',)
        
        input_ids = encoding.input_ids.to(device)
        attention_mask = encoding.attention_mask.to(device)
        with torch.no_grad():
            features = self.phobert(input_ids = input_ids, attention_mask=attention_mask)
        output = features.pooler_output.squeeze(0).to('cpu').numpy()
        # hidden_state = features.last_hidden_state.squeeze(0).to('cpu').numpy()
        # dimension = 3
        # pca = PCA(n_components=dimension)
        # flatten_hidden_state = pca.fit_transform(hidden_state).flatten()
        return output.tolist()
        

    # def convert_vncore(self, text):
    #     rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='D:/airflow_tutorial/MMIR/BE/Datapipeline/VnCoreNLP')
    #     tokenizer = rdrsegmenter.word_segment(text)
    #     tokenizer = ''.join(tokenizer)
    #     os.chdir('..')
    #     return tokenizer



# def convert_chunkdf(df):
#     chunk_size = 1000
#     num_chunks = len(df) // chunk_size + 1


#     for i in range(num_chunks):
#         start_idx = i * chunk_size
#         end_idx = (i + 1) * chunk_size
#         chunk_df = df.iloc[start_idx:end_idx].reset_index()
#         chunk_df = chunk_df.drop(['index', 'Unnamed: 0'], axis=1)
#         chunk_df.to_csv(f'./chunkdata/chunk_df{i}.csv')
#     return "done"

# def preprocessing(df):
#     # fill nan value by ''
#     df = df.fillna('')
#     return df

# def tokenizer(sentence, rdrsegmenter):
#     tokenizer = rdrsegmenter.word_segment(sentence)
#     tokenizer = ''.join(tokenizer)
#     return tokenizer

# def search(model, query, maxlen):
#     rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='D:/airflow_tutorial/VnCoreNLP')
#     query_token = tokenizer(query, rdrsegmenter)
#     os.chdir('..')
#     query_vector = encoding(query_token, model, maxlen)
    
#     q_ = {
#         "field": "tokenizedVector",
#         "query_vector": query_vector,
#         "k" : 2,
#         "num_candidates": 100,
#     }
    
#     res = es.knn_search(index='news', knn=q_, source=['title', 'link', 'date', 'description', 'paragraphs'])
#     print(res)
    
    
# if __name__ == '__main__':
#     maxlen = 239
#     model = Model()
#     query = 'Vinhomes dự kiến vận hành khu đô thị gần 1 tỷ USD từ 2026'
    # search(model, query, maxlen)
    # df = pd.read_csv('./after_token.csv')
    # df = preprocessing(df)
    # df = df.drop('Unnamed: 0', axis=1)
    # print('embedding')
    # df['tokenizedVector'] = df['tokenized'].apply(lambda x : encoding(x, model, maxlen))
    # df = df.drop(['des_n', 'tokenized'], axis=1)
    # records = df.to_dict('records')
    # output_path = f'./merge.jsonl'
    # print('start store file')
    # with open(output_path, 'w', encoding='utf-8') as f:
    #     for rec in records:
    #         json.dump(rec, f, ensure_ascii=False)
    #         f.write('\n')
    # list_chunk_df = os.listdir('./chunkdata')
    
    # for chunk_df in list_chunk_df:
    #     df = pd.read_csv('./chunkdata/'+ chunk_df)
        
    #     df['tokenizedVector'] = df['tokenized'].apply(lambda x : encoding(x, model, maxlen))
    #     df = df.drop(['Unnamed: 0', 'des_n', 'tokenized'], axis=1)
    #     records = df.to_dict('records')
    #     output_path = f'./encoding_out/{chunk_df.replace(".csv",".jsonl")}'
    #     print(output_path)
    #     with open(output_path, 'w', encoding='utf-8') as f:
    #         for rec in records:
    #             json.dump(rec, f, ensure_ascii=False)
    #             f.write('\n')
    #     print(f"done {chunk_df.split('/')[-1]}")
   
    



