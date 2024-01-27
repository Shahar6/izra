import requests
import winsound
from bs4 import BeautifulSoup
import re
import time


spy_data = {'spy': 'שלח את המרגלים'}
login_url = "http://s1.izra.co.il/login"
login_data = {"email": "vampire421@gmail.com", "password": "30121991", "rem": "on", "reg": "התחברות >>"}


spell_data1 = {"res_hour_mad": "3", "magic_res_defense": "הפעל את קסם מגן המשאבים"}
spell_data2 = {"sol_hour_mad": "23", "magic_sol_defense": "הפעל את קסם מגן החיילים"}


def getP(session, page):
    while True:
        try:
            response = session.get(page, timeout = 1)
            if response.status_code == 200:
                break
            else:
                sync_print('invalid response')
        except:
            continue
    time.sleep(0.5)
    return response


def login():
    s = requests.Session()
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    s.headers.update({'User-Agent': custom_user_agent})
    while True:
        try:
            response = s.post(login_url, data = login_data, timeout = 1)
            break
        except:
            continue
    return s


def spell(s, data, url):
    while True:
        try:
            response = s.post(url, data = data, timeout = 1)
            break
        except:
            continue


ses = login()
ses.headers['Referer'] = 'http://s1.izra.co.il'
r = getP(ses, "http://s1.izra.co.il/vacation")
soup = BeautifulSoup(r.content, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrf_token'})
csrf_token_value = csrf_token['value']
ret_data = {'csrf_token': csrf_token_value, 'come_back' : 'חזור מהחופשה'}
ses.post(f'http://s1.izra.co.il/vacation/comeback', data = ret_data)
spell(ses, spell_data1, "http://s1.izra.co.il/hero/magicresdef/")
#spell(ses, spell_data2, "http://s1.izra.co.il/hero/magicsoldef/")
