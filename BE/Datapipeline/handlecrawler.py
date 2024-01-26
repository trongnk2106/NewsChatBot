from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from elasticsearch import Elasticsearch

from model import Model
from elasticsearch import Elasticsearch
from indexMapping import indexMapping

from tqdm import tqdm

from embed import embedding




app = FastAPI()




es = Elasticsearch('http://localhost:9200',
                   basic_auth=('elastic', 'trongnt123'))


def get_indices():
    print(es.indices.get_alias().keys())

async def push_data(data):
    #using tqdm to show progress bar
    
    #get how many data in elastic
    last_id = es.count(index='news')['count'] 
    
    
    for idx, rec in tqdm(enumerate(data)):
        try:
            # print(idx)
            es.index(index='news', document=rec, id=idx + 1 + last_id)
        except Exception as e:
            print(e)
            print(idx)
            print(rec['title'], '\n', rec['link'], '\n', rec['date'] ,'\n', type(rec['author']) ,'\n', rec['description'] ,'\n', type(rec['paragraphs']))
            break
            # print(rec)
            
    return "done"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message" : "Hello World1111"}

@app.get("/updatedata")
async def revice_data():
        
    data = await embedding()
    print(data)
    status = await push_data(data)
    return {"message" : status}
    # return "done"



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port = 3000)

