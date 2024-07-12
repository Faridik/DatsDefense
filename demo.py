import requests
import yarl
import json
import time
import pathlib
from attack import nearest_enemies

HEADERS = {"X-Auth-Token": "6686ce63049946686ce6304999"}

HOST = "https://games-test.datsteam.dev/"
UNITS = "play/zombidef/units"
COMMAND = "play/zombidef/command"
WORLD = "play/zombidef/world"



def command(data):
    url = yarl.URL(HOST) / COMMAND
    r = requests.post(url, json=data, headers=HEADERS)
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


def main():
    print(json.dumps(units()))
    print(json.dumps(world()))


if __name__ == "__main__":
    print("----- super proga -----")
    i = 0
    while True:
        i += 1
        units_data = units()
        world_data = world()
        if units_data is None or world_data is None:
            continue
        if (err := units_data.get("error")) is not None:
            print(err)
            time.sleep(3)
            continue


        # Статистика базы.
        base_size = len(units_data.get("base") or [])
        base_health = 0
        for cell in (units_data.get("base") or []):
            base_health += cell.get("health", 0)
        print("TURN ", units_data['turn'], f"BASE SIZE = {base_size}, HP: {base_health}.")
        
        
        units_dir = pathlib.Path(f"dataset/{units_data['realmName']}/units")
        world_dir = pathlib.Path(f"dataset/{units_data['realmName']}/world")
        command_dir = pathlib.Path(f"dataset/{units_data['realmName']}/commands")
        units_dir.mkdir(parents=True, exist_ok=True)
        world_dir.mkdir(parents=True, exist_ok=True)
        command_dir.mkdir(parents=True, exist_ok=True)
        with open(units_dir / f"turn-{units_data['turn']}.json", "w") as f:
            json.dump(units_data, f, indent=2)
        with open(world_dir / f"world.json", "w") as f:
            json.dump(world_data, f, indent=2)

        enemy = nearest_enemies(units_data)
        command_result = command({"attack": nearest_enemies(units_data)})
        print(command_result)
        with open(command_dir / f"command-{time.time()}.json", "w") as f:
            json.dump(command_result, f, indent=2)

        time.sleep(5)
        
