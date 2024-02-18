import requests
from bs4 import BeautifulSoup
import time
import re
import locale
import xlsxwriter
import math
import threading
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

workbook = xlsxwriter.Workbook('resource_data_new.xlsx')
worksheet = workbook.add_worksheet()
row = 0
worksheet.write(row, 0, 'Name')
worksheet.write(row, 1, 'Sum')
worksheet.write(row, 2, 'Gold')
worksheet.write(row, 3, 'Iron')
worksheet.write(row, 4, 'Wood')
worksheet.write(row, 5, 'Food')
worksheet.write(row, 6, 'ID')
worksheet.write(row, 7, 'Page')
worksheet.write(row, 8, 'Slaves')
row = row + 1

start_time = time.time()
path = 'resource_data.xlsx'
spy_data = {'spy': 'שלח את המרגלים'}
login_url = "http://s1.izra.co.il/login"
email = 'shaharizra1@gmail.com'#input('Enter email: ')
password = '1234512345'#input('Enter password: ')
login_data = {"email": email, "password": password, "rem": "on", "reg": "התחברות >>"}
print_lock = threading.Lock()
write_lock = threading.Lock()

def sync_print(text):
    print_lock.acquire()
    print(text)
    print_lock.release()


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

def scout(session, url, spy_data):
    while True:
        try:
            response = session.post(url, data = spy_data, timeout = 1)
            if response.status_code == 200:
                break
            else:
                switch_proxy(session)
        except:
            continue
    return response

def write_book(name, summ, gold, iron, wood, food, number, page, workers):
    global row
    global worksheet
    global write_lock
    write_lock.acquire()
    worksheet.write(row, 0, name)
    worksheet.write(row, 1, summ)
    worksheet.write(row, 2, gold)
    worksheet.write(row, 3, iron)
    worksheet.write(row, 4, wood)
    worksheet.write(row, 5, food)
    worksheet.write(row, 6, number)
    worksheet.write(row, 7, page)
    worksheet.write(row, 8, workers)
    row = row + 1
    write_lock.release()
    

def format_with_commas(number):
    locale.setlocale(locale.LC_ALL, '')
    return locale.format_string("%d", number, grouping=True)

def thread_scan(start, finish):
    global row
    s = login()
    while(start <= finish):
        try:
            sync_print(finish)
            # gather all user links:
            page = f"http://s1.izra.co.il/attack/?p={finish}"
            r = getP(s, page)
            soup = BeautifulSoup(r.content, 'html.parser')
            tags = soup.find_all('a', href=lambda href: href.startswith('/attack/?attack_id='))
            results = []
            for tag in tags:
                href_value = tag['href']
                number = href_value.split('=')[-1]
                text_content = tag.get_text()
                results.append((number, text_content))
            # iterate over all links and scout them
            for number, text_content in results:
                response = scout(s, f"http://s1.izra.co.il/spy/spyuser/?targetId={number}", spy_data)
                soup = BeautifulSoup(response.content, 'html.parser')
                span_tag = soup.find('span', class_='row color-gold')
                if span_tag is not None:
                    gold = int(span_tag.get_text().replace(',', ''))
                    span_tag = soup.find('span', class_='row color-iron')
                    iron = int(span_tag.get_text().replace(',', ''))
                    span_tag = soup.find('span', class_='row color-wood')
                    wood = int(span_tag.get_text().replace(',', ''))
                    span_tag = soup.find('span', class_='row color-food')
                    food = int(span_tag.get_text().replace(',', ''))
                    slaves = int(re.findall('<span class="row">עבדים</span>\n<span class="row color-food">([0-9,]*)</span>', str(soup))[0].replace(',',''))
                    farmers = int(re.findall('<span class="row">איכרים</span>\n<span class="row color-food">([0-9,]*)</span>', str(soup))[0].replace(',',''))
                    summ = food + gold + iron + wood
                    if summ > 5000000 or slaves + farmers > 10000:
                        write_book(text_content, summ, gold, iron, wood, food, number, finish, slaves + farmers)
                        #sync_print(f'name: {text_content} gold: {gold}, iron: {iron}, wood: {wood}, food: {food}')

                else:
                    sync_print(f'page: {finish} name: {text_content} scout unsuccessful')
            finish = finish - 1
        except KeyboardInterrupt:
            sync_print('Interrupted')
            input('continue?')
start = 14
end = 768
threads_count = 20
divider = (end - start) // threads_count

threads = []
iter_len = start + divider

for i in range(threads_count):
    thread = threading.Thread(target=thread_scan, args=(start, iter_len))
    threads.append(thread)
    thread.start()
    sync_print(f'{start}::{iter_len}')
    start = start + divider + 1
    iter_len = iter_len + divider + 1
    if i == (threads_count - 2):
        iter_len = end
   
for thread in threads:
    thread.join()
    sync_print("thread closed")
    
workbook.close()
duration = time.time() - start_time
print("\nProgram execution time:", duration, "seconds")



