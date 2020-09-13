import requests
from pprint import pprint


def get_fact(msg):
    if len(msg) == 1:
        number = 'random'
    else:
        number = msg[1]

    url = f"https://numbersapi.p.rapidapi.com/{number}/trivia"

    r = requests.get(url)

    querystring = {"fragment": "false", "notfound": "floor", "json": "true"}

    headers = {
        'x-rapidapi-host': "numbersapi.p.rapidapi.com",
        'x-rapidapi-key': "YOUR_RAPIDAPI_KEY"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    # pprint(response.json())
    number = response.json()['number']
    fact = response.json()['text']
    print('-#- Math Trivia!\n')
    print(f'{number} is {fact}')


# math_facts(111111)
