import requests
import time

i = 1
while True:
    print(f"Попытка зарегистрироваться №{i}")
    HEADERS = {"X-Auth-Token": "6686ce63049946686ce6304999"}
    try:
        r = requests.put("https://games-test.datsteam.dev/play/zombidef/participate", headers=HEADERS)
        data = r.json()
        print(data)
    except:
        print("Ошибка...")
    time.sleep(100)
    i += 1