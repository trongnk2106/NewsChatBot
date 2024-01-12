from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import sys

sys.path.append('../../MMIR/BE/Datapipeline')

from Bot import Bot

app = FastAPI()

class DataItem(BaseModel):
    title : str
    date : str
    description : str
    paragraphs : str
    author : str
    link : str
    


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
    
    pass

@app.get("/chatbot")
async def chatbot(query : str, mode : str):
    if mode == 'Vector Search':
        bot = Bot()
        result = bot.botchat(query, mode)
        # print(result)
        # result = {'result' : result}
        return result
    else :
        bot = Bot()
        result = bot.botchat(query, mode)

        return result

@app.get("/search")
async def search(query : str, mode : str):
    # print(query)
    if mode == 'Vector Search':
        bot = Bot()
        result = bot.search_(query, mode)
        # print(result)
        result = {'result' : result}
        return result
    else:
        bot = Bot()
        result = bot.search_(query, mode)
        # print(result)
        result = {'result' : result}
        return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port = 9000)

