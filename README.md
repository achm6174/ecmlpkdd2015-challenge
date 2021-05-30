## Summary
This is my solution for EMCL/PKDD 2015 Discovery Challenge Taxi Trajectory Prediction and Taxi Trip Time Prediction.

## Problem
To improve the efficiency of electronic taxi dispatching systems it is important to be able to predict the final destination of a taxi while it is in service. Particularly during periods of high demand, there is often a taxi whose current ride will end near or exactly at a requested pick up location from a new rider. If a dispatcher knew approximately where their taxi drivers would be ending their current rides, they would be able to identify which taxi to assign to each pickup request.

The spatial trajectory of an occupied taxi could provide some hints as to where it is going. Similarly, given the taxi id, it might be possible to predict its final destination based on the regularity of pre-hired services. In a significant number of taxi rides (approximately 25%), the taxi has been called through the taxi call-center, and the passenger’s telephone id can be used to narrow the destination prediction based on historical ride data connected to their telephone id.

## Our solution
The summary of the approach is as follow:

* Perform trip matching first by extracting the trip with closest starting point on the map based on Haversine distance
* Match similar trips using Multivariate Dynamic Time Wrapping.
* Driver features are extracted and trained with Machine Learning model.

The model gives rank 4th for trip time prediction and 22th for trajectory prediction.

## Instruction
#### Download Data
* download `train.csv.zip`, `test.csv.zip`, `train.csv`, `test.csv`, and put into folder `./input`.

#### Generate prediction
* run `./main.sh` to generate submission, which take roughly 1 day, result will be at `./train/output` .

#### Sample submission
* `./sample_prediction`

