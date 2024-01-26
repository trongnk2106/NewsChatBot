from elasticsearch import Elasticsearch

from model import Model
import py_vncorenlp


es = Elasticsearch('http://localhost:9200',
                   basic_auth=('elastic', 'trongnt123'))

import os
def get_all_indices():
    return list(es.indices.get_alias().keys())


def get_lastid(index_name):
        # Truy vấn để lấy tài liệu cuối cùng
    query = {
    "query": {"match_all": {}},
    "size": 1,
    "sort": [{"_doc": {"order": "desc"}}]
}

# Thực hiện truy vấn
    result = es.search(index=index_name, body=query)
    res = result['hits']['hits'][0]['_id']

    return res

def getall_data(index):
    query = {"query" : {"match_all" : {}}}

    res = es.count(index=index, body=query)
    
    
def search(query):
    index = get_all_indices()[0]
    model = Model()
    query_vector = model.encoding(query)
    # q_ = {
    #     "field": "embedding",
    #     "query_vector": query_vector,
    #     "k" : 2,
    #     "num_candidates": 100,
    # }
    
    # # res = es.knn_search(index=index, knn=q_, source=['title', 'link', 'date','author', 'description', 'paragraphs'])
    # result = es.search(index=index, body={"query": {"knn": q_}}, _source=['title', 'link', 'date', 'author', 'description', 'paragraphs'])
    
    result = es.search(index=index, body={
    "size" : 10,
    "query": {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }
    }, _source=['title', 'link', 'date', 'author', 'description', 'paragraphs']) # select * 
    
    
    
    return result

def full_textsearch(query):
    index = get_all_indices()[0]
    result = es.search(index=index, body={
    "size" : 10,
    "query": {
        "multi_match": {
            "query": query,
            "fields": ["title", "description", "paragraphs"]
        }
    }
    }, _source=['title', 'link', 'date', 'author', 'description', 'paragraphs'])
    
    return result


# if __name__ == "__main__":
    
#     # get_lastid(indices)
#     # rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='D:/airflow_tutorial/MMIR/BE/Datapipeline/VnCoreNLP')

    
#     # query = 'TP HCM - Căn hộ hai phòng ngủ đa năng (2PN+1) tại The Privia có thiết kế cửa sổ lớn trong mỗi phòng, kèm không gian phụ đa năng linh hoạt chuyển đổi mục đích sử dụng'
#     query_ = 'Giá nhà liền thổ TP HCM tăng gần 7 lần trong một thập kỷ'
#     # query_token = rdrsegmenter.word_segment(query_)
#     # os.chdir('../..')
#     model = Model()
#     query_vector = model.encoding(query_)
    
#     search(query_vector, indices)