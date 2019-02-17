import requests
import json
import time
import bs4
from bs4 import BeautifulSoup as bs

url = "https://www.imdb.com/chart/top"

with open('imdb.json', 'r') as f:
    movies = json.load(f)

attempts = 0
success = False

while attempts < 3 and not success:
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        soup = bs(r.text, "html.parser")
        table = soup.tbody.contents
        t = time.localtime(time.time())
        date = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + " " + \
            str(t.tm_hour).zfill(2) + ":" + \
            str(t.tm_min).zfill(2) + ":" + str(t.tm_sec).zfill(2)

        for item in table:

            if isinstance(item, bs4.element.Tag):
                td = item.find('td', class_='titleColumn')
                a = td.a
                name = a.get_text().strip()
                url = a['href']
                tt = url.split('/')[2].strip()
                year = item.find(
                    'span', class_='secondaryInfo').get_text().strip()
                year = year[1:-1]
                rating = item.find(
                    'td', class_='ratingColumn').get_text().strip()
                rankStr = item.find('td', class_='titleColumn').get_text().strip()
                rank = rankStr[:rankStr.find('.')]

                if tt in movies:
                    ranks = movies[tt]['rank']
                    ratings = movies[tt]['rating']
                else:
                    ranks = dict()
                    ratings = dict()

                ranks[date] = rank
                ratings[date] = rating
                movies[tt] = {
                    'name': name,
                    'year': year,
                    'rating': ratings,
                    'rank': ranks
                }

        with open('imdb.json', 'w') as f:
            json.dump(movies, f)

        success = True
        log = "SUCCEEDED @ " + date + " with " + str(attempts + 1) + " attempts.\n"

    except:
        print("Failed")
        attempts += 1
        log = "FAILED @ " + date + ", it was the " + str(attempts) + " attempt.\n"
        if attempts == 3:
            break

with open('log.txt', 'a') as f:
    f.write(log)