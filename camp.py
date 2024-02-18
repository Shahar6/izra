import requests
from bs4 import BeautifulSoup
import time
import re
import winsound


spy_data = {'spy': 'שלח את המרגלים'}
login_url = "http://s1.izra.co.il/login"
login_data = {"email": "vampire421@gmail.com", "password": "30121992", "rem": "on", "reg": "התחברות >>"}


def getP(session, page):
    while True:
        try:
            response = session.get(page, timeout = 1)
            if response.status_code == 200:
                break
            else:
                time.sleep(1)
        except:
            continue
    return response


def login():
    global login_data
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


def attack(s, data, url):
    while True:
        try:
            response = s.post(url, data = data, timeout = 1)
            if response.status_code == 200:
                break
            else:
                time.sleep(1)
        except:
            continue
    return response

counter = 0
number = 9857
keep_attack = True
time.sleep(60*60)
while keep_attack:
    s = login()
    s.headers['Referer'] = 'http://s1.izra.co.il'
    for i in range(5):
        r = getP(s, f'http://s1.izra.co.il/attack/?attack_id={number}')
        soup = BeautifulSoup(r.content, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})
        csrf_token_value = csrf_token['value']
        attack_data = {'turns': '10', 'csrf_token': csrf_token_value ,'defender_id': f"{number}" , 'go': 'תקוף'}
        t = attack(s, attack_data, f'http://s1.izra.co.il/attack/attack/?attack_id={number}')
        soup = BeautifulSoup(t.content, 'html.parser')
        string_exists = "מגן חיילים פעיל" in soup.get_text() or "הפסדת" in soup.get_text()
        if string_exists:
            keep_attack = False
            winsound.PlaySound('Windows Background.wav', winsound.SND_FILENAME | winsound.SND_NOWAIT)
            break
        if i == 4:
            counter = counter + 5
            print(f'{counter} successful attacks')
    print('sleeping for an hour')
    time.sleep(3610)





