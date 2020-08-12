import requests


def phase():

    try:
        url = f'http://wttr.in/moon'
        moon = requests.get(url)
        for line in moon.text.splitlines()[:-1]:
            print(line)

    except:
        print("-!- Can't reach the moon right now. Try again later.")

    return True
