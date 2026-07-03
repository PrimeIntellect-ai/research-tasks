You are acting as a data scientist working on an industrial IoT project. We have a high-frequency sensor dataset containing vibration readings from various machines, but it contains noise and anomalies due to sensor glitches or sudden mechanical shocks. 

You need to write a C++ program to process this dataset, calculate rolling statistics, standardize the readings, and flag anomalies. 

**Input Data:**
There is an input file located at `/home/user/vibration_log.csv`. 
It has a header and three columns: `Timestamp`, `MachineID`, `VibrationValue`.
The data is already sorted chronologically by `Timestamp`.

**Requirements:**
1. Write a C++17 program at `/home/user/detector.cpp`.
2. The program must read `/home/user/vibration_log.csv` and process the data for each `MachineID` independently.
3. For each `MachineID`, maintain a sliding window of the most recent $K=10$ readings. 
4. For each incoming reading $V_t$ for a machine:
    a. Calculate the rolling mean ($\mu$) and sample standard deviation ($\sigma$) of the *current* elements in the sliding window (before adding $V_t$). 
    b. If the window has fewer than 2 elements, set $\mu = V_t$ and $\sigma = 0.0$.
    c. Standardize the current reading to get the Z-score: $Z_t = \frac{V_t - \mu}{\sigma}$. If $\sigma == 0$, set $Z_t = 0.0$.
    d. Flag the reading as an anomaly if $|Z_t| > 3.0$.
    e. Add $V_t$ to the sliding window (if the window already has 10 elements, remove the oldest element).
5. Output the results to `/home/user/processed_vibration.csv`. The output must be a CSV with the following exact header:
   `Timestamp,MachineID,VibrationValue,RollingMean,RollingStd,ZScore,IsAnomaly`
6. Formatting constraints for the output CSV:
   - `RollingMean`, `RollingStd`, and `ZScore` must be formatted as floating-point numbers with exactly 4 decimal places.
   - `IsAnomaly` must be `1` if an anomaly was detected, or `0` otherwise.
   - `Timestamp` is an integer, `MachineID` is a string, `VibrationValue` is a float formatted to 4 decimal places.
7. Compile your program into an executable at `/home/user/detector` using `g++` and run it to produce the output file.

Your final goal is to ensure `/home/user/processed_vibration.csv` is correctly generated.