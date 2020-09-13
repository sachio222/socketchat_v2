import os
import re
import folium
from folium.plugins import MeasureControl, MiniMap
from geopy.geocoders import Nominatim
# added geocoder later for ip address.
# Some redundancy with geopy.
import geocoder


def open_map(msg):

    map_style = 'OpenStreetMap'

    zoom = 10

    styles = {
        'toner': 'Stamen Toner',
        'default': 'OpenStreetMap',
        'terrain': 'Stamen Terrain',
        'watercolor': 'stamenwatercolor',
        'position': 'cartodbpositron',
        'dark': 'cartodbdark_matter'
    }

    def msg_ele(msg):
        """Generator, stops at args."""
        for word in msg:
            if '=' in word:
                return
            yield word

    new_msg = list(msg_ele(msg))
    new_msg = ' '.join(new_msg[1:])

    try:
        msg = ' '.join(msg[1:])
    except:
        pass

    if 'style=' in msg:
        end = msg.find('style=') + len('style=')
        part = msg[end:].split(' ')
        map_style = styles.get(part[0], 'default')

    if 'zoom=' in msg:
        end = msg.find('zoom=') + len('zoom=')
        part = msg[end:].split(' ')
        if 0 < int(part[0]) <= 18:
            zoom = int(part[0])

    address = new_msg
    geolocator = Nominatim(user_agent='myGeocoder')

    try:
        location = geolocator.geocode(address)
        coords = [location.latitude, location.longitude]
    except:
        location = geolocator.geocode(geocoder.ip('me').city)
        coords = [location.latitude, location.longitude]

    m = folium.Map(location=coords, tiles=map_style, zoom_start=zoom)

    # folium.TileLayer('openstreetmap', name='Open Street Map').add_to(m)
    folium.TileLayer('OpenStreetMap', name='Open Street Maps').add_to(m)
    folium.TileLayer('Stamen Toner', name='Toner').add_to(m)
    folium.TileLayer('Stamen Terrain', name='Terrain').add_to(m)
    folium.TileLayer('stamenwatercolor', name='Water Color').add_to(m)
    folium.TileLayer('cartodbpositron', name='Positron').add_to(m)
    folium.TileLayer('cartodbdark_matter', name='Dark Matter').add_to(m)
    folium.LayerControl().add_to(m)

    m.add_child(MeasureControl())
    m.add_child(
        MiniMap(position='bottomright',
                zoom_animation=True,
                toggle_display=True,
                minimized=True))
    m.add_child(folium.LatLngPopup())

    if map_style == 'Stamen Toner':
        folium.Circle(
            radius=500,
            location=coords,
            popup=f'<i>{location.address}</i>',
            color='crimson',
            fill=True,
        ).add_to(m)
    else:
        folium.Marker(coords, popup=f'<i>{location.address}</i>').add_to(m)

    path = 'downloads/map.html'
    m.save(path)

    try:
        print(f'-=- Opening map for {location.address}')
        os.system(f'open {path}')
    except:
        try:
            # Something to try for windows
            os.startfile(path)
        except:
            print('-!- Could not open file from terminal.')


if __name__ == "__main__":
    msg = '/map Tokyo, Japan style=default zoom=15'
    msg = msg.split(' ')
    open_map(msg)
