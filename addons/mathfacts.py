import os

import requests
from pprint import pprint


def get_fact(msg):
    if len(msg) == 1:
        number = 'random'
    else:
        number = msg[1]

    # Get your own key at rapidapi.com and export it as RAPIDAPI_KEY.
    api_key = os.environ.get("RAPIDAPI_KEY")
    if not api_key:
        print('-!- Set RAPIDAPI_KEY to use math trivia.')
        return

    url = f"https://numbersapi.p.rapidapi.com/{number}/trivia"

    querystring = {"fragment": "false", "notfound": "floor", "json": "true"}

    headers = {
        'x-rapidapi-host': "numbersapi.p.rapidapi.com",
        'x-rapidapi-key': api_key
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    # pprint(response.json())
    number = response.json()['number']
    fact = response.json()['text']
    print('-#- Math Trivia!\n')
    print(f'{number} is {fact}')


# math_facts(111111)
