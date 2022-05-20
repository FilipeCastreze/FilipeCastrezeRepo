import requests
import time

r = requests.get("https://www.sef.pt/pt/mySEF/Pages/default.aspx",auth=("castreze@gmail.com","N@t@lia1991"))
print(r.status_code)
