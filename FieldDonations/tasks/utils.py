import geopy
from geopy.distance import great_circle
from geopy.geocoders import Nominatim

from .models import FieldOffice

def get_address(lat, lon):
    geolocator = Nominatim()
    location = geolocator.reverse((lat, lon))
    if location.address:
        return location.address
    else:
        return "your location"

def verify_input(location, limit):
    geolocator = Nominatim()
    coords = geolocator.geocode(location)
    if coords and coords.latitude and coords.longitude:
        try:
            limit = int(limit)
        except:
            limit = 25
        return {'lat': coords.latitude, 'lon': coords.longitude, 'limit': limit}
    else:
        return False

def return_within_limit(ulat, ulong, limit):
    field_office_list = []
    try:
        user_loc = (ulat, ulong)
        for fo in FieldOffice.objects.all():
            distance = great_circle(user_loc, (fo.latitude, fo.longitude)).miles
            if distance < float(limit):
                field_office_list.append({'office': fo, 'distance': "%.2f" % (distance)})
    except:
        pass
    return field_office_list
