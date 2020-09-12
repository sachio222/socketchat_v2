import os
import re
import folium
from geopy.geocoders import Nominatim
# added geocoder later for ip address.
# Some redundancy with geopy.
import geocoder

def open_map(msg):
    def msg_ele(msg):
        for word in msg:
            if '=' in word:
                return
            yield word

    new_msg = list(msg_ele(msg))
    
    print('generated msg: ', new_msg[1:])
    try:
        msg = ' '.join(msg[1:])
    except:
        pass
    map_style = 'OpenStreetMap'
    zoom = 10

    styles = {'toner': 'Stamen Toner',
              'default': 'OpenStreetMap',
              'terrain': 'Stamen Terrain'  }

    if 'style=' in msg:
        end = msg.find('style=') + len('style=')
        part = msg[end:].split(' ')
        map_style = styles.get(part[0], 'default')

    if 'zoom=' in msg:
        end = msg.find('zoom=') + len('zoom=')
        part = msg[end:].split(' ')
        if 0 < int(part[0]) <= 20: 
            zoom = int(part[0])

    address = ' '.join(new_msg[1:])
    geolocator = Nominatim(user_agent='myGeocoder')

    try:
        location = geolocator.geocode(address)
        coords = [location.latitude, location.longitude]
    except:
        location = geolocator.geocode(geocoder.ip('me').city)
        coords = [location.latitude, location.longitude]

    m = folium.Map(
        location=coords,
        tiles=map_style,
        zoom_start=zoom
    )

    m.add_child(folium.LatLngPopup())

    folium.Marker(coords, popup=f'<i>{location.address}</i>').add_to(m)
    url = 'm.html'
    m.save(url)
    try:
        print(f'Opening map for {location.address}')
        os.system(f'open {url}')
    except:
        try:
            # Something to try for windows
            os.startfile(url)
        except:
            print('Could not open file from terminal.')

if __name__ == "__main__":
    msg = '/map Tokyo, Japan style=terrain zoom=2'
    msg = msg.split(' ')
    open_map(msg)