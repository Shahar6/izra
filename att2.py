import requests
from bs4 import BeautifulSoup
import time
import re


spy_data = {'spy': 'שלח את המרגלים'}
login_url = "http://s1.izra.co.il/login"
#login_data = {"email": input('Enter email: '), "password": input('Enter password: '), "rem": "on", "reg": "התחברות >>"}
login_data = {"email": 'liadyaadcheck@gmail.com', "password": '1234512345', "rem": "on", "reg": "התחברות >>"}

ids = ['11862'
,'63079'
,'64945
'
,'62562
'
,'62353
'
,'63090
'
,'62583
'
,'62382
'
,'62580
'
,'63091
'
,'62575
'
,'63109
'
,'62951
'
,'63462
'
,'71672
'
,'62960
'
,'61288
'
,'61282
'
,'62381
'
,'63442
'
,'62354
'
,'64914
'
,'62959
'
,'62331
'
,'62581
'
,'63095
'
,'63104
'
,'63439
'
,'64086
'
,'63092
'
,'64441
'
,'63719
'
,'64976
'
,'63974
'
,'63100
'
,'63768
'
,'63110
'
,'64969
'
,'62328
'
,'63013
'
,'64901
'
,'64877
'
,'63267
'
,'63271
'
,'63012
'
,'62950
'
,'62378
'
,'63099
'
,'63265
'
,'65075
'
,'63282
'
,'63467
'
,'62567
'
,'63066
'
,'62554
'
,'65113
'
,'64878
'
,'62588
'
,'64961
'
,'64896
'
,'64895
'
,'62337
'
,'62357
'
,'62385
'
,'64882
'
,'63105
'
,'64874
'
,'62949
'
,'71911
'
,'62514
'
,'64206
'
,'63433
'
,'63129
'
,'71963
'
,'62326
'
,'62582
'
,'63094
'
,'64998
'
,'63692
'
,'62501
'
,'64146
'
,'64968
'
,'63122
'
,'63085
'
,'63502
'
,'63106
'
,'63121
'
,'64871
'
,'63080
'
,'62308
'
,'63252
'
,'62330
'
,'63076
'
,'63253
'
,'64909
'
,'62318
'
,'62312
'
,'64323
'
,'62574
'
,'64782
'
,'64867
'
,'64115
'
,'63281
'
,'63022
'
,'63078
'
,'63071
'
,'63436
'
,'62570
'
,'62531
'
,'63299
'
,'63247
'
,'65119
'
,'62503
'
,'64883
'
,'63435
'
,'63272
'
,'61286
'
,'62506
'
,'62310
'
,'61289
'
,'65086
'
,'63293
'
,'64875
'
,'62569
'
,'63084
'
,'62572
'
,'63010
'
,'64204
'
,'65123
'
,'62566
'
,'65074
'
,'62952
'
,'64870
'
,'62512
'
,'65059
'
,'65008
'
,'65116
'
,'63081
'
,'64015
'
,'64535
'
,'63249
'
,'63269
'
,'64910
'
,'64873
'
,'63083
'
,'63077
'
,'62565
'
,'63082
'
,'63418
'
,'63476
'
,'63052
'
,'63431
'
,'63434
'
,'64884
'
,'62537
'
,'62522
'
,'62992
'
,'64390
'
,'63423
'
,'63428
'
,'63426
'
,'62511
'
,'63954
'
,'64362
'
,'61274
'
,'63503
'
,'62336
'
,'64848
'
,'64661
'
,'65117
'
,'64967
'
,'64088
'
,'64306
'
,'64820
'
,'63273
'
,'62961
'
,'62510
'
,'64885
'
,'64903
'
,'62550
'
,'64958
'
,'62515
'
,'63063
'
,'63062
'
,'62525
'
,'64600
'
,'64972
'
,'65096
'
,'65057
'
,'61292
'
,'65058
'
,'63264
'
,'63266
'
,'63008
'
,'65063
'
,'62497
'
,'62500
'
,'62496
'
,'63691
'
,'63014
'
,'63285
'
,'64104
'
,'64360
'
,'63250
'
,'65050
'
,'63020
'
,'63009
'
,'64016
'
,'62350
'
,'65041
'
,'63913
'
,'63128
'
,'62533
'
,'63132
'
,'63270
'
,'63315
'
,'61287
'
,'62400
'
,'63948
'
,'63308
'
,'63424
'
,'62551
'
,'63061
'
,'63319
'
,'61279
'
,'62556
'
,'62549
'
,'63064
'
,'63068
'
,'62332
'
,'63427
'
,'65012
'
,'64868
'
,'62559
'
,'65105
'
,'62557
'
,'63069
'
,'63065
'
,'64083
'
,'62334
'
,'62994
'
,'63420
'
,'63292
'
,'64277
'
,'65071
'
,'64897
'
,'62315
'
,'64176
'
,'64324
'
,'62552
'
,'64962
'
,'64970
'
,'64959
'
,'63103']
turns = 2400 #int(input('Enter turns to use: '))
start_turns = turns
start_time = time.time()


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
    global login_data
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


def attack(s, data, url):
    while True:
        try:
            response = s.post(url, data = data, timeout = 1)
            if response.status_code == 200:
                break
            else:
                time.sleep(1)
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
                turns = turns - 10
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
                print(f"attacked {start}")
                turns = turns - 10
                counter = counter + 1        

id_scan(ids)       
#thread_scan(int(input('First Page: ')), int(input('Last Page: ')))

    
print('\n')
duration = time.time() - start_time
print(f"turns used: {start_turns - turns}")
print("\nProgram execution time:", duration, "seconds")
input("\nPress Enter to exit...")

