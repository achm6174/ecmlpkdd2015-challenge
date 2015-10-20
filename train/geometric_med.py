import numpy as np
from scipy.spatial.distance import cdist, euclidean

def get_dist(lonlat1, lonlat2):
    lon_diff = np.abs(lonlat1[0]-lonlat2[0])*np.pi/360.0
    lat_diff = np.abs(lonlat1[1]-lonlat2[1])*np.pi/360.0
    a = np.sin(lat_diff)**2 + np.cos(lonlat1[1]*np.pi/180.0) * np.cos(lonlat2[1]*np.pi/180.0) * np.sin(lon_diff)**2
    d = 2*6371*np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return(d)


def geometric_median(X, eps=1e-12, step=10000):
    y = np.mean(X, 0)

    steps=0
    while True:
        steps+=1
        #D = cdist(X, [y])
        D = []
        for temp_loc in X:
            D.append([get_dist(temp_loc,y)])
        D = np.array(D)

        nonzeros = (D != 0)[:, 0]

        Dinv = 1 / D[nonzeros]
        Dinvs = np.sum(Dinv)
        W = Dinv / Dinvs
        T = np.sum(W * X[nonzeros], 0)

        num_zeros = len(X) - np.sum(nonzeros)
        if num_zeros == 0:
            y1 = T
        elif num_zeros == len(X):
            return y
        else:
            R = (T - y) * Dinvs
            r = np.linalg.norm(R)
            rinv = 0 if r == 0 else num_zeros/r
            y1 = max(0, 1-rinv)*T + min(1, rinv)*y
        #if euclidean(y, y1) < eps:
        if (get_dist(y, y1) < eps or steps > step):
            #print steps
            #print "###########"
            return y1
        y = y1
