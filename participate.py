import requests
# from .token import TOKEN

HEADERS = {"X-Auth-Token": "6686ce63049946686ce6304999"}
r = requests.put("https://games-test.datsteam.dev/play/zombidef/participate", headers=HEADERS)
print(r.json())