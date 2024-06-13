import requests
import winsound
import threading
from bs4 import BeautifulSoup
import re
import time
from math import ceil

adder = 0
p_user = 'rjjtzjxw'
p_pass = 'u8aovf7qutdn'
ips = ['23.109.208.30:6554', '104.238.8.190:6048', '23.109.225.254:5885', '104.238.8.100:5958', '23.109.232.242:6162',
       '154.92.125.62:5363', '104.238.9.112:6565', '154.92.124.232:5260', '104.238.9.90:6543', '23.109.225.56:5687',
       '104.222.187.196:6320', '23.109.225.185:5816', '23.109.225.168:5799', '23.109.225.93:5724', '154.92.124.80:5108',
       '23.109.208.183:6707', '104.222.187.248:6372', '23.109.232.79:5999', '154.92.124.121:5149', '154.92.124.7:5035',
       '104.222.187.217:6341', '104.222.187.89:6213', '23.109.232.237:6157', '23.109.232.93:6013',
       '104.222.187.182:6306', '104.238.9.198:6651', '104.222.185.235:5798', '109.207.130.173:8180',
       '23.109.208.108:6632', '23.109.232.41:5961', '154.92.125.198:5499', '154.92.125.215:5516',
       '109.207.130.222:8229', '104.238.8.9:5867', '23.109.232.166:6086', '109.207.130.45:8052', '23.109.208.81:6605',
       '154.92.124.92:5120', '104.238.9.50:6503', '23.109.225.166:5797', '104.222.185.119:5682', '23.109.232.103:6023',
       '23.109.208.147:6671', '154.92.125.119:5420', '23.109.225.124:5755', '104.238.8.37:5895', '104.238.8.164:6022',
       '104.222.185.244:5807', '154.92.124.77:5105', '104.238.8.109:5967', '104.238.9.57:6510', '154.92.124.85:5113',
       '109.207.130.5:8012', '154.92.125.97:5398', '104.222.185.209:5772', '23.109.219.56:6280', '23.109.208.28:6552',
       '154.92.124.159:5187', '104.238.9.108:6561', '23.109.208.27:6551', '23.109.219.90:6314', '104.222.187.113:6237',
       '23.109.225.117:5748', '23.109.208.75:6599', '104.238.8.24:5882', '23.109.208.38:6562', '109.207.130.171:8178',
       '109.207.130.32:8039', '23.109.219.39:6263', '104.238.8.7:5865', '104.222.187.17:6141', '154.92.124.202:5230',
       '104.222.187.100:6224', '109.207.130.89:8096', '104.222.185.237:5800', '104.238.8.44:5902', '23.109.219.97:6321',
       '23.109.225.147:5778', '104.222.185.172:5735', '104.238.8.110:5968', '104.222.187.18:6142',
       '23.109.232.101:6021', '23.109.225.182:5813', '154.92.125.195:5496', '23.109.232.232:6152',
       '104.222.187.114:6238', '104.222.185.4:5567', '23.109.219.164:6388', '104.222.187.119:6243',
       '104.238.9.110:6563', '23.109.208.46:6570', '154.92.125.206:5507', '154.92.125.102:5403', '23.109.225.4:5635',
       '104.222.187.48:6172', '109.207.130.176:8183', '154.92.124.96:5124', '104.238.8.81:5939', '23.109.225.140:5771',
       '104.238.9.166:6619']
'''
response = requests.get("http://worldtimeapi.org/api/ip")
data = response.json()
current_year = data['datetime'][:4]
current_month = data['datetime'][5:7]


if(current_year != "2024" or (current_month != "01")):
    print('License expired you may contact me to renew on discord, my user-name is _shahar')
    input("Press Enter to exit...")
    exit()
'''

login_url = "http://s1.izra.co.il/login"
# print('Hello there, this program is meant to attack users as they leave vacation in izra.co.il')
# print('For support, you can reach _shahar in discord')

high_priority_work_active = False
condition = threading.Condition()
print_lock = threading.Lock()

leader_email = 'something@gmail.com'  # input("enter your account's email: ")
leader_password = '123321'  # input("enter password: ")
login_data = {"email": leader_email, "password": leader_password, "rem": "on", "reg": "התחברות >>"}
spell_data = {"res_hour_mad": '12', "magic_res_defense": "הפעל את קסם מגן המשאבים"}


# spell_data = {"res_hour_mad": input('Resource shield hours after attacking:(1-23) '), "magic_res_defense": "הפעל את קסם מגן המשאבים"}


def sync_print(text):
    print_lock.acquire()
    print(text)
    print_lock.release()


# P for persistent
def getP(session, page):
    while True:
        try:
            response = session.get(page, timeout=1)
            if response.status_code == 200:
                break
            else:
                sync_print('invalid response')
                time.sleep(1)
        except:
            continue
    return response


def login(p=0):
    proxies = {
        'http': f"http://{p_user}:{p_pass}@{ips[p]}"
    }
    s = requests.Session()
    s.proxies = proxies
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    s.headers.update({'User-Agent': custom_user_agent})
    while True:
        try:
            response = s.post(login_url, data=login_data, timeout=1)
            break
        except:
            continue
    return s


def spell(s, data, url):
    check = False
    while True:
        try:
            response = s.post(url, data=data, timeout=1)
            if response.status_code == 200:
                break
            else:
                if not check:
                    check = True
                    sync_print('invalid response')
        except:
            sync_print('err')
            continue


def attack(s, data, url):
    while True:
        try:
            response = s.post(url, data=data, timeout=1)
            break
        except:
            sync_print('err')
            continue
    return response


def thread_op(attack_ids, threshold, proxy):
    global high_priority_work_active
    ses = login(proxy)
    ses.headers['Referer'] = 'http://s1.izra.co.il'
    sync_print(f'starting {proxy} with {len(attack_ids)} targets.. keep the program running')
    while len(attack_ids) > 0:
        with condition:
            while high_priority_work_active:
                condition.wait()
        for url in attack_ids:
            cur = time.time()
            use_spell = False
            keep_attack = True
            r = getP(ses, url)
            soup = BeautifulSoup(r.content, 'html.parser')
            string_exists = "השחקן בחופשה" in soup.get_text()
            if not string_exists:
                with condition:
                    high_priority_work_active = True
                    condition.notify_all()
                    while keep_attack:
                        try:
                            r = getP(ses, url)
                            soup = BeautifulSoup(r.content, 'html.parser')
                            csrf_token = soup.find('input', {'name': 'csrf_token'})
                            csrf_token_value = csrf_token['value']
                            attack_data = {'turns': '10', 'csrf_token': csrf_token_value, 'defender_id': f"{url[39:]}",
                                           'go': 'תקוף'}
                            r = attack(ses, attack_data, f'http://s1.izra.co.il/attack/attack/?attack_id={url[39:]}')
                            soup = BeautifulSoup(r.content, 'html.parser')
                            span_tag = soup.find('span', class_='row color-gold')
                            if (span_tag is None):
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
                            sync_print(f"{proxy} attacked {url[39:]}:collected {gold + iron + wood + food} resources")
                            if (gold + iron + wood + food) < threshold:
                                attack_ids.remove(url)
                                keep_attack = False
                            else:
                                use_spell = True
                        except Exception as e:
                            sync_print(f'{proxy} err {e} {url[39:]}')
                            keep_attack = False
                    if use_spell:
                        sync_print("spell")
                        spell(ses, spell_data, "http://s1.izra.co.il/hero/magicresdef/")
                        winsound.PlaySound('Windows Background.wav', winsound.SND_FILENAME | winsound.SND_NOWAIT)
                    high_priority_work_active = False
                    condition.notify_all()
            to_sleep = 0.6 - (time.time() - cur)
            if to_sleep > 0:
                time.sleep(to_sleep)
    sync_print(f"thread {proxy} finished")


s = login()
site = "http://s1.izra.co.il/vacationlist"
html = getP(s, site).content
soup = BeautifulSoup(html, 'html.parser')

# x = re.findall('title="אלפים"/></td>\n.*.\n.*attack_id=([0-9]*)">.*</a>.*\n.*\n.*[0-9][0-9],.*,.*</td>\n.*<td>.*איזרהלנד.*</td>', str(soup))
x = re.findall('<td>\d[0-9]+ </td>.*\n.*attack_id=([0-9]*)">.*</a>.*\n.*\n.*\n.*<td>.*איזרהלנד.*</td>', str(soup))
# x = re.findall('.*\n.*attack_id=([0-9]*)">.*</a>.*\n.*\n.*\n.*<td>.*דארקלנד.*</td>', str(soup))
print(f'{len(x)} targets')

# keep = True
# print("Below you may enter ID's to camp on, recommended no more than 4 for best performance")
# while keep:
#   em = input("Enter ID: ")
#  ids.append(em)
# keep = input("Do you want to enter another member? (enter 'y' if yes): ") == 'y'

proxy_index = 0
threshold = 2000000  # int(input("minimum amount of resources (gold + wood + iron + food) taken to keep attacking: (example: 100000 means, stop attacking if you get only 99999)"))
attack_links = [f"http://s1.izra.co.il/attack/?attack_id=" + iden for iden in x]
# thread_op(attack_links, threshold, proxy_index)

threads = []

while len(attack_links) > 0:
    count = ceil(len(attack_links) / (len(ips) - len(threads)))
    thread = threading.Thread(target=thread_op, args=(attack_links[:2], threshold, proxy_index))
    threads.append(thread)
    thread.start()
    attack_links = attack_links[2:]
    proxy_index = proxy_index + 1

for thread in threads:
    thread.join()
    sync_print("thread closed")

input("finished, press enter to close")
