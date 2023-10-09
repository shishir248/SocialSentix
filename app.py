import json
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from typing import List
import datetime as dt
from bardapi import Bard
import itertools

app = FastAPI()

top = 10

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/bard/getAnswer/{ques}")
def get_answers(ques):
    consumer = get_consumer(ques)
    return consumer

def get_consumer(ques):
    token = "bwjoHefQZkzzO6K5RKAkht0hMQl2QhduqYYyiGts1h2FLLnwmNAWabPseBBcpCf-x42w9w."
    print(ques)
    response = Bard(token=token).get_answer(ques)['content']
    print(response)
    return response

@app.get("/api", response_model=None)
def get_info(symbol: List[str] = Query(None), limit: int|None = None, start: dt.date|None = None, end: dt.date|None = None):
    # For API
    data_file = open("./new_symbols.json", "r")
    data = json.load(data_file)
    data_file.close()

    r = data
    if symbol:
        symbol = list(filter(lambda x: x != "", symbol))
    if symbol and len(symbol) > 0:
        r = {}
        try:
            for s in symbol:
                r[s.upper()] = data[s.upper()]
        except:
            return {"status": 404, "message": "Invalid Symbol"}

    if limit and not start and not end:
        # r = data.copy()
        if limit == -1:
            return r
        for k,v in r.items():
            if len(v['comments']) > limit:
                r[k]['comments'] = v['comments'][:limit]

    if start and end:
        try:
            t = {}
            for k,v in r.items():
                filtered_comments = []
                for comment in v['comments']:
                    if start < dt.datetime.strptime(comment['timestamp'], '%Y-%m-%d %H:%M:%S').date() < end:
                        filtered_comments.append(comment)
                v['comments'] = filtered_comments
                if len(filtered_comments) > 0:
                    t[k] = v
            r = t
        except Exception as error:
            print(error)
            return {"status": 404, "message": f'{error}'}
    headers = {"Cache-Control": "no-store"}
    return JSONResponse(content = { "status" : 200, "data": r},  headers = headers)

@app.get("/api/popular")
async def get_popular(top: int = top, limit: int|None = None, start: dt.date|None = None, end: dt.date|None = None):
    data_file = open("./new_symbols.json", "r")
    data = json.load(data_file)
    data_file.close()

    r = data

    tops = dict(sorted(data.items(),key=lambda item: len(item[1]['comments']), reverse=True))
    r = dict(itertools.islice(tops.items(), top))

    if limit and not start and not end:
        for k,v in r.items():
            r[k]['comments'] = v['comments'][:limit]
    if start and end:
        try:
            t = {}
            for k,v in r.items():
                filtered_comments = []
                for comment in v['comments']:
                    if start < dt.datetime.strptime(comment['timestamp'], '%Y-%m-%d %H:%M:%S').date() < end:
                        filtered_comments.append(comment)
                v['comments'] = filtered_comments
                t[k] = v
            r = t
        except Exception as error:
            print(error)
            return {"status": 404, "message": f'{error}'}
    return { "status" : 200, "data": r }

