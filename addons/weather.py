import requests


def report(msg):
    loc = ''
    weather = "-!- Can't reach weather service right meow."

    try:
        # loc = input('-?- Where? (press enter for ip location): ')
        if msg[9:]:
            loc = msg[9:]
        weather = requests.get(f'http://wttr.in/{loc}?format=4')
        weather = weather.text
    except:
        pass

    return weather
