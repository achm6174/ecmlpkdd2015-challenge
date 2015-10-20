## Summary
This is the simplified version of my model framework in EMCL/PKDD 2015: Taxi Trajectory Prediction https://www.kaggle.com/c/pkdd-15-predict-taxi-service-trajectory-i and Taxi Trip time Prediction https://www.kaggle.com/c/pkdd-15-taxi-trip-time-prediction-ii. The idea is 
* Perform trip matching first by extracting the trip with closest starting point on the map based on Haversine distance
* Match similar trips using Multivariate Dynamic Time Wrapping. 
* Driver features were extracted, trained with any Machine Learning model.

## Result
The sample prediction `./sample_prediction` is generated from this framework, with parameter optimization and feature engineering at the final step, which is not contained here (Only a simple median prediction is provided).
* Trip time score 0.53035 (Rank 4 at private leaderboard), using logistics regression with log transform on time, 75 trip matching, and feature engineering on drivers driving behaviours.
* Trip Trajectory score 2.24419 (Rank 22 at private leaderboard) using geometric median of 10 most similar trips.

## Instruction
#### Download Data
* download `train.csv.zip`, `test.csv.zip`, `train.csv`, `test.csv`, and put into folder `./input`.

#### Generate prediction
* run `./main.sh` to generate submission, which take roughly 1 day, result will be at `./train/output` .

#### Sample submission
* If you don't want to run the code or downloading data, use submission from `./sample_prediction`
