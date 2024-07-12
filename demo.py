import requests
import yarl
import json

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
    data = r.json()
    return data

def world():
    url = yarl.URL(HOST) / WORLD
    r = requests.get(url, headers=HEADERS)
    data = r.json()
    return data


def main():
    print(json.dumps(units()))
    print(json.dumps(world()))


if __name__ == "__main__":
    print("----- super proga -----")
    main()