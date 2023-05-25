from math import radians, sin, cos, sqrt, atan2

def distance(lat1, lon1, lat2, lon2):
    # convert degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371 # radius of Earth in kilometers
    distance = r * c
    # print("Distance: ", distance)
    return distance
