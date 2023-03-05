import pandas as pd
import numpy as np
import pprint
import reverse_geocoder as rg
import sys

pd.set_option('display.max_columns', None)

coordinates = pd.read_csv('C://Users//pawel//Datasets//Bike Trip//Final//Coordinates.csv', delimiter=',')

latitude = coordinates['Latitude']
longitude = coordinates['Longitude']
date = coordinates['Date']

longitude = longitude.values.tolist()
latitude = latitude.values.tolist()
date = date.values.tolist()
rng = coordinates['Longitude']

for value in range(0,len(rng)):
    def reverseGeocode(addresses):
        result = rg.search(addresses)
        restorePoint = sys.stdout
        sys.stdout = open('C://Users//pawel//Datasets//Bike Trip//Final//Coordinates & Addresses.csv', 'a')
        datedict = 'Date' + ':' + date[0] + ':' + date[0]
        pprint.pprint(datedict)
        pprint.pprint(result)
        sys.stdout = restorePoint

    if __name__ == "__main__":
        addresses = (latitude[0], longitude[0])
        reverseGeocode(addresses)

    del latitude[0]
    del longitude[0]
    del date[0]

next