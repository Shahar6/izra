import requests
from bs4 import BeautifulSoup
import time
import re
import math
import random
import winsound


spy_data = {'spy': 'שלח את המרגלים'}
login_url = "http://s1.izra.co.il/login"
email = 'shaharizra1@gmail.com'#input('Enter email: ')
password = '1234512345'#input('Enter password: ')
login_data = {"email": email, "password": password, "rem": "on", "reg": "התחברות >>"}



# P for persistent
def getP(session, page):
    while True:
        try:
            response = session.get(page, timeout = 1)
            if response.status_code == 200:
                break
            else:
                switch_proxy(session)
        except:
            continue
    return response



def login(data = login_data):
    s = requests.Session()
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    s.headers.update({'User-Agent': custom_user_agent})
    while True:
        try:
            response = s.post(login_url, data = data, timeout = 1)
            if response.status_code == 200:
                break
            else:
                time.sleep(1)
        except:
            continue
    return s

def scout(session, url, spy_data):
    while True:
        try:
            response = session.post(url, data = spy_data, timeout = 1)
            if response.status_code == 200:
                break
            else:
                time.sleep(1)
        except:
            continue
    return response
    

def format_with_commas(number):
    locale.setlocale(locale.LC_ALL, '')
    return locale.format_string("%d", number, grouping=True)

def thread_scan():
    s = login()
    prev = 0
    log_data = {"email": 'something@gmail.com', "password": '30121992', "rem": "on", "reg": "התחברות >>"}
    s2 = login(log_data)
    s2.headers['Referer'] = 'http://s1.izra.co.il'
    while True:
        response = scout(s, f"http://s1.izra.co.il/spy/spyuser/?targetId=70594", spy_data)
        soup = BeautifulSoup(response.content, 'html.parser')
        if 'חופשות שנוצלו:' in soup.text:
            time.sleep(10)
            continue
        attack_power = int(re.findall('עוצמת התקפה<span class="num">([0-9,]*)</span>', str(soup))[0].replace(',',''))
        print(attack_power)
        if attack_power > 25780659191280:
            r = getP(s2, 'http://s1.izra.co.il/configurations')
            soup = BeautifulSoup(r.content, 'html.parser')
            csrf_token = soup.find('input', {'name': 'csrf_token'})
            csrf_token_value = csrf_token['value']
            url_data = 'http://s1.izra.co.il/configurations/gotovacation'
            vac_data = {'csrf_token': csrf_token_value, 'vacin': 'צא לחופשה!'}
            s2.post(url_data, data = vac_data)
            winsound.PlaySound('Windows Background.wav', winsound.SND_FILENAME | winsound.SND_NOWAIT)
            break
        if attack_power > prev:
            prev = attack_power
            winsound.PlaySound('Windows Background.wav', winsound.SND_FILENAME | winsound.SND_NOWAIT)
        time.sleep(5)
        
thread_scan()



