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
    train_data = {"soldiers": '0', "slaves": f'{count-1}', "spy": '0', "sentry": '0', "horsemen": '0', "train": 'אמן את האוכלוסיה'}
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
    slave_data = {"gold": f'{count//4}', "food": f'{count//4}', "iron": f'{count//4}', "wood": f'{count//4}', 'slavessend': 'שלח את העבדים'}
    #slave_data = {"gold": f'{count}', "food": '0', "iron": '0', "wood": '0', 'slavessend': 'שלח את העבדים'}
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
    emails = ['shaharizra1@gmail.com', 'shahar3232@walla.com', 'liadebaywatch@gmail.com', 'elanam48@gmail.com', 'lokjrami44@gmail.com', 'shaharizra2@gmail.com', 'toharbm1@gmail.com', 'dp1480171@gmail.com',
            'biuvit324@gmail.com', 'zmnywy@gmail.com', 'shaharau@post.bgu.ac.il', 'shaharb4r@gmail.com', 'yakirdavid111111@gmail.com', 'tevagreen1987@gmail.com',
            'lyshoees@gmail.com', 'liadyaadcheck@gmail.com', 'adimarom4@gmail.com', 'liad@fix.co.il', 'dwrytrwznbrg97@gmail.com', 'maplebgu@gmail.com']
    for email in emails:
        data = {"email": email, "password": '1234512345' if email != 'lyshoees@gmail.com' else '123321', "rem": "on", "reg": "התחברות >>"}
        ses, r = login(data)
        join_clan(ses)

    data = {"email": 'vampire421@gmail.com', "password": '30121992', "rem": "on", "reg": "התחברות >>"}
    ses, r = login(data)
    url = 'http://s1.izra.co.il/clan/activatemagic'
    data = {'magic': 'more_population_timeout'}
    postP(ses, url, data)

    for email in emails:
        data = {"email": email, "password": '1234512345' if email != 'lyshoees@gmail.com' else '123321', "rem": "on", "reg": "התחברות >>"}
        ses, r = login(data)
        exitClan(ses)
    



emails = [ 'liadebaywatch@gmail.com', 'shaharizra1@gmail.com', 'shahar3232@walla.com', 'elanam48@gmail.com', 'lokjrami44@gmail.com', 'shaharizra2@gmail.com', 'toharbm1@gmail.com',
          'dp1480171@gmail.com', 'biuvit324@gmail.com', 'zmnywy@gmail.com', 'shaharb4r@gmail.com', 'shaharau@post.bgu.ac.il',
          'yakirdavid111111@gmail.com','tevagreen1987@gmail.com', 'liadyaadcheck@gmail.com', 'adimarom4@gmail.com', 'liad@fix.co.il','dwrytrwznbrg97@gmail.com', 'maplebgu@gmail.com']

email0 = ['wasifgf8@gmail.com','jgfdwryu@gmail.com','aslamjg45677@gmail.com','tnseer181@gmail.com','adiljg47788@gmail.com','asid7625@gmail.com','arifjg33556@gmail.com','oumarjg35789@gmail.com','asifjg34678@gmail.com','zahoorjg3467@gmail.com','zuhebjg4558@gmail.com','rmzan128@gmail.com','rohanjg825@gmail.com','adnanjg21@gmail.com','asifjg45688@gmail.com','saberjg78@gmail.com','saqibgf6@gmail.com','khgdserty@gmail.com','shafeeqghg5@gmail.com','jameelgf6@gmail.com','saleemgf568@gmail.com','kaleemgf298@gmail.com','hasangf08@gmail.com','afangf31@gmail.com','asfindgffd0@gmail.com','raheemgf7@gmail.com','rahoolhg4@gmail.com','rahitgf886@gmail.com','khadimgf1@gmail.com','bukhatgf002@gmail.com','asifgf845@gmail.com','asadgf688@gmail.com','aslamgf469@gmail.com','outewsghj845@gmail.com','najeebgf15@gmail.com','fhdtu9618@gmail.com','hstcdhgh5@gmail.com','jdtdnn1@gmail.com','jsehgh@gmail.com','hhdyhh936@gmail.com','fjfygghg17@gmail.com','offthyu730@gmail.com','degkb71@gmail.com','bddonn873@gmail.com','hyye961@gmail.com','fdrkit146@gmail.com','heeouf@gmail.com','urscjgd@gmail.com','jifcvdr@gmail.com','jufcjcr@gmail.com','nhskiey@gmail.com','gyefb157@gmail.com','mvvkoh@gmail.com','oigvjgji@gmail.com','uisndh1@gmail.com','itgjvv2@gmail.com','jugjvh5@gmail.com','knnhgv7@gmail.com','jggok07@gmail.com','jbdvjis@gmail.com','ndgnsk7@gmail.com','kokn74353@gmail.com','jghjbg92@gmail.com','jgvbikh@gmail.com','innjgyv@gmail.com','iggikk26@gmail.com','knbokk42@gmail.com','kiie01796@gmail.com','jhhd2193@gmail.com','mnbiih98@gmail.com','jffvujvhyfjc@gmail.com','cerhyu023@gmail.com','sgchh3372@gmail.com','ewfggh72@gmail.com','jsjdhbdjjd64@gmail.com','fjjcktf@gmail.com','hshgeheh1@gmail.com','hiifjj00@gmail.com','yehdhhdyehdhh@gmail.com','ghfghjj139@gmail.com','hjjsergh@gmail.com','hjjchnb@gmail.com','bjkbjj989@gmail.com','highh7067@gmail.com','kerghjk60@gmail.com','nbcggj8@gmail.com','khjjhik3@gmail.com','hejsjsjjs9@gmail.com','vehdsetgs@gmail.com','bkvgcjj@gmail.com','ghsegff05@gmail.com','hsjjsowhs@gmail.com','gtygh1653@gmail.com','thffgh49@gmail.com','dgswe18@gmail.com','fjdegg81@gmail.com','yhigiuh6@gmail.com','ufyffuv@gmail.com','sefghh33@gmail.com','seffgh544@gmail.com','ngvhctt@gmail.com','xvbffgh2@gmail.com','xeggbjj8@gmail.com','hehgehh159@gmail.com','cstghei@gmail.com','ddrggvgg@gmail.com','cvvxsev@gmail.com','deghgjj@gmail.com','gjmhj27@gmail.com','fynfhe@gmail.com','jiubdgh@gmail.com','iejjueg@gmail.com','ksksbb560@gmail.com','nsosnb0@gmail.com','bjzjsb875@gmail.com','bxisbsn@gmail.com','b88442542@gmail.com','njxjb4385@gmail.com','bskjs145@gmail.com','vzjsb54@gmail.com']
email1 = ['bhdxxc649@gmail.com','xndiv8684@gmail.com','nsksbb559@gmail.com','ksosbb873@gmail.com','nsisbb0@gmail.com','fgshsj107@gmail.com','jjcxxd8@gmail.com','b85706117@gmail.com','ajiab8503@gmail.com','nzksb095@gmail.com','b05901776@gmail.com','ndkdbb7@gmail.com','lsjsb74@gmail.com','ossbb86@gmail.com','j69965716@gmail.com','nsksb840@gmail.com','bjdjsb617@gmail.com','vanaj3817@gmail.com','jdidbb022@gmail.com','j40019827@gmail.com','jsisvv624@gmail.com','ksosb232@gmail.com','v3314418@gmail.com','bxjsjb3@gmail.com','j33732171@gmail.com','jbxcc738@gmail.com','kaobb62@gmail.com','alirazakhan0523@gmail.com','nomanazam6929@gmail.com','tabishumar887@gmail.com','naveedazan7292@gmail.com','inyarsalam70@gmail.com','basitn059@gmail.com','azmatomer453@gmail.com','asifhameed6395@gmail.com','alijunaid0913@gmail.com','alijabbar0347@gmail.com','alizamin0913@gmail.com','azmat6526463@gmail.com','erroryt8573634@gmail.com']
email2 = ['asad757465@gmail.com','rashid75747465@gmail.com','atahrali670@gmail.com','gitangli75757565@gmail.com','azharghaffar711@gmail.com','khanazamatullah68@gmail.com','nasem85736363@gmail.com','daan75646353@gmail.com','erica7267565@gmail.com','zaman75646@gmail.com','ayatullahali800@gmail.com','waqr85746364@gmail.com','error85645465@gmail.com','anushka885736343@gmail.com']

emails = email0 + email1 + email2

login_url = "http://s1.izra.co.il/login"


#spell clan:

while True:
    #spellClan()
    #exit()
    #waitnextCollect()
    print('waking up')
    for email in emails:
        data = {"email": email, "password": '1234512345' if email != 'lyshoees@gmail.com' else '123321', "rem": "on", "reg": "התחברות >>"}
        ses, r = login(data)
        #exitClan(ses)
        # expand population
        expand_population(ses)
        # train workers
        train_population(ses)
        # take back workers
        return_slaves(ses)
        # send workers to gather
        send_slaves(ses)
        # expand gatherings
        expand_resource(ses, 'gold')
        expand_resource(ses, 'food')
        expand_resource(ses, 'wood')
        expand_resource(ses, 'iron')
    exit()
    
