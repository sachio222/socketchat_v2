import requests


def report(msg):

    loc = ''
    split = msg[9:].split(' ')
    weather = "-!- Can't reach weather service right meow."

    try:
        # loc = input('-?- Where? (press enter for ip location): ')
        if msg[9:]:
            loc = msg[9:]

        if '1line' in split:
            split.remove('1line')
            fmt = 'format=4'
        else:
            fmt = ''

        loc = ' '.join(split)
        url = f'http://wttr.in/{loc}?{fmt}'
        weather = requests.get(url)

        print('\r-=- ', end='')
        for line in weather.text.splitlines()[:7]:
            print(line)

    except:
        pass

    return True
