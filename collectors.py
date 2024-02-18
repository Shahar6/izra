import requests
from bs4 import BeautifulSoup
import time
import re
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


response = requests.get("http://worldtimeapi.org/api/ip")
data = response.json()
current_year = data['datetime'][:4]
current_month = data['datetime'][5:7]
    

if(current_year != "2024" or (int(current_month) > 5)):
    print('License expired you may contact me to renew on discord, my user-name is _shahar')
    input("Press Enter to exit...")
    exit()


start_time = time.time()


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
    proxies = {
                'http': f"http://{p_user}:{p_pass}@{ips[random.randint(0, len(ips)-1)]}"
        }
    ses.proxies = proxies

def login(email, password):
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
    login_url = "http://s1.izra.co.il/login"
    login_data = {"email": email, "password": password, "rem": "on", "reg": "התחברות >>"}
    while True:
        try:
            response = s.post(login_url, data = login_data, timeout = 1)
            if response.status_code == 200:
                break
            else:
                switch_proxy(s)
        except:
            continue
    return s, response


def attack(s, u_id, times):
    if times <= 0:
        return
    s.headers['Referer'] = 'http://s1.izra.co.il'
    r = getP(s, f'http://s1.izra.co.il/attack/?attack_id={u_id}')
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    csrf_token_value = csrf_token['value']
    attack_data = {'turns': '10', 'csrf_token': csrf_token_value ,'defender_id': f"{u_id}" , 'go': 'תקוף'}
    url = f'http://s1.izra.co.il/attack/attack/?attack_id={u_id}'
    while True:
        try:
            response = s.post(url, data = data, timeout = 1)
            if response.status_code == 200:
                break
            else:
                switch_proxy(s)
        except:
            continue
    attack(s, u_id, times - 1)
    

def id_scan(s, id_list, times):
    for i in id_list:
        attack(s, i, times)


email0 = ['bhdxxc649@gmail.com','aslamjg45677@gmail.com','tnseer181@gmail.com','adiljg47788@gmail.com','asid7625@gmail.com','arifjg33556@gmail.com','oumarjg35789@gmail.com','asifjg34678@gmail.com','zahoorjg3467@gmail.com','zuhebjg4558@gmail.com','rmzan128@gmail.com','rohanjg825@gmail.com','adnanjg21@gmail.com','asifjg45688@gmail.com','saberjg78@gmail.com','saqibgf6@gmail.com','khgdserty@gmail.com','shafeeqghg5@gmail.com','jameelgf6@gmail.com','saleemgf568@gmail.com','kaleemgf298@gmail.com','hasangf08@gmail.com','afangf31@gmail.com','asfindgffd0@gmail.com','raheemgf7@gmail.com','rahoolhg4@gmail.com','rahitgf886@gmail.com','khadimgf1@gmail.com','bukhatgf002@gmail.com','asifgf845@gmail.com','asadgf688@gmail.com','aslamgf469@gmail.com','outewsghj845@gmail.com','najeebgf15@gmail.com','fhdtu9618@gmail.com','hstcdhgh5@gmail.com','jdtdnn1@gmail.com','jsehgh@gmail.com','hhdyhh936@gmail.com','fjfygghg17@gmail.com','offthyu730@gmail.com','degkb71@gmail.com','bddonn873@gmail.com','hyye961@gmail.com','fdrkit146@gmail.com','heeouf@gmail.com','urscjgd@gmail.com','jifcvdr@gmail.com','jufcjcr@gmail.com','nhskiey@gmail.com','gyefb157@gmail.com','mvvkoh@gmail.com','oigvjgji@gmail.com','uisndh1@gmail.com','itgjvv2@gmail.com','jugjvh5@gmail.com','knnhgv7@gmail.com','jggok07@gmail.com','jbdvjis@gmail.com','ndgnsk7@gmail.com','kokn74353@gmail.com','jghjbg92@gmail.com','jgvbikh@gmail.com','innjgyv@gmail.com','iggikk26@gmail.com','knbokk42@gmail.com','kiie01796@gmail.com','jhhd2193@gmail.com','mnbiih98@gmail.com','jffvujvhyfjc@gmail.com','cerhyu023@gmail.com','sgchh3372@gmail.com','ewfggh72@gmail.com','jsjdhbdjjd64@gmail.com','fjjcktf@gmail.com','hshgeheh1@gmail.com','hiifjj00@gmail.com','yehdhhdyehdhh@gmail.com','ghfghjj139@gmail.com','hjjsergh@gmail.com','hjjchnb@gmail.com','bjkbjj989@gmail.com','highh7067@gmail.com','kerghjk60@gmail.com','nbcggj8@gmail.com','khjjhik3@gmail.com','hejsjsjjs9@gmail.com','vehdsetgs@gmail.com','bkvgcjj@gmail.com','ghsegff05@gmail.com','hsjjsowhs@gmail.com','gtygh1653@gmail.com','thffgh49@gmail.com','dgswe18@gmail.com','fjdegg81@gmail.com','yhigiuh6@gmail.com','ufyffuv@gmail.com','sefghh33@gmail.com','seffgh544@gmail.com','ngvhctt@gmail.com','xvbffgh2@gmail.com','xeggbjj8@gmail.com','hehgehh159@gmail.com','cstghei@gmail.com','ddrggvgg@gmail.com','cvvxsev@gmail.com','deghgjj@gmail.com','gjmhj27@gmail.com','fynfhe@gmail.com','jiubdgh@gmail.com','iejjueg@gmail.com','ksksbb560@gmail.com','nsosnb0@gmail.com','bjzjsb875@gmail.com','bxisbsn@gmail.com','b88442542@gmail.com','njxjb4385@gmail.com','bskjs145@gmail.com','vzjsb54@gmail.com']
email1 = ['asad757465@gmail.com','rashid75747465@gmail.com','nsksbb559@gmail.com','ksosbb873@gmail.com','nsisbb0@gmail.com','fgshsj107@gmail.com','jjcxxd8@gmail.com','b85706117@gmail.com','ajiab8503@gmail.com','nzksb095@gmail.com','b05901776@gmail.com','ndkdbb7@gmail.com','lsjsb74@gmail.com','ossbb86@gmail.com','j69965716@gmail.com','nsksb840@gmail.com','bjdjsb617@gmail.com','vanaj3817@gmail.com','jdidbb022@gmail.com','j40019827@gmail.com','jsisvv624@gmail.com','ksosb232@gmail.com','v3314418@gmail.com','bxjsjb3@gmail.com','j33732171@gmail.com','jbxcc738@gmail.com','kaobb62@gmail.com','alirazakhan0523@gmail.com','nomanazam6929@gmail.com','tabishumar887@gmail.com','naveedazan7292@gmail.com','inyarsalam70@gmail.com','basitn059@gmail.com','azmatomer453@gmail.com','asifhameed6395@gmail.com','alijunaid0913@gmail.com','alijabbar0347@gmail.com','alizamin0913@gmail.com','azmat6526463@gmail.com','erroryt8573634@gmail.com']
email2 = ['atahrali670@gmail.com','gitangli75757565@gmail.com','azharghaffar711@gmail.com','khanazamatullah68@gmail.com','nasem85736363@gmail.com','daan75646353@gmail.com','erica7267565@gmail.com','zaman75646@gmail.com','ayatullahali800@gmail.com','waqr85746364@gmail.com','error85645465@gmail.com','anushka885736343@gmail.com']
email3 = []
email4 = []
email5 = []
email6 = []
input('test')

ids0 = ['16410','72174','72171', '72172','72170','72175','72173','72178','71911','71635','71991','72341','72081','71913','11862','72177','63420','62388','71687','63425','63417','63432','63429','63475','64676','64958','63423','63431','63136','63433','63692','64950','63922','62400','64967','64928','62368','63426','63430','63428','63434','63436','63921','64938','62378','64953','62971','71545','71646','71686','63427','62963','71649','62943','63438','63913','62965','63446','63682','62954','63686','63435','63691','63929','71648','63451','63445','63454','63985','64181','64931','63452','63920','63693','63934','63935','63912','63689','63449','63914','63930','62373','62950','64186','63681','62967','63925','63904','63938','64171','63698','62393','63472','64177','63684','63703','64182','63932','64187','63694','63464','63700','64215','63690','64184','64247','63980','63936','63696','63457','63456','64164','65008','63230','63979','63919','63711','63706','64214','63688','63905','64179','63460','64253','63683','63697','64189','62952','63918','63916','64230','64193','62970','64225','63975','63734','62949','64975','63961','63732','63444','63710','63964','64234','62953','62956','63937','63973','62969','64191','63685','64220','64194','63942','72176','63981','63907','64205','63990','64169','63699','63949','63991','63713','63484','63453','64202','63917','64172','64183','64213','63926','63707','63924','64201','63955','63718','63968','63722','63911','64173','63729','63727','64170','64985','64979','64708','63726','63740','63476','63989','65000','63421','64252','63970','63705','63455','63947','64254','63941','63909','64174','63269','63743','63742','63443','63952','63447','62512','63474','63946','63983','63418','62975','63931','64211','63915','64190','63695','64180','63424','65019','62959','63954','63725','63480','63940','63135','63462','63468','62367','62973','65011','63442','63465','63470','63477','62966','62961','63971','64984','64977','63471','62964','62968','63768','63467','63439','62946','62510','63687','63009','62962','63243','63277','63296','62947','63001','62501','63478','68559','63717','63963','68059','62527','64988','63268','62505','63264','63010','63993','62945','63469','63287','62490','68054','62503','63258','63506','63466','62518','62984','63487','61911','62960','63440','66509','62519','62957','62948','63481','63995','64207','63290','63122','63099','63242','63715','65030','63498','62944','63080','63458','63489','62494','63733','63256','63000','63499','63992','63441','63967','63096','64045','62531','63240','63259','63736','62496','63088','63302','62951','63236','63902','63005','63231','63994','63003','63966','61315','63119','63061','62530','63315','62551','63107','64085','63071','63859','63306','63988','63977','63901','64031','63232','63895','63313','68569','63875','64228','62539','62532','62525','64086','64044','63739','63127','64306','64108','63716','63953','68048','64117','63495','62972','64281','62567','63070','64217','63114','64052','64235','62526','63089','63314','63266','62553','63888','62550','64094','63051','64226','63307','64061','63129','63959','64092','63309','62582','63702','62507','64151','64101','63092','64222','63903','63986','63490','64212','63957','63741','66268','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','64418','63058','64036','64142','66267','63855','67793','64024','64072','64013','68561','64256','64026','63978','63856','64064','63100','64065','63735','64069','62982','63128','63130','64133','63708','63972','63485','63874','63887','64090','64130','64124','63889','63885','63757','63701','64032','64114','63879','64057','64118','64227','63491','63014','63262','64027','64099','64025','63488','65502','62515','63503','64147','64071','62570','63720','63263','64050','65470','64047','64139','63753','64060','64132','68287','63271','64127','63893','63858','64143','64077','64059','64073','63976','64039','62542','62549','64053','63897','64054','64042','62533','62540','63012','63997','64148','63308','63273','63007','63076','63756','64003','64051','64141','64010','64008','64276','64288','62326','62343','62566','64017','64096','62558','63502','62559','63312','63105','63013','63055','63311','63021','64062','63319','63744','63249','62537','63006','62545','63085','63737','64023','63116','64890','61289','65110','62318','63497','64149','63882','64892','64883','63267','64098','63018','62495','63270','62581','62492','62580','63260','62352','64012','63082','62554','64030','63022','62561','63008','63496','63075','63019','63091','63251','63060','63758','62331','62552','62548','64068','62994','61264','65071','63110','66270','63883','63057','64063','62576','63891','63265','62328','63252','64875','64019','64079','63272','64290','64401','63017','64782','62988','64043','62330','65057','65113','64083','63759','64258','63770','63133','63020','63282','64055','63755','62544','63134','64870','62562','64056','62346','63132','64001','64914','64896','64912','62339','63257','65058','64028','63746','65118','62583','63862','63063','63084','63077','63751','62321','62989','64895','63279','65081','63124','62992','64877','63754','63494','64022','62572','62508','64268','65092','65112','63104','63750','64058','65038','62354','64034','63052','64261','63745','64048','63761','63749','61260','64310','63053','62514','65105','63235','64041','63250','63065','65089','65067','62497','64918','62586','62357','62575','64000','62569','64820','63093','62563','62500','62511','61282','65091','63102','65034','61287','62522','64067','62506','62588','65046','65086','64075','64014','63111','62985','61268','63280','63062','64040','65119','63121','63285','64021','62997','62366','64921','63244','62308','62509','63083','65123','62513','62991','65075','63078','63295','63297','63056','64005','62978','62574','63233','63101','62557','63299','63069','63064','62528','63137','63255','71672','62541','65099','63291','63118','63095','63103','63246','72416','62363','62565','63293','63298','63123','63087','62516','63292','65065','63109','64035','64006','63241','62986','64049','63066','62987','62521','62979','61321','64015','69085','62998','63288','65079','62355','65048','63286','63281','63090','63054','63247','62981','62993','63068','63304','64115','63239','62556','63305','64016','62337','63500','63253','63289','63079','64277','62493','53160','64218','63939','63923','64145','64196','64157','63709','63969','63719','64162','65024','63974','64081','63081','64206','63928','62517','67939','64297','63876','68821','64362','64399','63881','64074','63237','63878','64472','63869','68451','64463','64176','63884','64391','64136','64146','63854','64089','64138','64159','64436','63999','64078','63851','64441','63852','64584','63898','64154','64097','64417','63896','64246','63730','64844','64324','63867','64156','63864','67938','63861','63871','64066','63863','64650','64144','64137','68707','64029','63998','64082','63853','64368','64106','64243','63886','64103','63870','64018','63873','64009','64080','64430','64352','64474','63728','64087','64231','63948']
ids1 = []
ids2 = []
ids3 = []
ids4 = []
ids5 = []
ids6 = []
ids7 = []

passw = '1234512345'

threads = []
for email in email0:
    s, r = login(email, passw)
    soup = BeautifulSoup(r.content, 'html.parser')
    c_id = re.findall('friend=([0-9,]+)', str(soup))[0]
    ids1.append(c_id)
    thread = threading.Thread(target=id_scan, args=(s,ids0[:7],2))
    threads.append(thread)
    ids0 = ids0[7:]

for thread in threads:
    thread.start()
    
for thread in threads:
    thread.join()

print('first lap ended')



threads = []
for email in email1:
    s, r = login(email, passw)
    soup = BeautifulSoup(r.content, 'html.parser')
    c_id = re.findall('friend=([0-9,]+)', str(soup))[0]
    ids2.append(c_id)
    thread = threading.Thread(target=id_scan, args=(s,ids1[:3], 5))
    threads.append(thread)
    ids1 = ids1[3:]

for thread in threads:
    thread.start()
    
for thread in threads:
    thread.join()

print('second lap ended')

threads = []
for email in email2:
    s, r = login(email, passw)
    soup = BeautifulSoup(r.content, 'html.parser')
    c_id = re.findall('friend=([0-9,]+)', str(soup))[0]
    ids3.append(c_id)
    thread = threading.Thread(target=id_scan, args=(s,ids2[:3], 5))
    threads.append(thread)
    ids2 = ids2[3:]

for thread in threads:
    thread.start()
    
for thread in threads:
    thread.join()

print('third lap ended')


threads = []
for email in email3:
    s, r = login(email, passw)
    soup = BeautifulSoup(r.content, 'html.parser')
    c_id = re.findall('friend=([0-9,]+)', str(soup))[0]
    ids4.append(c_id)
    thread = threading.Thread(target=id_scan, args=(s,ids3[:2], 8))
    threads.append(thread)
    ids3 = ids3[2:]

for thread in threads:
    thread.start()
    
for thread in threads:
    thread.join()

print('fourth lap ended')

threads = []
for email in email4:
    s, r = login(email, passw)
    soup = BeautifulSoup(r.content, 'html.parser')
    c_id = re.findall('friend=([0-9,]+)', str(soup))[0]
    ids5.append(c_id)
    thread = threading.Thread(target=id_scan, args=(s,ids4[:2], 8))
    threads.append(thread)
    ids4 = ids4[2:]

for thread in threads:
    thread.start()
    
for thread in threads:
    thread.join()

print('fifth lap ended')


threads = []
for email in email5:
    s, r = login(email, passw)
    soup = BeautifulSoup(r.content, 'html.parser')
    c_id = re.findall('friend=([0-9,]+)', str(soup))[0]
    ids6.append(c_id)
    thread = threading.Thread(target=id_scan, args=(s,ids5[:2], 8))
    threads.append(thread)
    ids5 = ids5[2:]

for thread in threads:
    thread.start()
    
for thread in threads:
    thread.join()

print('sixth lap ended')

threads = []
for email in email6:
    s, r = login(email, passw)
    soup = BeautifulSoup(r.content, 'html.parser')
    c_id = re.findall('friend=([0-9,]+)', str(soup))[0]
    ids7.append(c_id)
    thread = threading.Thread(target=id_scan, args=(s,ids6[:2], 8))
    threads.append(thread)
    ids6 = ids6[2:]

for thread in threads:
    thread.start()
    
for thread in threads:
    thread.join()


print('seventh lap ended')

s, r = login('vampire421@gmail.com', '30121992')
id_scan(s, ids7[:1], 13)
 

print('eighth lap (last one) ended')
    
print('\n')
duration = time.time() - start_time
print("\nProgram execution time:", duration, "seconds")
input("\nPress Enter to exit...")

