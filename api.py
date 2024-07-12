import requests
import yarl

HEADERS = {"X-Auth-Token": "6686ce63049946686ce6304999"}

HOST = "https://games-test.datsteam.dev/"
UNITS = "play/zombidef/units"
COMMAND = "play/zombidef/command"
WORLD = "play/zombidef/world"
PARTICIPATE = "play/zombidef/participate"


def command(data):
    url = yarl.URL(HOST) / COMMAND
    try:
        r = requests.post(url, json=data, headers=HEADERS)
        response_data = r.json()
    except:
        response_data = {}
        print("Failed to send command")
    return response_data

def units():
    url = yarl.URL(HOST) / UNITS
    r = requests.get(url, headers=HEADERS)
    try:
        data = r.json()
    except:
        data = {}
    return data

def world():
    url = yarl.URL(HOST) / WORLD
    try:
        r = requests.get(url, headers=HEADERS)
        data = r.json()
    except:
        data = {}
    return data

def participate():
    url = yarl.URL(HOST) / PARTICIPATE
    try:
        r = requests.put(url, headers=HEADERS)
        data = r.json()
    except:
        data = {}
    return data