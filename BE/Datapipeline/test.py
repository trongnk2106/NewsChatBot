from elasticsearch import Elasticsearch
import os
# use tdqm to show progress bar
from tqdm import tqdm




es = Elasticsearch('http://localhost:9200',
                   basic_auth=('elastic', 'trongnt123'))


# def create_index():
#     es.indices.create(index='news', mappings=indexMapping)

def get_indices():
    last_id = es.count(index='news')['count'] 
    print(last_id)
    
def get_doc():
    result = es.search(index='news', body={"query": {"match_all": {}}})

# In ra kết quả
    for hit in result["hits"]["hits"]:
        print(hit)
        break
get_indices()
# get_doc()