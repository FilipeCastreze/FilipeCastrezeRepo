from re import T
import requests

url_Login = "https://www.sef.pt/_layouts/15/SEF.WebControls/LoginPage.aspx?ReturnUrl=%2fpt%2fmySEF%2f_layouts%2f15%2fAuthenticate.aspx%3fSource%3d%252Fpt%252FmySEF%252FPages%252Fautenticacao%252Despecial%252Easpx%253FauthRedirect%253D%25252fpt%25252fmySEF%25252fPages%25252frenovacao%252Dautomatica%252Easpx&Source=%2Fpt%2FmySEF%2FPages%2Fautenticacao%2Despecial%2Easpx%3FauthRedirect%3D%252fpt%252fmySEF%252fPages%252frenovacao%2Dautomatica%2Easpx"
url_Renovacao = "https://www.sef.pt/pt/mySEF/Pages/autenticacao-especial.aspx?authRedirect=%2fpt%2fmySEF%2fPages%2frenovacao-automatica.aspx"

r = requests.get(url_Login,auth=("castreze@gmail.com","N@t@lia1991"))
header = r.headers
print("\nResponse code: " + str(r.status_code) +"\n")

for i in header:
    print(str(i) + " : " + str(header[i]))