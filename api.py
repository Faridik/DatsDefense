import requests
import yarl
from datetime import datetime
import pathlib
import json
from functools import wraps

HEADERS = {"X-Auth-Token": "6686ce63049946686ce6304999"}

HOST = "https://games.datsteam.dev/"
UNITS = "play/zombidef/units"
COMMAND = "play/zombidef/command"
WORLD = "play/zombidef/world"
PARTICIPATE = "play/zombidef/participate"
SAVE_DATA = True


def save_data(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if SAVE_DATA:
            try:
                realm_name = str(result.get("realmName", "no-realm"))
                p = pathlib.Path("dataset") / realm_name / func.__name__ /( datetime.now().strftime("%Y-%m-%d %H.%M.%S") + ".json")
                p.parent.mkdir(parents=True, exist_ok=True)
                with open(p, "w") as f:
                    json.dump(result, f, indent=2)
            except Exception as e:
                print("Failed to save data", e)
                raise e
        return result
    return wrapper
 
@save_data
def command(data):
    url = yarl.URL(HOST) / COMMAND
    try:
        r = requests.post(url, json=data, headers=HEADERS)
        response_data = r.json()
    except:
        response_data = {}
        print("Failed to send command")
    return response_data

@save_data
def units():
    url = yarl.URL(HOST) / UNITS
    r = requests.get(url, headers=HEADERS)
    try:
        data = r.json()
    except:
        data = {}
    return data

@save_data
def world():
    url = yarl.URL(HOST) / WORLD
    try:
        r = requests.get(url, headers=HEADERS)
        data = r.json()
    except:
        data = {}
    return data

@save_data
def participate():
    url = yarl.URL(HOST) / PARTICIPATE
    try:
        r = requests.put(url, headers=HEADERS)
        data = r.json()
    except:
        data = {}
    return data