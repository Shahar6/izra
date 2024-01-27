import requests
from bs4 import BeautifulSoup
import time
import re
import locale
import math
import openpyxl

def extract_ids_from_excel(file_path, sheet_name, start_cell, end_cell):
    ids = []
    # Load the workbook
    wb = openpyxl.load_workbook(file_path)
    # Select the active sheet
    sheet = wb[sheet_name]
    
    # Iterate through the specified range of cells
    for row in sheet[start_cell:end_cell]:
        for cell in row:
            # Assuming each cell contains a single ID
            ids.append(cell.value)
    
    return ids

def write_to_specific_cell(workbook, cell, data):
    # Get the active sheet
    ws = workbook.active
    
    # Write data to the specified cell
    ws[cell] = data


# Example usage
file_path = "resource_data.xlsx"
sheet_name = "Sheet"  # Change to your sheet name
start_cell = "G2"
end_cell = "G1693"
ids = extract_ids_from_excel(file_path, sheet_name, start_cell, end_cell)

spy_data = {'spy': 'שלח את המרגלים'}
login_url = "http://s1.izra.co.il/login"

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
login_data = {"email": 'shaharizra1@gmail.com', "password": '1234512345', "rem": "on", "reg": "התחברות >>"}


s = login()
try:
    wb = openpyxl.load_workbook(file_path)
except FileNotFoundError:
    wb = openpyxl.load_workbook(file_path)


for index, number in enumerate(ids):
    print(index)
    response = scout(s, f"http://s1.izra.co.il/spy/spyuser/?targetId={number}", spy_data)
    soup = BeautifulSoup(response.content, 'html.parser')
    span_tag = soup.find('span', class_='row color-gold')
    if 'חופשות שנוצלו' in soup.text:
        summ = 'vacation'
    elif 'war_no_rcity' in soup.text:
        summ = 'diff city'
    elif span_tag is not None:
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
        write_to_specific_cell(wb, f'C{index+2}', gold)
        write_to_specific_cell(wb, f'D{index+2}', iron)
        write_to_specific_cell(wb, f'E{index+2}', wood)
        write_to_specific_cell(wb, f'F{index+2}', food)
        write_to_specific_cell(wb, f'I{index+2}', slaves)
    write_to_specific_cell(wb, f'B{index+2}', summ)





wb.save(file_path)
 

