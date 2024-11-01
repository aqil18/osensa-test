# PM2.5 Average Calculator
## What is PM2.5
PM2.5, or fine particulate matter, is a mixture of particles in the air that are 2.5 micrometers or less in diameter. PM2.5 is a health risk because it can travel deep into the lungs when inhaled. 

## What this calculator does
This python script will produce the average PM2.5 found in a map bound by 2 coordinates and also each of the samples taken from the stations within the map.

## How to run it
1. Install python3 on the command line
2. Run pip install -r requirements.txt
3. Run python3 main.py lat1 long 1 lat2 long2 --sampling_period 1 --sampling_rate 1
    a. lat1 long1 lat2 long2 -> 2 coordinates that would represent a map 
    b. sampling_rate -> sampling rate in sample(s) / minute (default = 1)
    c. sampling_period -> sampling period in minutes (default = 5)
4. Example command python3 main.py 39.379436 116.091230 40.235643 116.784382 --sampling_period 1 --sampling_rate 1