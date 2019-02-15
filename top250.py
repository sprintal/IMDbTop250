import requests
import json
import time
from bs4 import BeautifulSoup as bs

url = "https://www.imdb.com/chart/top?ref_=nv_mv_250"
t = time.localtime(time.time())
date = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday)
with open('imdb.json', 'r') as f:
    data = json.load(f)
try:
    # data = dict()
    r = requests.get(url)
    r.raise_for_status()
    soup = bs(r.text, "html.parser")
    table = soup.tbody.contents
    for item in table:
        if type(item) is not type(table[0]):
            td = item.find('td', class_='titleColumn')
            a = td.a
            name = a.get_text().strip()
            url = a['href']
            tt = url.split('/')[2].strip()
            year = item.find('span', class_='secondaryInfo').get_text().strip()
            year = year[1:-1]
            rating = item.find('td', class_='ratingColumn').get_text().strip()
            str = item.find('td', class_ = 'titleColumn').get_text().strip()
            rank = str[:str.find('.')]
            print(name, tt, year, rating, rank)
            if tt in data:
                ranks = data[tt]['rank']
                ratings = data[tt]['rating']
            else:
                ranks = dict()
                ratings = dict()
            
            ranks[date] = rank
            ratings[date] = rating
            data[tt] = {
                'name': name,
                'year': year,
                'rating': ratings,
                'rank': ranks

            }
    print(data)
    
    with open('imdb.json', 'w') as f:
        json.dump(data, f)


except:
    print("Failed")
