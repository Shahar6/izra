import requests
import winsound
from bs4 import BeautifulSoup
import re
import time

spy_data = {'spy': 'שלח את המרגלים'}
login_url = "http://s1.izra.co.il/login"
spell_data = {"res_hour_mad": "10", "magic_res_defense": "הפעל את קסם מגן המשאבים"}
login_data = {"email": input('enter email: '), "password": input('enter password: '), "rem": "on", "reg": "התחברות >>"}


# P for persistent
def getP(session, page):
    while True:
        try:
            response = session.get(page, timeout = 1)
            if response.status_code == 200:
                break
            else:
                print('invalid response')
                time.sleep(1)
        except:
            continue
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
    check = False
    while True:
        try:
            response = s.post(url, data = data, timeout = 1)
            if response.status_code == 200:
                break
            else:
                if not check:
                    check = True
                    print('invalid response')
        except:
            continue

def attack(s, data, url):
    while True:
        try:
            response = s.post(url, data = data, timeout = 1)
            break
        except:
            continue
    return response

def spell(s, data, url):
    while True:
        try:
            response = s.post(url, data = data, timeout = 1)
            break
        except:
            continue

def thread_op(attack_ids, threshold):
    ses = login()
    ses.headers['Referer'] = 'http://s1.izra.co.il'
    print('starting')
    while len(attack_ids) > 0:
        for url in attack_ids:
            use_spell = False
            keep_attack = True
            r = getP(ses, url)
            soup = BeautifulSoup(r.content, 'html.parser')
            print(soup)
            string_exists = "השחקן בחופשה" in soup.get_text()
            gold = int(re.findall('gold.png" width="40"/>זהב             <br/>([0-9,]+)</a>', str(soup))[0].replace(',',''))
            if not string_exists and gold > threshold:
                while keep_attack:
                    try:
                        r = getP(ses, url)
                        soup = BeautifulSoup(r.content, 'html.parser')
                        csrf_token = soup.find('input', {'name': 'csrf_token'})
                        csrf_token_value = csrf_token['value']
                        attack_data = {'turns': '10', 'csrf_token': csrf_token_value ,'defender_id': f"{url[39:]}" , 'go': 'תקוף'}
                        r = attack(ses, attack_data, f'http://s1.izra.co.il/attack/attack/?attack_id={url[39:]}')
                        soup = BeautifulSoup(r.content, 'html.parser')
                        span_tag = soup.find('span', class_='row color-gold')
                        if(span_tag is None):
                            time.sleep(0.6)
                            break
                        gold = int(span_tag.get_text().replace(',', ''))
                        span_tag = soup.find('span', class_='row color-iron')
                        iron = int(span_tag.get_text().replace(',', ''))
                        span_tag = soup.find('span', class_='row color-wood')
                        wood = int(span_tag.get_text().replace(',', ''))
                        span_tag = soup.find_all('span', class_='row color-food')
                        food = 0
                        for tag in span_tag:
                            tag = int(tag.get_text().replace(',', ''))
                            if tag > food:
                                food = tag
                        if(gold+iron+wood+food) < 250000:
                            attack_ids.remove(url)
                            keep_attack = False
                        else:
                            use_spell = True
                        print(f"attacked {url[39:]}")
                    except Exception as e:
                        print(f'err {e} {url[39:]}')
                        keep_attack = False
                if use_spell:
                   spell(ses, spell_data, "http://s1.izra.co.il/hero/magicresdef/")
            time.sleep(0.6)

attack_ids = []
keep = True
print("Below you may enter ID's to camp on, recommended no more than 4 for best performance")
while keep:
    em = input("Enter ID: ")
    attack_ids = attack_ids + em
    keep = input("Do you want to enter another member? (enter 'y' if yes): ") == 'y'
attack_links = [f"http://s1.izra.co.il/attack/?attack_id={id}" for id in attack_ids]
threshold = int(input("amount of gold to attack from: "))
thread_op(attack_links, threshold)

input("finished, press enter to close")

