import pandas as pd
import numpy as np
import json
import os
import pprint
import re

pd.set_option('display.max_columns', None)

dataset = ('C://Users//pawel//Datasets//Bike Trip//JSON//')
maindata = pd.DataFrame()
pointsdata = pd.DataFrame()
points = pd.DataFrame()

for path, subdirs, files in os.walk(dataset):
    for name in files:
        fname = os.path.join(path, name)
        jsfile = pd.read_json(fname)
        jsdf = pd.DataFrame(jsfile)
        jsdf = jsdf.fillna(method='ffill')
        jsdf = jsdf.dropna()
        jsdf = jsdf.drop_duplicates(subset='start_time')
        pointsdata = pd.concat([pointsdata,jsdf])
        pointsdata = pointsdata[pointsdata['source'] == 'TRACK_MOBILE']
        pointsdata = pointsdata[pointsdata['sport'] == 'CYCLING_SPORT']
        maindata = pd.concat([maindata, jsdf])

data = pd.DataFrame(maindata)
points = pd.DataFrame(pointsdata.loc[:,'points'])

data.drop(['sport', 'source', 'created_date', 'points', 'pictures', 'notes'], axis=1, inplace=True)
data.rename(columns = {'start_time':'Date_start','end_time':'Date_end', 'message': 'Message', 'duration_s': 'Duration_s',
                       'distance_km': 'Distance_km', 'calories_kcal': 'Calories_kcal',
                       'altitude_min_m': 'Altitude_min_m', 'altitude_max_m': 'Altitude_max_m',
                       'speed_avg_kmh': 'Speed_avg_kmh', 'hydration_l': 'Hydration_l',
                       'ascend_m': 'Ascend_m', 'descend_m':'Descend_m'}, inplace=True)

data['Date'] = data['Date_start'].astype(str)
data['Year'] = data['Date'].str.split('-', expand=True)[0].astype(int)
data['Date'] = data['Date'].str.split(' ', expand=True)[0].astype(np.datetime64)

data = data[(data['Date'] >= '2015-10-12') | (data['Date'] <= '2015-08-06') &
                    (data['Date'] >= '2017-07-10') | (data['Date'] <= '2017-09-04')]

def tripcategory(row):
    if row >= 2017:
        return 'Tychy - Fatima - Cabo da Roca'
    else:
        return 'Tychy - Roma'

data['Trip'] = data['Year'].map(tripcategory)
data = data.drop(['Year'], axis=1)
data.set_index('Date', inplace=True)

data.to_csv('C://Users//pawel//Datasets//Bike Trip//Final//Data.csv')
points.to_csv('C://Users//pawel//Datasets//Bike Trip//Final//Points.csv')

points = pd.read_csv('C://Users//pawel//Datasets//Bike Trip//Final//Points.csv')
points = points.iloc[:,-1:]

points = points['points'].str.split('location', expand=True)
points = points.drop(points.columns[0], axis=1)
points = points.reset_index()
points['id'] = points.index
points = points.melt(id_vars=['id'])
points = points[points['variable'] != 'index']
points = points.dropna()
points = points.iloc[:,-1]
points = pd.DataFrame(points)
points = points['value'].str.split(',', expand=True)
points['id'] = points.index
points.set_index('id', inplace=True)

latitude = pd.DataFrame(points[points[0].str.contains('latitude')==True].iloc[:,0])
longitude = pd.DataFrame(points[points[1].str.contains('longitude')==True].iloc[:,1])

altitude1 = points[points[2].str.contains('altitude')==True].iloc[:,2]
altitude2 = points[points[3].str.contains('altitude')==True].iloc[:,3]
altitude3 = points[points[4].str.contains('altitude')==True].iloc[:,4]
altitude4 = points[points[5].str.contains('altitude')==True].iloc[:,5]
altitude5 = points[points[6].str.contains('altitude')==True].iloc[:,6]

distance1 = points[points[2].str.contains('distance_km')==True].iloc[:,2]
distance2 = points[points[3].str.contains('distance_km')==True].iloc[:,3]
distance3 = points[points[4].str.contains('distance_km')==True].iloc[:,4]
distance4 = points[points[5].str.contains('distance_km')==True].iloc[:,5]
distance5 = points[points[6].str.contains('distance_km')==True].iloc[:,6]

speed1 = points[points[2].str.contains('speed_kmh')==True].iloc[:,2]
speed2 = points[points[3].str.contains('speed_kmh')==True].iloc[:,3]
speed3 = points[points[4].str.contains('speed_kmh')==True].iloc[:,4]
speed4 = points[points[5].str.contains('speed_kmh')==True].iloc[:,5]
speed5 = points[points[6].str.contains('speed_kmh')==True].iloc[:,6]

timestamp1 = points[points[2].str.contains('timestamp')==True].iloc[:,2]
timestamp2 = points[points[3].str.contains('timestamp')==True].iloc[:,3]
timestamp3 = points[points[4].str.contains('timestamp')==True].iloc[:,4]
timestamp4 = points[points[5].str.contains('timestamp')==True].iloc[:,5]
timestamp5 = points[points[6].str.contains('timestamp')==True].iloc[:,6]

altitude = pd.DataFrame(pd.concat([altitude1, altitude2, altitude3, altitude4, altitude5]))
distance_km = pd.DataFrame(pd.concat([distance1, distance2, distance3, distance4, distance5]))
speed_kmh = pd.DataFrame(pd.concat([speed1, speed2, speed3, speed4, speed5]))
timestamp = pd.DataFrame(pd.concat([timestamp1, timestamp2, timestamp3, timestamp4, timestamp5]))

latitude = latitude.rename(columns={latitude.columns[0]:'Latitude'})
longitude = longitude.rename(columns={longitude.columns[0]:'Longitude'})
altitude = altitude.rename(columns={altitude.columns[0]:'Altitude'})
distance_km = distance_km.rename(columns={distance_km.columns[0]:'Distance_km'})
speed_kmh = speed_kmh.rename(columns={speed_kmh.columns[0]:'Speed_kmh'})
timestamp = timestamp.rename(columns={timestamp.columns[0]:'Timestamp'})

points = pd.concat([latitude, longitude, altitude, distance_km, speed_kmh, timestamp], axis=1)

latitude = points['Latitude'].str.split(':', expand=True)
longitude = points['Longitude'].str.split(':', expand=True)
altitude = points['Altitude'].str.split(':', expand=True)
distance = points['Distance_km'].str.split(':', expand=True)
speed = points['Speed_kmh'].str.split(':', expand=True)
timestamp = points['Timestamp'].str.split('timestamp', expand=True)

fpoints = pd.DataFrame()

fpoints['Latitude'] = latitude[2].apply(lambda s: s.replace('}','')).astype(np.float64)
fpoints['Longitude'] = longitude[1].apply(lambda s: s.replace('}',''))
fpoints['Longitude'] = fpoints['Longitude'].apply(lambda s: s.replace(']',''))
fpoints['Longitude'] = fpoints['Longitude'].apply(lambda s: s.replace(' ','')).astype(np.float64)
fpoints['Altitude'] = altitude[1].astype(str).apply(lambda s: s.replace('}','')).astype(np.float64)
fpoints['Distance_km'] = distance[1].astype(str).apply(lambda s: s.replace('}','')).astype(np.float64)
fpoints['Speed_kmh'] = speed[1].astype(str).apply(lambda s: s.replace('}','')).astype(np.float64)
fpoints['Timestamp'] = timestamp[1].astype(str).apply(lambda s: s.replace('}',''))
fpoints['Timestamp'] = fpoints['Timestamp'].apply(lambda s: s.replace('{',''))
fpoints['Timestamp'] = fpoints['Timestamp'].apply(lambda s: s.replace("'",''))
fpoints['Timestamp'] = fpoints['Timestamp'].apply(lambda s: s.replace(']',''))
fpoints['Timestamp'] = fpoints['Timestamp'].str.slice(2)

points = pd.DataFrame(fpoints)

points['Month'] = points['Timestamp'].str.split(' ', expand=True)[1]
points['Month'] = points['Month'].apply(lambda s: s.replace('Jul','07'))
points['Month'] = points['Month'].apply(lambda s: s.replace('Aug','08'))
points['Month'] = points['Month'].apply(lambda s: s.replace('Sep','09'))
points['Date'] = points['Timestamp'].str.split(' ', expand=True)[5] \
    + '-' + points['Month'] + '-' + points['Timestamp'].str.split(' ', expand=True)[2]
points['Year'] = points['Timestamp'].str.split(' ', expand=True)[5]
points['Time'] = points['Timestamp'].str.split(' ', expand=True)[3]
points['Hour'] = points['Time'].str.split(':', expand=True)[0]
points['Coordinates'] = points['Latitude'].astype(str) + ':' + points['Longitude'].astype(str)
points.sort_values(['Date', 'Time'], ascending=[True, True])

points = points[(points['Date'] >= '2015-10-12') | (points['Date'] <= '2015-08-06') &
                    (points['Date'] >= '2017-07-10') | (points['Date'] <= '2017-09-04')]

points.to_csv('C://Users//pawel//Datasets//Bike Trip//Final//Points.csv')

coordinates = pd.DataFrame()
coordinates['First coordinate'] = points.pivot_table(values=['Coordinates'], index=['Date', 'Hour'], aggfunc='first')
coordinates['Last coordinate'] = points.pivot_table(values=['Coordinates'], index=['Date', 'Hour'], aggfunc='last')
coordinates.reset_index(inplace=True)
coordinates.drop(['Hour'], axis=1, inplace=True)
coordinates = coordinates.melt(id_vars=['Date'])
coordinates.drop(['variable'], axis=1, inplace=True)
coordinates['Latitude'] = coordinates['value'].str.split(':', expand=True)[0]
coordinates['Longitude'] = coordinates['value'].str.split(':', expand=True)[1]
coordinates.drop(['value'], axis=1, inplace=True)
coordinates.set_index('Date', inplace=True)

coordinates.to_csv('C://Users//pawel//Datasets//Bike Trip//Final//Coordinates.csv')