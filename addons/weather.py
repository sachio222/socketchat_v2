import requests


def report(msg):

    loc = ''
    weather = "-!- Can't reach weather service right meow."
    print_lines = None

    try:
        # loc = input('-?- Where? (press enter for ip location): ')

        if '1line' in msg:
            msg.remove('1line')
            fmt = 'format=4'
        elif 'full' in msg:
            msg.remove('full')
            fmt = ''
            print_lines = -1

        else:
            fmt = ''
            print_lines = 7

        if msg[1:]:
            loc = ' '.join(msg[1:])

        url = f'http://wttr.in/{loc}?{fmt}'
        weather = requests.get(url)

        print('\r-=- ', end='')
        for line in weather.text.splitlines()[:print_lines]:
            print(line)


    except:
        pass

    return True
