from bs4 import BeautifulSoup
import requests
import httplib2

#Cities names and main url on olx.pl
warsaw = ['https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/warszawa/?page=', 'Warsaw']
wroclaw = ['https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/wroclaw/?page=', 'Wroclaw']
gdynia = ['https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/gdynia/?page=', 'Gdynia']
gdansk = ['https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/gdansk/?page=', 'Gdansk']
cracow = ['https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/krakow/?page=', 'Cracow']
szczecin = ['https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/szczecin/?page=', 'Szczecin']
poznan = ['https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/poznan/?page=', 'Poznan']
zielona_gora = ['https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/zielonagora/?page=', 'Zielona Gora']

#Array of data
cities = [warsaw, wroclaw, gdynia, gdansk, cracow, szczecin, poznan, zielona_gora]

#Dictionary for scrapped data
records_olx = {'d':[]}
records_oto = {'d':[]}

def scrap_olx_for_urls(URL, name):
    c = requests.get(URL)
    soup_content = BeautifulSoup(c.content, 'html.parser')

    #Get all urls from page and scrap for each url
    for i1 in soup_content.find_all('div', {'class':'css-19ucd76'}):
        for i2 in i1.find_all('a',  {'class':'css-1bbgabe'}):
            if i2['href'][0] == 'h':
                print("STARTING: OTODOM")
                scrap_otodom(i2['href'], name)
            if i2['href'][0] == '/':
                print("STARTING: OLX")
                scrap_olx('https://www.olx.pl'+i2['href'], name)

#Olx scrapper
def scrap_olx(URL, name):
    c = requests.get(URL)
    soup_content = BeautifulSoup(c.content, 'html.parser')
    row=[]
    row.append(name)
    print(name)
    for i6 in soup_content.find_all('div', {'class':'css-dcwlyx'}):
        price = i6.find('h3').get_text()
        row.append(price)
    for i1 in soup_content.find_all('ul', {'class':'css-sfcl1s'}):
        for i2 in i1.find_all('p', {'class':'css-xl6fe0-Text eu5v0x0'}):
            row.append(i2.text)
        for i3 in i1.find_all('p', {'class':'css-7xdcwc-Text eu5v0x0'}):
            row.append(i3.text)
    records_olx['d'].append(row)

#Otodom scrapper
def scrap_otodom(URL, name):
    c = requests.get(URL)
    soup_content = BeautifulSoup(c.content, 'html.parser')
    row=[]
    row.append(name)
    print(name)
    for i1 in soup_content.find_all('div', {'class':'css-1sxg93g e1t9fvcw3'}):
        price = i1.find('strong').get_text()
        row.append(price)
        price_per_meter = i1.find('div', {'class':'css-1p44dor eu6swcv15'}).get_text()
        row.append(price_per_meter)
    for i3 in soup_content.find_all('div', {'class':'css-1ccovha estckra9'}):
        row.append(i3.text)
    records_oto['d'].append(row)
    

def save_to_file(name, dictionary):
    try:
        with open(name, "w", encoding="utf-8") as f:
            for i in dictionary:
                line = ';'.join(i)
                f.write(line+'\n')
                print(line)
        f.close()
        print('SaveToFile: OK.')
    except:
        print('SaveToFile: ERROR.')

#If site status is less than 400, return false and break loop
def check_status(url):
    h = httplib2.Http()
    resp = h.request(url, 'HEAD')
    if (int(resp[0]['status']) < 400):
        return True
    else:
        return False

def loop_for_scrap(city):
    count = 1
    while True:
        if check_status(city[0] + str(count)):
            scrap_olx_for_urls(city[0] + str(count), city[1])
            count += 1
        else:
            break

for i in cities:
    loop_for_scrap(i)

#Save records variables into csv file
save_to_file('raw_olx.csv', records_olx['d'])
save_to_file('raw_oto.csv', records_oto['d'])