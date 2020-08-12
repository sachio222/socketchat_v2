"""
Thanks to:
https://github.com/nmercer/urbandict_py/blob/master/urbandict.py
"""

import urllib.parse, urllib.request, json
import re

_URBANDICT_URL = "http://api.urbandictionary.com/v0/define?term="

def _run_urbandict(search):
    safe_search = ""
    words = ' '.join(search.split()).split(' ')
    for idx, word in enumerate(words):
        if len(words) == idx+1:

            safe_search += "%s" % urllib.parse.quote_plus(word)
        else:
            safe_search += "%s+" % urllib.parse.quote_plus(word)
    response = urllib.request.urlopen(_URBANDICT_URL + safe_search)
    return json.loads(response.read())

def urbandict(word):
    term = word[8:]
    try:
        entry = _run_urbandict(term)
        entry = entry['list'][0].get('definition').replace('[', '').replace(']', '')
        print(f'-=- 📖 UrbanDictionary.com\n')
        print(f'Top definition for "{term}":\n')
        print(entry)
    except:
        print(f'-=- 📖 UrbanDictionary.com\n')
        print(f'Nothing found for "{term}". Try something else.')

