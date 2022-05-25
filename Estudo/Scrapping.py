from re import T
import requests

url_Login = "https://www.sef.pt/_layouts/15/SEF.WebControls/LoginPage.aspx?ReturnUrl=/_layouts/15/error.aspx&Source=%2fpt%2fmySEF%2fPages%2fautenticacao-especial.aspx%3fauthRedirect%3d%252Fpt%252FmySEF%252FPages%252Frenovacao-automatica.aspx"
url_Renovacao = "https://www.sef.pt/pt/mySEF/Pages/autenticacao-especial.aspx?authRedirect=%2fpt%2fmySEF%2fPages%2frenovacao-automatica.aspx"

email = "castreze@gmail.com"
password = "N@t@lia1991"
ar = "L29178K46"

dataRenov = {
    "txtAuthPanelEmail":email,
    "txtAuthPanelPassword":password,
    "txtAuthPanelDocument":ar}

r = requests.get(url_Login,auth=(email,password))
print("\nResponse code Login: " + str(r.status_code) +"\n")

r = requests.post(url_Renovacao,data=dataRenov)
header = r.headers
print("Response code Renovação: " + str(r.status_code) +"\n")

for i in header:
   print(str(i) + " : " + str(header[i]))