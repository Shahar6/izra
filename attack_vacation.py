import requests
import winsound
from bs4 import BeautifulSoup
import time


response = requests.get("http://worldtimeapi.org/api/ip")
data = response.json()
current_year = data['datetime'][:4]
current_month = int(data['datetime'][5:7])
current_day = int(data['datetime'][8:10])


if not (current_year == "2024" and current_month < 3):
    print('License expired you may contact me to renew on discord, my user-name is _shahar')
    input("Press Enter to exit...")
    exit()
    


login_url = "http://s1.izra.co.il/login"
print('Hello, this program is meant to attack users as they leave vacation in izra.co.il')
print('For support, you can reach _shahar in discord')


leader_email = 'vampire421@gmail.com'#input("enter your account's email: ")
leader_password = '30121991'#input("enter password: ")
login_data = {"email": leader_email, "password": leader_password, "rem": "on", "reg": "התחברות >>"}
#spell_data = {"res_hour_mad": '3', "magic_res_defense": "הפעל את קסם מגן המשאבים"}
spell_data = {"res_hour_mad": '0', "magic_res_defense": "הפעל את קסם מגן המשאבים"}
#spell_data = {"res_hour_mad": input('Resource shield hours after attacking:(0-23) '), "magic_res_defense": "הפעל את קסם מגן המשאבים"}


# P for persistent
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



def thread_op(attack_ids, threshold):
    print('starting.. keep the program running')
    ses = login()
    ses.headers['Referer'] = 'http://s1.izra.co.il'
    while len(attack_ids) > 0:
        for url in attack_ids:
            use_spell = False
            keep_attack = True
            r = getP(ses, url)
            soup = BeautifulSoup(r.content, 'html.parser')
            string_exists = "השחקן בחופשה" in soup.get_text()
            if not string_exists:
                while keep_attack:
                    try:
                        r = getP(ses, url)
                        soup = BeautifulSoup(r.content, 'html.parser')
                        csrf_token = soup.find('input', {'name': 'csrf_token'})
                        csrf_token_value = csrf_token['value']
                        attack_data = {'turns': '10', 'csrf_token': csrf_token_value ,'defender_id': f"{url[39:]}" , 'go': 'תקוף'}
                        r = attack(ses, attack_data, f'http://s1.izra.co.il/attack/attack/?attack_id={url[39:]}')
                        print(f"attacked {url[39:]}")
                        soup = BeautifulSoup(r.content, 'html.parser')
                        span_tag = soup.find('span', class_='row color-gold')
                        if(span_tag is None):
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
                        if(gold + iron + wood + food) < threshold:
                            attack_ids.remove(url)
                            keep_attack = False
                        else:
                            use_spell = True
                    except Exception as e:
                        print(f'err {e} {url[39:]}')
                        attack_ids.remove(url)
                        keep_attack = False
                if use_spell:
                    spell(ses, spell_data, "http://s1.izra.co.il/hero/magicresdef/")
                    winsound.PlaySound('Windows Background.wav', winsound.SND_FILENAME|winsound.SND_NOWAIT)
            time.sleep(0.6)
            


ids = []
'''keep = True
print("Below you may enter ID's to camp on, recommended no more than 4 for best performance")
while keep:
    em = input("Enter ID: ")
    ids.append(em)
    keep = input("Do you want to enter another member? (enter 'y' if yes): ") == 'y'
#threshold = int(input("minimum amount of resources (gold + wood + iron + food) taken to keep attacking: (example: 100000 means, stop attacking if you get only 99999) "))
'''
ids = ['71908']
attack_links = [f"http://s1.izra.co.il/attack/?attack_id=" + iden for iden in ids]


thread_op(attack_links, 600000)


print("")
input("finished, press enter to close")

