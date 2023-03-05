import pandas as pd
import numpy as np
import pprint
import re

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

adr = pd.read_csv('C://Users//pawel//Datasets//Bike Trip//Final//Coordinates & Addresses.csv',names = ['location', 'value', 'date'], delimiter=':')
adr = pd.DataFrame(adr)

adr = adr.fillna(method='ffill')
adr['location'] = adr['location'].apply(lambda s: s.replace('[',''))
adr['location'] =adr['location'].apply(lambda s: s.replace('{',''))
adr['location'] = adr['location'].apply(lambda s: s.replace("'",''))
adr['location'] = adr['location'].apply(lambda s: s.replace(" ",''))
adr['value'] = adr['value'].apply(lambda s: s.replace(']',''))
adr['value'] = adr['value'].apply(lambda s: s.replace('}',''))
adr['value'] = adr['value'].apply(lambda s: s.replace("'",''))
adr['value'] = adr['value'].apply(lambda s: s.replace(",",''))
adr = adr[adr['location'] != 'date']
adr = adr[adr['location'] != 'name']
adr = adr.reset_index()
adr = adr.drop(['index'], axis=1)
adr['id'] = adr.index.astype(str)
adr['temp'] = adr['location'] + adr['id']
adr = adr.sort_index(ascending=False)

def id(row):
    if row[:3] == 'lon':
        return row[3:]
    elif row[:3] != 'lon':
        return np.nan

adr['temp'] = adr['temp'].map(id)
adr = adr.fillna(method='ffill')

adr['temp'] = adr['temp'] + ' ' + adr['date']
adr = adr.drop(['id'], axis=1)

adr.set_index('temp', inplace=True)
adr = adr.drop(['date'], axis=1)
adr['temp'] = adr.index

adr = adr.pivot(index='temp', columns='location', values='value')
adr['temp'] = adr.index

adr['date'] = adr['temp'].str.split(' ', expand=True)[1]
adr = adr.drop(['temp'], axis=1)
adr['date'] = adr['date'].apply(lambda s: s.replace("'",""))
adr.set_index('date', inplace=True)
adr = adr.sort_index(ascending=True)

adr = adr.rename(columns = {'admin1':'Area', 'admin2':'Province', 'cc':'Country', 'lat': 'Latitude', 'lon': 'Longitude'})

adr['Country'] = adr['Country'].apply(lambda s: s.replace(' ',''))
adr['Latitude'] = adr['Latitude'].apply(lambda s: s.replace(' ',''))
adr['Longitude'] = adr['Longitude'].apply(lambda s: s.replace(' ',''))
adr['Area'] = adr['Area'].apply(lambda s: s.replace(' ',''))
adr['Area'] = adr['Area'].apply(lambda s: s.replace('"',''))
adr['Province'] = adr['Province'].apply(lambda s: s.replace(' ',''))
adr['Province'] = adr['Province'].apply(lambda s: s.replace('"',''))

def countryname(row):
    if row == 'PL':
        return 'Poland'
    elif row == 'CZ':
        return 'Czech Republic'
    elif row == 'AT':
        return 'Austria'
    elif row == 'SK':
        return 'Slovakia'
    elif row == 'HU':
        return 'Hungary'
    elif row == 'HR':
        return 'Croatia'
    elif row == 'SI':
        return 'Slovenia'
    elif row == 'IT':
        return 'Italy'
    elif row == 'VA':
        return 'Vaticano'
    elif row == 'FR':
        return 'France'
    elif row == 'MC':
        return 'Monaco'
    elif row == 'ES':
        return 'Spain'
    elif row == 'GI':
        return 'Gibraltar'
    elif row == 'PT':
        return 'Portugal'

adr['Country'] = adr['Country'].map(countryname)

adr['Date'] = adr.index
adr['Date'] = adr['Date'].apply(lambda s: s.replace("'",''))
adr['Trip'] = adr['Date'].str.split('-', expand=True)[0].astype(int)

def tripcategory(row):
    if row >= 2017:
        return 'Tychy - Fatima - Cabo da Roca'
    else:
        return 'Tychy - Roma'

adr['Trip'] = adr['Trip'].map(tripcategory)

adr['Latitude'] = adr['Latitude'].astype(np.float64)
adr['Longitude'] = adr['Longitude'].astype(np.float64)
adr['Date'] = adr['Date'].astype(np.datetime64)

adr.to_csv('C://Users//pawel//Datasets//Bike Trip//Final//Locations.csv')