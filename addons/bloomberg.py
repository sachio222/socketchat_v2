import requests
from pprint import pprint

class Bloomberg():
    def __init__(self):
        self.get_stories_about(['/bloomberg', 'usdjpy'])

    def get_stories_about(self, msg):
        msg = ' '.join(msg[1:])
        print(f'-$- Bloomberg news about {msg}')
        url = "https://bloomberg-market-and-financial-news.p.rapidapi.com/stories/list"

        querystring = {"template":"CURRENCY","id":msg}

        headers = {
            'x-rapidapi-host': "bloomberg-market-and-financial-news.p.rapidapi.com",
            'x-rapidapi-key': "YOUR_RAPIDAPI_KEY"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        stories = response.json()['stories']
        # pprint(stories[1])
        for i, story in enumerate(stories):
            # pprint(stories[story])
            label = stories[i]['primarySite']
            title = stories[i]['title']
            url = stories[i]['shortURL']
            internalID = stories[i]['internalID']
            print(f"{i+1}. {title} [{label.capitalize()}]")
            print(f"{url}\n")

if __name__ == "__main__()":
    bloomberg = Bloomberg()