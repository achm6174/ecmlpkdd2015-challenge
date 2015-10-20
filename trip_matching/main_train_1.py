import json
import zipfile
import numpy as np
import pandas as pd
import time
from dtw import dtw

### Control the number of closest trips used to calculate trip duration
N_trips = 20000

### Get Haversine distance
def get_dist(lonlat1, lonlat2):
    lon_diff = np.abs(lonlat1[0]-lonlat2[0])*np.pi/360.0
    lat_diff = np.abs(lonlat1[1]-lonlat2[1])*np.pi/360.0
    a = np.sin(lat_diff)**2 + np.cos(lonlat1[1]*np.pi/180.0) * np.cos(lonlat2[1]*np.pi/180.0) * np.sin(lon_diff)**2
    d = 2*6371*np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return(d)

# read test
zf = zipfile.ZipFile('../input/test.csv.zip')
test = pd.read_csv(zf.open('test.csv'), usecols=['TRIP_ID', 'POLYLINE'])
test['POLYLINE'] = test['POLYLINE'].apply(json.loads)
test['snapshots'] = test['POLYLINE'].apply(len)
test['lonlat'] = test['POLYLINE'].apply(lambda x: x[0])
test = test.reset_index(drop=True)

# read train
zf = zipfile.ZipFile('../input/train.csv.zip')
train = pd.read_csv(zf.open('train.csv'), usecols=['TRIP_ID', 'POLYLINE'], converters={'POLYLINE': lambda x: json.loads(x)[0:1]})
train['snapshots'] = train['POLYLINE'].apply(len)
train['lonlat'] = train['POLYLINE'].apply(lambda x: [0,0] if x==[] else x[0])
train = train.reset_index(drop=True)
print train

test['TRAVEL_TIME'] = 0

for row, ll in enumerate(test['lonlat']):
    print row

    # Find the closest starting position
    d = train['lonlat'].apply(lambda x: get_dist(x, ll))
    i = np.argpartition(d, N_trips)[0:N_trips]

    # Save file
    file_name = './output_1/trip_'+ `row` + '.csv'
    f = open(file_name, 'w')
    print file_name
    for item in i:
        f.write("%s\n" % item)
    f.close()
