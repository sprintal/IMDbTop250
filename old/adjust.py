import json

with open('imdb.json', 'r') as f:
    movies = json.load(f)

newMovies = dict()
newRatings = {}

for item in movies:
    newRatings = {}
    name = movies[item]['name']
    year = movies[item]['year']
    ratings = movies[item]['rating']
    ranks = movies[item]['rank']
    newMovies[item] = {
        'name': name,
        'year': int(year),
        'ratings': {}
    }
    for part in ratings:
        parts = part.split(' ')
        date = parts[0]
        time = parts[1]
        data = [float(ratings[part]), int(ranks[part])]
        if date in newRatings:
            newRatings[date][time] = data
        else:
            newRatings[date] = dict()
            newRatings[date][time] = data
    newMovies[item]['ratings'] = newRatings

with open('new.json', 'w') as f:
    json.dump(newMovies, f)