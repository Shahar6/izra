import requests
import re
from bs4 import BeautifulSoup
import time
import threading
from datetime import datetime
import random


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


tax_emails = ['shaharizra1@gmail.com', 'liadebaywatch@gmail.com','elanam48@gmail.com','lokjrami44@gmail.com', 'shaharizra2@gmail.com',
               'toharbm1@gmail.com', 'dp1480171@gmail.com', 'biuvit324@gmail.com', 'zmnywy@gmail.com',
               'shahar3232@walla.com', 'shaharau@post.bgu.ac.il', 'shaharb4r@gmail.com', 'yakirdavid111111@gmail.com',
               'tevagreen1987@gmail.com', 'lyshoees@gmail.com', 'liadyaadcheck@gmail.com', 'adimarom4@gmail.com',
               'liad@fix.co.il', 'dwrytrwznbrg97@gmail.com', 'maplebgu@gmail.com']


clan_emails = ['liadshahar3@gmail.com', 'liadshahar4@gmail.com', 'liadshahar5@gmail.com', 'itay50@gmail.com',
               'liadshahar6@gmail.com', 'oceanecom1@gmail.com', '2016.rayman@gmail.com', 'giladd.99@gmail.com',
               'gujdianastewart@gmail.com', 'hsbebdhbs@gmail.com','wasifgf8@gmail.com','jgfdwryu@gmail.com']


login_url = "http://s1.izra.co.il/login"
tax_url = "http://s1.izra.co.il/clan/paytaxes"


def switch_proxy(ses):
    global p_pass
    global p_user
    global ips
    print('switching proxy')
    proxies = {
                'http': f"http://{p_user}:{p_pass}@{ips[random.randint(0, len(ips)-1)]}"
        }
    ses.proxies = proxies
    
# print('enter leader data:')
# leader_data = {"email": input('Enter Email: '), "password": input('Enter Password: '), "rem": "on", "reg": "התחברות >>"}
# leader_id = input('enter leader id: ')

# leader_data = {"email": 'shaharizra1@gmail.com', "password": '1234512345', "rem": "on", "reg": "התחברות >>"}
# leader_id = '44260'
# clan_id = '26'

leader_data = {"email": 'vampire421@gmail.com', "password": '30121992', "rem": "on", "reg": "התחברות >>"}
# clan_id = '23'
last_spell = time.time() - (3*60*60)


# P for persistent
def getP(session, page):
    while True:
        try:
            response = session.get(page, timeout=1)
            if response.status_code == 200:
                break
            else:
                switch_proxy(session)
        except:
            continue
    return response


def wait_next_action(spell_time):  # waiting for either new spell or update
    current_time = time.localtime()
    minute = current_time.tm_min
    mins_until_spell = ((spell_time + (3 * 60 * 60)) - time.time()) / 60
    wake = min((61 - minute) % 30, mins_until_spell)
    wake = max(1, wake)
    print(f'sleeping for {wake} minutes')
    time.sleep(60 * wake)


def login(data):
    proxies = {
        'http': f"http://{p_user}:{p_pass}@{ips[random.randint(0, len(ips)-1)]}"
    }
    s = requests.Session()
    s.proxies = proxies
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    s.headers.update({'User-Agent': custom_user_agent})
    while True:
        try:
            response = s.post(login_url, data=data, timeout=1)
            if response.status_code != 200:
                switch_proxy(s)
            else:
                break
        except:
            continue
    return s, response


def postP(session, page, dataF):
    while True:
        try:
            response = session.post(page, data=dataF, timeout=1)
            if response.status_code != 529:
                break
            else:
                switch_proxy(s)
        except:
            continue
    return response


def join_clan(ses, clanId):
    getP(ses, f'http://s1.izra.co.il/clanslist/enterclan/?join_clanid={clanId}')


def pay_tax(s):
    while True:
        try:
            response = s.post("http://s1.izra.co.il/clan/paytaxes/", data={}, timeout=1)
            if response.status_code != 529:
                break
            else:
                switch_proxy(s)
        except:
            continue
    return response


def mass_join(clan_id):
    global clan_emails
    global tax_emails
    emails = clan_emails + tax_emails
    temp = 0
    for mail in emails:
        data = {"email": mail, "password": '1234512345' if mail != 'lyshoees@gmail.com' else '123321', "rem": "on",
                "reg": "התחברות >>"}
        ses, r = login(data)
        join_clan(ses, clan_id)
        temp = ses
    temp.headers['Referer'] = 'http://s1.izra.co.il'
    r = getP(temp, f'http://s1.izra.co.il/attack/?attack_id=33790')
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    csrf_token_value = csrf_token['value']
    attack_data = {'turns': '1', 'csrf_token': csrf_token_value, 'defender_id': "33790", 'go': 'תקוף'}
    attack(temp, attack_data)
    r = getP(temp, f'http://s1.izra.co.il/attack/?attack_id=33790')
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    csrf_token_value = csrf_token['value']
    attack_data = {'turns': '1', 'csrf_token': csrf_token_value, 'defender_id': "33790", 'go': 'תקוף'}
    attack(temp, attack_data)
    
def mass_exit():
    global clan_emails
    global tax_emails
    emails = clan_emails + tax_emails
    temp = 0
    for mail in emails:
        data = {"email": mail, "password": '1234512345' if mail != 'lyshoees@gmail.com' else '123321', "rem": "on",
                "reg": "התחברות >>"}
        ses, r = login(data)
        exit_clan(ses)


def spell_clan(session):
    url = 'http://s1.izra.co.il/clan/activatemagic'
    data = {'magic': 'more_population_timeout'}
    postP(session, url, data)


def attack(s, data, url='http://s1.izra.co.il/attack/attack/?attack_id=33790'):
    while True:
        try:
            response = s.post(url, data=data, timeout=1)
            if response.status_code == 200:
                break
            else:
                switch_proxy(s)
        except:
            continue


def exit_clan(s):
    while True:
        try:
            response = s.post("http://s1.izra.co.il/clan/getout", data={'exit_code': 'יציאה', 'send': 'המשך'},
                              timeout=1)
            if response.status_code != 529:
                break
            else:
                switch_proxy(s)
        except:
            continue
    return response


def find_clan_id(session, sleep=60):
    time.sleep(sleep)
    res = getP(lead_ses, 'http://s1.izra.co.il/attack/?p=1')
    soup = BeautifulSoup(res.content, 'html.parser')
    cl_id = int(re.findall('<td>.*\n.*באטרס.*</td>.*\n.*clan_id=([0-9,]+)', str(soup))[0])
    return cl_id


while True:
    print('wake up')
    lead_ses, r = login(leader_data)
    clan_id = find_clan_id(lead_ses, 0)
    soup = BeautifulSoup(r.content, 'html.parser')
    leader_id = re.findall('friend=([0-9,]+)', str(soup))[0]
    if (last_spell + (3 * 60 * 60)) < time.time():
        spell_clan(lead_ses)  # cast spell
        url = 'http://s1.izra.co.il/clan/closeclan/'  # close clan
        leave_data = {'close_code': 'סגור', 'close:': 'סגור'}
        postP(lead_ses, url, leave_data)
        # create clan
        open_url = 'http://s1.izra.co.il/clanOpen/openclan/'
        open_data = {'clan_name': 'DikinBaus', 'open': 'צור שבט'}
        postP(lead_ses, open_url, open_data)
        getP(lead_ses, 'http://s1.izra.co.il/clan/change_clan_state/?state=open')
        postP(lead_ses, 'http://s1.izra.co.il/clan/updateleadertaxes/', {'mas': '25000'})
        clan_id = find_clan_id(lead_ses)
        # add members
        mass_join(clan_id)
        getP(lead_ses, 'http://s1.izra.co.il/clan/change_clan_state/?state=closed')
        last_spell = time.time()

    adds = 0
    getP(lead_ses, 'http://s1.izra.co.il/clan/change_clan_state/?state=open')
    for email in tax_emails:
        member_data = {"email": email, "password": '1234512345' if email != 'lyshoees@gmail.com' else '123321',
                       "rem": "on", "reg": "התחברות >>"}
        memb_ses, r = login(member_data)
        soup = BeautifulSoup(r.content, 'html.parser')
        if 'חופשות שנוצלו' in soup.text:
            continue
        member_id = re.findall('friend=([0-9,]+)', str(soup))[0]
        res = getP(memb_ses, 'http://s1.izra.co.il/training')
        soup = BeautifulSoup(res.content, 'html.parser')
        count = int(
            re.findall('\nאוכלוסיה לא מאומנת: <span style="color: #444">2500 / </span>([0-9,]+) \|\n', str(soup))[
                0].replace(',', ''))
        train_data = {"soldiers": '0', "slaves": f'{count}', "spy": '0', "sentry": '0', "horsemen": '0',
                      "train": 'אמן את האוכלוסיה'}
        postP(memb_ses, 'http://s1.izra.co.il/training/train/', train_data)
        res = getP(memb_ses, 'http://s1.izra.co.il/work')
        soup = BeautifulSoup(res.content, 'html.parser')
        count = int(re.findall('<span class="row">עבדים חופשיים</span>\n<span class="row">([0-9,]+)</span>', str(soup))[
                        0].replace(',', ''))
        slave_data = {"gold": f'{count}', "food": '0', "iron": '0', "wood": '0', 'slavessend': 'שלח את העבדים'}
        postP(memb_ses, 'http://s1.izra.co.il/work/manageslaves/', slave_data)
        soup = BeautifulSoup(r.content, 'html.parser')
        x = int(re.findall('<span class="row color-gold">([0-9,]*)</span>', str(soup))[0].replace(',', ''))
        count = x // 25000
        #count = min(count, 20)
        adds = adds + count
        join_clan(memb_ses, clan_id)  # member join clan
        while count > 0:
            pay_tax(memb_ses)
            getP(lead_ses,
                 f"http://s1.izra.co.il/clan/setclanpos/?pos=1&uid={member_id}")  # make member new head of clan
            exit_clan(lead_ses)  # leader exit clan
            join_clan(lead_ses, clan_id)  # leader join clan
            getP(memb_ses,
                 f"http://s1.izra.co.il/clan/setclanpos/?pos=1&uid={leader_id}")  # make leader new head of clan
            exit_clan(memb_ses)  # member leaves
            join_clan(memb_ses, clan_id)  # member join clan
            count = count - 1
            #print('paid')
        # exit_clan(memb_ses)  # member leaves
    getP(lead_ses, 'http://s1.izra.co.il/clan/change_clan_state/?state=closed')
    print(f'{adds * 25000} collected in total')
    wait_next_action(last_spell)
