import requests
import time

r = requests.get("https://twitter.com/home")
print(r.status_code)
