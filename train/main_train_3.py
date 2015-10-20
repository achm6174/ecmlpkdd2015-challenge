import json
import zipfile
import numpy as np
import pandas as pd
import time
import geometric_med as gm

### Get Haversine distance
def get_dist(lonlat1, lonlat2):
    lon_diff = np.abs(lonlat1[0]-lonlat2[0])*np.pi/360.0
    lat_diff = np.abs(lonlat1[1]-lonlat2[1])*np.pi/360.0
    a = np.sin(lat_diff)**2 + np.cos(lonlat1[1]*np.pi/180.0) * np.cos(lonlat2[1]*np.pi/180.0) * np.sin(lon_diff)**2
    d = 2*6371*np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return(d)

# read test
test = pd.read_csv(open('../input/test.csv'), usecols=['TRIP_ID', 'POLYLINE'])
test['POLYLINE'] = test['POLYLINE'].apply(json.loads)
test['snapshots'] = test['POLYLINE'].apply(len)
print sum(test['snapshots']-1)*15
test['lonlat'] = test['POLYLINE'].apply(lambda x: x[0])
test = test.reset_index(drop=True)

# read train
# Store total travel time
train = pd.read_csv(open('./input/train.csv'), usecols=['TRIP_ID', 'POLYLINE'], converters={'POLYLINE': lambda x: len(json.loads(x))})
# Store last location
train_2 = pd.read_csv(open('./input/train.csv'), usecols=['TRIP_ID', 'POLYLINE'], converters={'POLYLINE': lambda x: json.loads(x)[-1:]})
train_2['POLYLINE'] = train_2['POLYLINE'].apply(lambda x: [0,0] if x==[] else x[0])
train = train.reset_index(drop=True)
train_2 = train_2.reset_index(drop=True)

test['TRAVEL_TIME'] = 0
test['FINAL_LOC_1'] = 0.0
test['FINAL_LOC_2'] = 0.0

similar_trip = 100

for row, ll in enumerate(test['lonlat']):
    print row
    f_name = 'trip_'+ `row` + '_dtw_%i.csv' %similar_trip
    dtw_index = [int(line.rstrip('\n')) for line in open(f_name)]

    d = []
    for i in dtw_index:
        d.append(train.loc[i,'POLYLINE'])

    # Estimated travel time
    test.loc[row, 'TRAVEL_TIME']  = 15 * (np.median(d)-1)
    print test.loc[row, 'TRAVEL_TIME']

    # Estimated location
    location_index = []
    for i in dtw_index:
        location_index.append((train.loc[i, 'POLYLINE']==(np.median(d))))

    l=[]
    for i in range(0,len(location_index)):
        if (location_index[i]==True):
            if (train_2.loc[dtw_index[i],'POLYLINE'] != [0,0] ):
                l.append(train_2.loc[dtw_index[i],'POLYLINE'])
    print l

    test.loc[row, 'FINAL_LOC_1']  = gm.geometric_median(np.array(l))[0]
    test.loc[row, 'FINAL_LOC_2']  = gm.geometric_median(np.array(l))[1]

test['TRAVEL_TIME'] = test['TRAVEL_TIME'].astype(int)
test['FINAL_LOC_1'] = test['FINAL_LOC_1'].astype(float)
test['FINAL_LOC_2'] = test['FINAL_LOC_2'].astype(float)
test[['TRIP_ID', 'TRAVEL_TIME', 'FINAL_LOC_1', 'FINAL_LOC_2']].to_csv('submission.csv', index=False)
