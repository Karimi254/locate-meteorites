import math
import requests

#Haversine formula for calculating long and latitude distances
#eg lat1 = paris latitude, lon1 = paris longitude,
# lat2 = your city lat, lon2= your city longitude
def calc_dist(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin( (lat2 - lat1) / 2 ) ** 2 + \
      math.cos(lat1) * \
      math.cos(lat2) * \
      math.sin( (lon2 - lon1) / 2 ) ** 2

    return 6372.8 * 2 * math.asin(math.sqrt(h))


def get_dist(meteor):
    """Function that sorts the meteor dictionary by its keys"""
    #math.inf retuns an infinite number
    return meteor.get('distance', math.inf)

if __name__ == '__main__':
    #set your location as a tuple og lat and long
    my_loc = (-1.300783, 36.815706)

    #Use NASA public API to load Meteorites data
    meteor_resp = requests.get('https://data.nasa.gov/resource/y77d-th95.json')
    #convert the response to more Pythonic format
    meteor_data = meteor_resp.json()

    for meteor in meteor_data:
        #Checks if item being iterated on contains both the longitude and latitude.
        if not ('reclat' in meteor and 'reclong' in meteor): continue
        #We use float() to convert the reclat and reclong strings to float for
        #calculating distance.
        meteor['distance'] = calc_dist(float(meteor['reclat']),
                                       float(meteor['reclong']),
                                       my_loc[0],
                                       my_loc[1])

    meteor_data.sort(key=get_dist)

    print(meteor_data[0:10])
