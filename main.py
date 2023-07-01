import os, json
import requests
from fastapi import FastAPI, HTTPException

PATH = os.path.join("conf", "conf.json")
INFO_ENDPOINT = "/user/icon_desc.json?type={}"
ACTION_ENDPOINT = "/user/action.cgi?type={}&num{}={}"

app = FastAPI()

#loading config file
conf = {}
with open(PATH, "r") as conf_file:
    conf = json.load(conf_file)

@app.get("/")
async def root():
    return {"message": "Comelit api"}

@app.get("/get_map")
async def get_map():
    return conf["map"]

@app.get("/get_categories")
async def get_cats():
    return {"categories":[cat for cat in conf["map"]]}

@app.get("/{category}/get_elements")
async def get_cats(category:str):
    try:
        el = conf["map"][category]
        return el
    except KeyError:
        raise HTTPException(status_code=404, detail="Category not found")

@app.get("/{category}/{ref_id}/{action}")
async def act(category: str, ref_id: int | str, action:str):
    #possibility to use ref id to be added
    act = {
        "on": 1,
        "off": 0
    }
    requests.get(conf["url"]+ACTION_ENDPOINT.format(category, act[action], ref_id))
    r = requests.get(conf["url"]+INFO_ENDPOINT.format(category))
    return r.json()