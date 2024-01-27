import requests
import re
from bs4 import BeautifulSoup
import time


def waitnextCollect():
    current_time = time.localtime()
    minute = current_time.tm_min
    print(f'sleeping for {(61-minute)%30} minutes')
    time.sleep(60*((61-minute)%30))

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

def train_population(ses):
    res = getP(ses, 'http://s1.izra.co.il/training')
    soup = BeautifulSoup(res.content, 'html.parser')
    count = int(re.findall('\nאוכלוסיה לא מאומנת: <span style="color: #444">2500 / </span>([0-9,]+) \|\n', str(soup))[0].replace(',',''))
    train_data = {"soldiers": '0', "slaves": f'{count}', "spy": '0', "sentry": '0', "horsemen": '0', "train": 'אמן את האוכלוסיה'}
    postP(ses, 'http://s1.izra.co.il/training/train/', train_data)

def expand_population(ses):
    addr = 'http://s1.izra.co.il/develop'
    data = {"dev_population": 'פתח'}
    keep = True
    while keep:
        res = postP(ses, addr, data)
        soup = BeautifulSoup(res.content, 'html.parser')
        if 'אין לך מספיק משאבים' in soup.text:
            keep = False

def send_slaves(ses):
    res = getP(ses, 'http://s1.izra.co.il/work')
    soup = BeautifulSoup(res.content, 'html.parser')
    count = int(re.findall('<span class="row">עבדים חופשיים</span>\n<span class="row">([0-9,]+)</span>', str(soup))[0].replace(',',''))
    #slave_data = {"gold": f'{count//4}', "food": f'{count//4}', "iron": f'{count//4}', "wood": f'{count//4}', 'slavessend': 'שלח את העבדים'}
    slave_data = {"gold": f'{count}', "food": '0', "iron": '0', "wood": '0', 'slavessend': 'שלח את העבדים'}
    postP(ses, 'http://s1.izra.co.il/work/manageslaves/', slave_data)

def return_slaves(ses):
    res = getP(ses, 'http://s1.izra.co.il/work')
    soup = BeautifulSoup(res.content, 'html.parser')
    gold = int(re.findall('<td>מכרה זהב</td>\n<td>([0-9,]+)</td>', str(soup))[0].replace(',',''))
    food = int(re.findall('<td>איכרים</td>\n<td>([0-9,]+)</td>', str(soup))[0].replace(',',''))
    iron = int(re.findall('<td>מכרה מתכת</td>\n<td>([0-9,]+)</td>', str(soup))[0].replace(',',''))
    wood = int(re.findall('<td>חוטבי עצים</td>\n<td>([0-9,]+)</td>', str(soup))[0].replace(',',''))
    slave_data = {"gold": f'{gold}', "food": f'{food}', "iron": f'{iron}', "wood": f'{wood}', 'slavesout': 'החזר את העבדים'}
    postP(ses, 'http://s1.izra.co.il/work/manageslaves/', slave_data)

def expand_resource(ses, resource):
    # possible resources: gold, food, wood, iron
    addr = 'http://s1.izra.co.il/develop'
    data = {f"dev_{resource}": 'פתח'}
    keep = True
    while keep:
        res = postP(ses, addr, data)
        soup = BeautifulSoup(res.content, 'html.parser')
        if 'אין לך מספיק משאבים' in soup.text:
            keep = False

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
            
def join_clan(ses):
    getP(ses, f'http://s1.izra.co.il/clanslist/enterclan/?join_clanid=23')

def exitClan(ses):
    while True:
        try:
            response = ses.post("http://s1.izra.co.il/clan/getout", data = {'exit_code': 'יציאה', 'send': 'המשך' }, timeout = 1)
            if response.status_code != 529:
                break
            else:
                time.sleep(1)
        except:
            continue
    return response



def spellClan():
    # 'shaharizra1@gmail.com', 'shahar3232@walla.com',
    emails = ['liadebaywatch@gmail.com', 'elanam48@gmail.com', 'lokjrami44@gmail.com', 'shaharizra2@gmail.com', 'toharbm1@gmail.com', 'dp1480171@gmail.com',
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
    



emails = [ 'liadebaywatch@gmail.com', 'shaharizra1@gmail.com', 'shahar3232@walla.com', 'elanam48@gmail.com', 'lokjrami44@gmail.com', 'shaharizra2@gmail.com', 'toharbm1@gmail.com',
          'dp1480171@gmail.com', 'biuvit324@gmail.com', 'zmnywy@gmail.com', 'shaharb4r@gmail.com', 'shaharau@post.bgu.ac.il',
          'yakirdavid111111@gmail.com','tevagreen1987@gmail.com', 'liadyaadcheck@gmail.com', 'adimarom4@gmail.com', 'liad@fix.co.il','dwrytrwznbrg97@gmail.com', 'maplebgu@gmail.com']

login_url = "http://s1.izra.co.il/login"


#spell clan:

while True:
    #spellClan()
    #exit()
    #waitnextCollect()
    print('waking up')
    for email in emails:
        data = {"email": email, "password": "password": '1234512345' if email != 'lyshoees@gmail.com' else '123321', "rem": "on", "reg": "התחברות >>"}
        ses, r = login(data)
        #exitClan(ses)
        # expand population
        # expand_population(ses)
        # train workers
        train_population(ses)
        # take back workers
        return_slaves(ses)
        # send workers to gather
        send_slaves(ses)
        # expand gatherings
        #expand_resource(ses, 'gold')
        #expand_resource(ses, 'food')
        #expand_resource(ses, 'wood')
        #expand_resource(ses, 'iron')
    exit()
    
