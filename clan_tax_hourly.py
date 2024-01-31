import requests
import re
from bs4 import BeautifulSoup
import time
import threading
from datetime import datetime

city_emails = ['liadyaadcheck@gmail.com', 'shaharizra1@gmail.com', 'liadebaywatch@gmail.com', 'elanam48@gmail.com',
               'lokjrami44@gmail.com', 'shaharizra2@gmail.com', 'toharbm1@gmail.com', 'dp1480171@gmail.com',
               'zmnywy@gmail.com', 'shahar3232@walla.com', 'shaharau@post.bgu.ac.il', 'shaharb4r@gmail.com',
               'yakirdavid111111@gmail.com', 'tevagreen1987@gmail.com',
               'lyshoees@gmail.com', 'adimarom4@gmail.com', 'liad@fix.co.il', 'dwrytrwznbrg97@gmail.com',
               'maplebgu@gmail.com']
city_ids = ['72101', '44260', '72137', '72100', '71875', '44261', '71843', '71849', '71894', '8690', '71806', '71792',
            '71882', '72113', '71833', '71909', '72114', '71908', '71807']

login_url = "http://s1.izra.co.il/login"
tax_url = "http://s1.izra.co.il/clan/paytaxes"

# print('enter leader data:')
# leader_data = {"email": input('Enter Email: '), "password": input('Enter Password: '), "rem": "on", "reg": "התחברות >>"}
# leader_id = input('enter leader id: ')

# leader_data = {"email": 'shaharizra1@gmail.com', "password": '1234512345', "rem": "on", "reg": "התחברות >>"}
# leader_id = '44260'
# clan_id = '26'

leader_data = {"email": 'vampire421@gmail.com', "password": '30121992', "rem": "on", "reg": "התחברות >>"}
leader_id = '14578'
# clan_id = '23'
last_spell = time.time()


def getP(session, page):
    while True:
        try:
            response = session.get(page, timeout=1)
            if response.status_code != 529:
                break
            else:
                time.sleep(1)
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


def login(login_data):
    s = requests.Session()
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    s.headers.update({'User-Agent': custom_user_agent})
    while True:
        try:
            response = s.post(login_url, data=login_data, timeout=1)
            if response.status_code != 529:
                break
            else:
                time.sleep(1)
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
                time.sleep(1)
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
                time.sleep(1)
        except:
            continue
    return response


def mass_join(clan_id):
    emails = ['shaharizra1@gmail.com', 'shahar3232@walla.com', 'liadebaywatch@gmail.com', 'elanam48@gmail.com',
              'lokjrami44@gmail.com', 'shaharizra2@gmail.com', 'toharbm1@gmail.com', 'dp1480171@gmail.com',
              'zmnywy@gmail.com', 'shaharau@post.bgu.ac.il', 'shaharb4r@gmail.com',
              'yakirdavid111111@gmail.com', 'tevagreen1987@gmail.com',
              'lyshoees@gmail.com', 'liadyaadcheck@gmail.com', 'adimarom4@gmail.com', 'liad@fix.co.il',
              'dwrytrwznbrg97@gmail.com', 'liadshahar1@gmail.com', 'liadshahar2@gmail.com', 'maplebgu@gmail.com']
    temp = 0
    for mail in emails:
        data = {"email": mail, "password": '1234512345' if mail != 'lyshoees@gmail.com' else '123321', "rem": "on",
                "reg": "התחברות >>"}
        ses, r = login(data)
        join_clan(ses, clan_id)
        temp = ses
    r = getP(temp, f'http://s1.izra.co.il/attack/?attack_id=33790')
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    csrf_token_value = csrf_token['value']
    attack_data = {'turns': '1', 'csrf_token': csrf_token_value, 'defender_id': "33790", 'go': 'תקוף'}
    temp.headers['Referer'] = 'http://s1.izra.co.il'
    attack(temp, attack_data)


def spell_clan(session):
    url = 'http://s1.izra.co.il/clan/activatemagic'
    data = {'magic': 'more_population_timeout'}
    postP(session, url, data)
    '''emails = ['shaharizra1@gmail.com', 'shahar3232@walla.com', 'liadebaywatch@gmail.com', 'elanam48@gmail.com',
              'lokjrami44@gmail.com', 'shaharizra2@gmail.com', 'toharbm1@gmail.com', 'dp1480171@gmail.com',
              'biuvit324@gmail.com', 'zmnywy@gmail.com', 'shaharau@post.bgu.ac.il', 'shaharb4r@gmail.com',
              'yakirdavid111111@gmail.com', 'tevagreen1987@gmail.com',
              'lyshoees@gmail.com', 'liadyaadcheck@gmail.com', 'adimarom4@gmail.com', 'liad@fix.co.il',
              'dwrytrwznbrg97@gmail.com', 'maplebgu@gmail.com']
    for mail in emails:
        data = {"email": mail, "password": '1234512345' if mail != 'lyshoees@gmail.com' else '123321', "rem": "on",
                "reg": "התחברות >>"}
        ses, r = login(data)
        join_clan(ses)

    # data = {"email": 'vampire421@gmail.com', "password": '30121992', "rem": "on", "reg": "התחברות >>"}
    # ses, r = login(data)


   for mail in emails:
        data = {"email": mail, "password": '1234512345', "rem": "on", "reg": "התחברות >>"}
        ses, r = login(data)
        exit_clan(ses)'''


def attack(s, data, url='http://s1.izra.co.il/attack/attack/?attack_id=33790'):
    while True:
        try:
            response = s.post(url, data=data, timeout=1)
            if response.status_code == 200:
                break
            else:
                time.sleep(1)
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
                time.sleep(1)
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
    if (last_spell + (3 * 60 * 60)) < time.time():
        spell_clan(lead_ses)  # cast spell
        url = 'http://s1.izra.co.il/clan/closeclan/'  # close clan
        leave_data = {'close_code': 'סגור', 'close:': 'סגור'}
        postP(lead_ses, url, leave_data)
        # create clan
        open_url = 'http://s1.izra.co.il/clanOpen/openclan/'
        open_data = {'clan_name': 'Faith + 1', 'open': 'צור שבט'}
        postP(lead_ses, open_url, open_data)
        getP(lead_ses, 'http://s1.izra.co.il/clan/change_clan_state/?state=open')
        postP(lead_ses, 'http://s1.izra.co.il/clan/updateleadertaxes/', {'mas': '25000'})
        clan_id = find_clan_id(lead_ses)
        # add members
        mass_join(clan_id)
        getP(lead_ses, 'http://s1.izra.co.il/clan/change_clan_state/?state=closed')
        last_spell = time.time()

    adds = 0
    for email, c_id in zip(city_emails, city_ids):
        member_data = {"email": email, "password": '1234512345' if email != 'lyshoees@gmail.com' else '123321',
                       "rem": "on", "reg": "התחברות >>"}
        member_id = c_id
        memb_ses, r = login(member_data)
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
        # exit_clan(memb_ses)  # member leaves
    print(f'{adds * 25000} collected in total')
    wait_next_action(last_spell)
