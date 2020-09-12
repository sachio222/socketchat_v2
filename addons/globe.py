import os
from PIL import Image
import io


import json
import requests
from pprint import pprint
from tqdm import trange, tqdm

def animate():
    path = './downloads/globe/'
    if not os.path.exists(path):
        os.makedirs(path)

    url = 'https://epic.gsfc.nasa.gov/api/images.php'
    r = requests.get(url)
    data = r.json()

    fn = f'earth{data[0]["date"].replace(" ", "_").replace(":", ".")}.png'
    stack = []
    
    print('-=- Earth Polychromatic Imaging Camera (EPIC)')
    print(f'-=- Getting latest images from {data[0]["date"]}.')
    for d in tqdm(data, desc='-+- Downloading'):
        date = d['date'].split(' ')[0].replace('-', '/')
        img_id = d['image']
        # with open(f'{path}{img_id}.png', 'wb') as f:
        img_url = f'https://epic.gsfc.nasa.gov/archive/natural/{date}/png/{img_id}.png'
        r = requests.get(img_url).content
        img = Image.open(io.BytesIO(r))
        stack.append(img)
            # f.write(r)

    for i in tqdm(range(1), desc="-+- Animating PNG"):      
        stack[0].save(f'{path}{fn}', format='PNG', save_all=True, append_images=stack[1:], duration=1000, loop=0, allow_mixed=True)
    
    print(f'-+- File saved to {path}{fn}')
    del stack
    try:
        os.system(f'open {path}{fn}')
    except:
        try:
            # Something to try for windows
            os.startfile(path)
        except:
            print('-!- Could not open file from terminal.')

if __name__ == '__main__':
    animate()