import requests
import yarl
import json
import time
import pathlib

HEADERS = {"X-Auth-Token": "6686ce63049946686ce6304999"}

HOST = "https://games-test.datsteam.dev/"
UNITS = "play/zombidef/units"
COMMAND = "play/zombidef/command"
WORLD = "play/zombidef/world"



def command(data):
    url = yarl.URL(HOST) / COMMAND
    r = requests.post(url, data=data, headers=HEADERS)
    data = r.json()
    return data

def units():
    url = yarl.URL(HOST) / UNITS
    r = requests.get(url, headers=HEADERS)
    try:
        data = r.json()
    except:
        data = None
    return data

def world():
    url = yarl.URL(HOST) / WORLD
    r = requests.get(url, headers=HEADERS)
    try:
        data = r.json()
    except:
        data = None
    return data