import requests
from bs4 import BeautifulSoup
import time
import re


spy_data = {'spy': 'שלח את המרגלים'}
login_url = "http://s1.izra.co.il/login"
#login_data = {"email": input('Enter email: '), "password": input('Enter password: '), "rem": "on", "reg": "התחברות >>"}
login_data = {"email": 'liadyaadcheck@gmail.com', "password": '1234512345', "rem": "on", "reg": "התחברות >>"}


turns = 2000 #int(input('Enter turns to use: '))
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

        
thread_scan(int(input('First Page: ')), int(input('Last Page: ')))

    
print('\n')
duration = time.time() - start_time
print(f"turns used: {start_turns - turns}")
print("\nProgram execution time:", duration, "seconds")
input("\nPress Enter to exit...")

