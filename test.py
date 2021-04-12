import urllib.request
import json

with urllib.request.urlopen("http://127.0.0.1:5000/test") as url:
    data = json.loads(url.read().decode())

    for key, value in data.items():
        print(f'{key} has value {value}')

