import requests
import re
from bs4 import BeautifulSoup
import time
from datetime import datetime


city_emails = ['shaharizra1@gmail.com', 'liadebaywatch@gmail.com', 'elanam48@gmail.com', 'lokjrami44@gmail.com', 'shaharizra2@gmail.com', 'toharbm1@gmail.com', 'dp1480171@gmail.com',
            'biuvit324@gmail.com', 'zmnywy@gmail.com', 'shahar3232@walla.com', 'shaharau@post.bgu.ac.il', 'shaharb4r@gmail.com', 'yakirdavid111111@gmail.com', 'tevagreen1987@gmail.com',
            'lyshoees@gmail.com', 'liadyaadcheck@gmail.com', 'adimarom4@gmail.com', 'liad@fix.co.il', 'dwrytrwznbrg97@gmail.com', 'maplebgu@gmail.com']
city_ids = ['44260', '72137', '72100', '71875', '44261', '71843', '71849', '71910', '71894', '8690', '71806', '71792', '71882', '72113', '71833', '72101', '71909', '72114', '71908', '71807']



login_url = "http://s1.izra.co.il/login"
tax_url = "http://s1.izra.co.il/clan/paytaxes"

# print('enter leader data:')
# leader_data = {"email": input('Enter Email: '), "password": input('Enter Password: '), "rem": "on", "reg": "התחברות >>"}
# leader_id = input('enter leader id: ')

#leader_data = {"email": 'shaharizra1@gmail.com', "password": '1234512345', "rem": "on", "reg": "התחברות >>"}
#leader_id = '44260'
#clan_id = '26'

leader_data = {"email": 'vampire421@gmail.com', "password": '30121991', "rem": "on", "reg": "התחברות >>"}
leader_id = '14578'
clan_id = '23'

def getP(session, page):
    while True:
        try:
            response = session.get(page, timeout = 1)
            if response.status_code != 529:
                break
            else:
                time.sleep(1)
        except:
            continue
    return response

def waitnextCollect():
    current_time = time.localtime()
    minute = current_time.tm_min
    print(f'sleeping for {(61-minute)%30} minutes')
    time.sleep(60*((61-minute)%30))

def login(login_data):
    s = requests.Session()
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    s.headers.update({'User-Agent': custom_user_agent})
    while True:
        try:
            response = s.post(login_url, data = login_data, timeout = 1)
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
            response = session.post(page, data = dataF, timeout = 1)
            if response.status_code != 529:
                break
            else:
                time.sleep(1)
        except:
            continue
    return response

def pay_tax(s):
    while True:
        try:
            response = s.post("http://s1.izra.co.il/clan/paytaxes/", data = {}, timeout = 1)
            if response.status_code != 529:
                break
            else:
                time.sleep(1)
        except:
            continue
    return response

def spellClan():
    emails = ['shaharizra1@gmail.com', 'shahar3232@walla.com', 'liadebaywatch@gmail.com', 'elanam48@gmail.com', 'lokjrami44@gmail.com', 'shaharizra2@gmail.com', 'toharbm1@gmail.com', 'dp1480171@gmail.com',
            'biuvit324@gmail.com', 'zmnywy@gmail.com', 'shaharau@post.bgu.ac.il', 'shaharb4r@gmail.com', 'yakirdavid111111@gmail.com', 'tevagreen1987@gmail.com',
            'lyshoees@gmail.com', 'liadyaadcheck@gmail.com', 'adimarom4@gmail.com', 'liad@fix.co.il', 'dwrytrwznbrg97@gmail.com', 'maplebgu@gmail.com']
    for email in emails:
        data = {"email": email, "password": '1234512345' if email != 'lyshoees@gmail.com' else '123321', "rem": "on", "reg": "התחברות >>"}
        ses, r = login(data)
        join_clan(ses)

    data = {"email": 'vampire421@gmail.com', "password": '30121991', "rem": "on", "reg": "התחברות >>"}
    ses, r = login(data)
    url = 'http://s1.izra.co.il/clan/activatemagic'
    data = {'magic': 'more_population_timeout'}
    postP(ses, url, data)

    for email in emails:
        data = {"email": email, "password": '1234512345', "rem": "on", "reg": "התחברות >>"}
        ses, r = login(data)
        exitClan(ses)

def exitClan(s):
    while True:
        try:
            response = s.post("http://s1.izra.co.il/clan/getout", data = {'exit_code': 'יציאה', 'send': 'המשך' }, timeout = 1)
            if response.status_code != 529:
                break
            else:
                time.sleep(1)
        except:
            continue
    return response


cast_today = True
hour_to_cast = 14
while True:
    lead_ses, r = login(leader_data)
    
    if cast_today == True and int(datetime.now().strftime('%H')) < hour_to_cast:
        cast_today = False

    if cast_today == False and int(datetime.now().strftime('%H')) == hour_to_cast:
        spellClan()
        print('casted spell')
        cast_today = True
        
    waitnextCollect()        
    for email, c_id in zip(city_emails, city_ids): 
        member_data = {"email": email, "password": '1234512345' if email != 'lyshoees@gmail.com' else '123321', "rem": "on", "reg": "התחברות >>"}
        member_id = c_id
        memb_ses, r = login(member_data)
        res = getP(memb_ses, 'http://s1.izra.co.il/training')
        soup = BeautifulSoup(res.content, 'html.parser')
        count = int(re.findall('\nאוכלוסיה לא מאומנת: <span style="color: #444">2500 / </span>([0-9,]+) \|\n', str(soup))[0].replace(',',''))
        train_data = {"soldiers": '0', "slaves": f'{count}', "spy": '0', "sentry": '0', "horsemen": '0', "train": 'אמן את האוכלוסיה'}
        postP(memb_ses, 'http://s1.izra.co.il/training/train/', train_data)
        res = getP(memb_ses, 'http://s1.izra.co.il/work')
        soup = BeautifulSoup(res.content, 'html.parser')
        count = int(re.findall('<span class="row">עבדים חופשיים</span>\n<span class="row">([0-9,]+)</span>', str(soup))[0].replace(',',''))
        slave_data = {"gold": f'{count}', "food": '0', "iron": '0', "wood": '0', 'slavessend': 'שלח את העבדים'}
        postP(memb_ses, 'http://s1.izra.co.il/work/manageslaves/', slave_data)
        soup = BeautifulSoup(r.content, 'html.parser')
        x = int(re.findall('<span class="row color-gold">([0-9,]*)</span>', str(soup))[0].replace(',',''))
        count = x // 25000
        print(f'paying {count} times ({count * 25000} gold in total)')
        getP(memb_ses, f'http://s1.izra.co.il/clanslist/enterclan/?join_clanid={clan_id}') # member join clan
        while count > 0:
            pay_tax(memb_ses)
            getP(lead_ses, f"http://s1.izra.co.il/clan/setclanpos/?pos=1&uid={member_id}") # make member new head of clan
            exitClan(lead_ses) # leader exit clan
            getP(lead_ses, f'http://s1.izra.co.il/clanslist/enterclan/?join_clanid={clan_id}') # leader join clan
            getP(memb_ses, f"http://s1.izra.co.il/clan/setclanpos/?pos=1&uid={leader_id}") # make leader new head of clan
            exitClan(memb_ses) # member leaves
            getP(memb_ses, f'http://s1.izra.co.il/clanslist/enterclan/?join_clanid={clan_id}') # member join clan
            count = count - 1
        exitClan(memb_ses) # member leaves
    
    

