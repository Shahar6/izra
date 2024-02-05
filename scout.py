import requests
from bs4 import BeautifulSoup
import time
import re
import locale
import xlsxwriter
import math

workbook = xlsxwriter.Workbook('resource_data1.xlsx')
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
email = input('Enter email: ')
password = input('Enter password: ')
login_data = {"email": email, "password": password, "rem": "on", "reg": "התחברות >>"}

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
    time.sleep(0.5)
    return response

def login():
    s = requests.Session()
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    s.headers.update({'User-Agent': custom_user_agent})
    while True:
        try:
            response = s.post(login_url, data = login_data, timeout = 1)
            if response.status_code == 200:
                break
            else:
                time.sleep(1)
        except:
            continue
        time.sleep(0.5)
    return s

def scout(session, url, spy_data):
    while True:
        try:
            response = session.post(url, data = spy_data, timeout = 1)
            if response.status_code == 200:
                break
            else:
                time.sleep(1)
        except:
            continue
        time.sleep(0.5)
    return response

def format_with_commas(number):
    locale.setlocale(locale.LC_ALL, '')
    return locale.format_string("%d", number, grouping=True)

def thread_scan(start, finish):
    global row
    s = login()
    while(start <= finish):
        try:
            print(finish)
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
                    if summ > 500000 or slaves + farmers > 3000:
                        worksheet.write(row, 0, text_content)
                        worksheet.write(row, 1, summ)
                        worksheet.write(row, 2, gold)
                        worksheet.write(row, 3, iron)
                        worksheet.write(row, 4, wood)
                        worksheet.write(row, 5, food)
                        worksheet.write(row, 6, number)
                        worksheet.write(row, 7, finish)
                        worksheet.write(row, 8, slaves + farmers)
                        row = row + 1
                        print(f'name: {text_content} gold: {gold}, iron: {iron}, wood: {wood}, food: {food}')

                else:
                    print(f'page: {finish} name: {text_content} scout unsuccessful')
            finish = finish - 1
        except KeyboardInterrupt:
            print('Interrupted')
            input('continue?')


thread_scan(int(input('start page: ')), int(input('end page: ')))
duration = time.time() - start_time
workbook.close()
print("\nProgram execution time:", duration, "seconds")



