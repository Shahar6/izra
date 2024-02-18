import requests
from bs4 import BeautifulSoup
import time
import re
import threading
import random

turn_lock = threading.Lock()
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

response = requests.get("http://worldtimeapi.org/api/ip")
data = response.json()
current_year = data['datetime'][:4]
current_month = data['datetime'][5:7]

    

if(current_year != "2024" or (current_month != "02")):
    print('License expired you may contact me to renew on discord, my user-name is _shahar')
    input("Press Enter to exit...")
    exit()

spy_data = {'spy': 'שלח את המרגלים'}
login_url = "http://s1.izra.co.il/login"
#login_data = {"email": input('Enter email: '), "password": input('Enter password: '), "rem": "on", "reg": "התחברות >>"}
login_data = {"email": 'zmnywy@gmail.com', "password": '1234512345', "rem": "on", "reg": "התחברות >>"}
ids=[]
turns = 4580 # int(input('Enter turns to use: '))
start_turns = turns
start_time = time.time()

def dec_turn():
    turn_lock.acquire()
    turns = turns - 10
    turn_lock.release()


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

def switch_proxy(ses):
    global p_pass
    global p_user
    global ips
    # sync_print('switching proxy')
    proxies = {
                'http': f"http://{p_user}:{p_pass}@{ips[random.randint(0, len(ips)-1)]}"
        }
    ses.proxies = proxies

def login():
    global p_pass
    global p_user
    global ips
    s = requests.Session()
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    s.headers.update({'User-Agent': custom_user_agent})
    proxies = {
                'http': f"http://{p_user}:{p_pass}@{ips[random.randint(0, len(ips)-1)]}"
        }
    s.proxies = proxies
    while True:
        try:
            response = s.post(login_url, data = login_data, timeout = 1)
            if response.status_code == 200:
                break
            else:
                switch_proxy(s)
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
                switch_proxy(s)
        except:
            continue


def thread_scan(start, finish):
    minimum = int(input('minimum gold to attack: '))
    maximum = int(input('maximum gold to attack: '))
    o_start = start
    global turns
    s = login()
    counter = 0
    s.headers['Referer'] = 'http://s1.izra.co.il'
    while turns >= 10 and start <= finish:
        print(start)
        page = f"http://s1.izra.co.il/attack/?p={start}"
        r = getP(s, page)
        soup = BeautifulSoup(r.content, 'html.parser')
        #print(str(soup))
        x = re.findall('אלפים.*\n.*\n.*attack_id=([0-9]*)">.*\n.*\n.*\n.*\n.*"color-gold">([0-9,]*)', str(soup))
        a_links = []
        for j in x:
            value = int(j[1].replace(',',''))
            if(value > minimum and value < maximum):
                a_links.append(j[0])
        for number in a_links:
            r = getP(s, f'http://s1.izra.co.il/attack/?attack_id={number}')
            soup = BeautifulSoup(r.content, 'html.parser')
            csrf_token = soup.find('input', {'name': 'csrf_token'})
            csrf_token_value = csrf_token['value']
            attack_data = {'turns': '10', 'csrf_token': csrf_token_value ,'defender_id': f"{number}" , 'go': 'תקוף'}
            if turns >= 10:
                attack(s, attack_data, f'http://s1.izra.co.il/attack/attack/?attack_id={number}')
                print(f"attacked {start}")
                dec_turn()
                counter = counter + 1
        start = start +1
        if(start > finish):
            print(f'attacked {counter} times this cycle with minimum {minimum}')
            start = o_start
            minimum = minimum - 15000
            counter = 0

            

def id_scan(id_list):
    global turns
    s = login()
    counter = 0
    s.headers['Referer'] = 'http://s1.izra.co.il'
    while turns >= 10:
        for number in id_list:
            r = getP(s, f'http://s1.izra.co.il/attack/?attack_id={number}')
            soup = BeautifulSoup(r.content, 'html.parser')
            csrf_token = soup.find('input', {'name': 'csrf_token'})
            csrf_token_value = csrf_token['value']
            attack_data = {'turns': '10', 'csrf_token': csrf_token_value ,'defender_id': f"{number}" , 'go': 'תקוף'}
            if turns >= 10:
                attack(s, attack_data, f'http://s1.izra.co.il/attack/attack/?attack_id={number}')
                print(f"attacked {number}")
                turns = turns - 10
                counter = counter + 1        

#id_scan(ids)
ids=['72391','72175','72176','16410','72179','72174','62386','72178','72171','72170','72173','72177','72341','65085','64989','64047','64418','64141','71911','64401','11862','63918','63709','64206','64463','65073','64196','64176','64476','64108','63888','64195','63919','64169','72172','64452','64459','64199','64193','63979','64728','64431','62395','64733','64909','64436','63937','64213','63711','64187','64969','64191','64186','63939','63885','64157','64230','64143','64127','64136','64109','64372','64220','63940','63967','63923','64362','64686','64146','63694','63977','63867','63947','64086','63925','64212','63978','63959','63932','63728','63948','63702','64369','63964','63707','63905','63953','64441','64399','64602','63861','64204','64650','63688','63700','62362','64234','63858','64475','63720','64114','63854','64124','63718','63685','63889','64632','63955','63681','64442','63853','64184','64134','64451','64380','63968','64240','64201','64233','64203','64669','63719','63941','64433','64092','62334','64090','63683','64394','64406','62338','64194','63938','63690','63706','64495','64175','64145','64118','64465','63729','64179','63879','64425','64384','64473','64411','64117','64375','64214','64162','64461','64159','64471','64998','64446','64218','63697','63903','64116','64140','64396','64383','64697','64119','64208','64631','64360','63974','64417','64487','64110','64350','63985','64445','64474','63942','64373','64466','64751','64189','64374','64378','63911','64489','64479','61274','64231','63893','64103','64429','64185','64153','64402','64450','63886','64354','62307','64224','64161','63907','63883','63981','64112','63695','64750','64651','64155','63914','64171','64153','64098','63902','64415','64456','63904','64370','63726','63993','64106','63882','63891','64486','64457','64430','64147','64101','64093','64419','63986','64170','64349','65098','63874','63887','64412','64413','64685','64359','64409','64496','64405','64407','64414','64498','64646','64236','64483','64160','64494','64167','64462','64933','64974','64924','64221','62312','64128','64403','64150','64389','63698','64976','64426','64477','64467','64352','64488','61309','64986','64992','61283','64959','64661','64865','64408','64945','64644','64152','64395','64688','63989','64952','64502','64397','64871','64693','64947','62350','64961','64444','64682','64379','61912','64957','64943','62399','62392','64712','64391','64913','64991','64863','61913','64970','62390','64954','65114','64387','64252','64965','64197','64897','64968','64246','64361','64990','64923','64704','61286','64948','61285','64971','64428','64980','64432','64972','64248','62314','64249','61924','64365','64878','64469','64158','64657','64404','65122','62370','62310','64901','64874','64966','64599','65117','62309','64423','64596','64449','62394','64951','64982','64899','64245','64630','64366','64113','64222','64392','64910','64680','64720','64478','64347','63739','64454','64382','64752','64239','64700','64443','64634','64385','64198','64364','64133','64438','64149','64660','64925','64903','64497','64082','65120','65115','64400','64470','63732','64398','64453','64447','64869','64683','64939','64390','65006','64911','64915','64393','64713','64200','64703','64416','64944','64458','64850','64072','64884','65005','64937','62340','64647','61900','64087','64089','64601','62349','64343','64342','62317','64600','62322','64508','64882','64088','64876','62316','64900','65121','62361','63991']
#thread_scan(int(input('First Page: ')), int(input('Last Page: ')))
threads_count = 30
threads = []
start = 0
iter_len = len(ids)//threads_count
divider = iter_len

for i in range(threads_count):
    thread = threading.Thread(target=id_scan, args=(ids[start:iter_len],))
    threads.append(thread)
    thread.start()
    start = start + divider + 1
    iter_len = iter_len + divider + 1
    if i == (threads_count - 2):
        iter_len = len(ids) - 1
   
for thread in threads:
    thread.join()
    print("thread closed")
    
print('\n')
duration = time.time() - start_time
print(f"turns used: {start_turns - turns}")
print("\nProgram execution time:", duration, "seconds")
input("\nPress Enter to exit...")

