from fastapi import FastAPI
from pydantic import BaseModel
from onlineapi import search_in_ddg

app = FastAPI()

class Msg(BaseModel):
    msg: str


@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}


@app.get("/path")
async def demo_get():
    return {"message": "This is /path endpoint, use a post request to transform the text to uppercase"}


@app.post("/path")
async def demo_post(inp: Msg):
    return {"message": inp.msg.upper()}


@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}


@app.get("/onlineapi")
async def onlineapi_get():
    return {"message": "This is /onlineapi endpoint, use a post request to search the text in site:https://datagy.io/"}


@app.post("/onlineapi")
async def onlineapi_post(inp: Msg):
    search_rtn = search_in_ddg(inp.msg)
    # {"most_common_apis": most_common_apis, "search_page": search_page, "apis_count": apis_count}
    return search_rtn