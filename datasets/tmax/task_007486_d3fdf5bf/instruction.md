You are acting as a data scientist cleaning a messy dataset of sensor logs using C. 

You have been provided with a raw log file at `/home/user/sensor_logs.txt`. 

Your goal is to build a 2-stage data processing pipeline in C, orchestrated by a Makefile.

**Stage 1: Extractor**
Write a C program named `/home/user/extractor.c`. 
It must read `/home/user/sensor_logs.txt` line by line and use POSIX Regular Expressions (`<regex.h>`) to extract valid sensor readings.
A valid log line looks exactly like this:
`[<TIMESTAMP>] <LOGLEVEL> - sensor_id: <SENSOR_ID>, val: <VALUE>`
Example: `[2023-10-01T12:00:02Z] INFO - sensor_id: S1, val: 10.5`

Your regex should capture the TIMESTAMP, SENSOR_ID, and VALUE. Ignore any lines that do not match this pattern.
The program must output a CSV file to `/home/user/parsed.csv` with the header: `timestamp,sensor_id,value` followed by the extracted valid records in the order they appear.

**Stage 2: Anomaly Detector**
Write a C program named `/home/user/detector.c`.
It must read `/home/user/parsed.csv`. For the sensor `S1` only, track the consecutive values. 
Detect "changepoints" (anomalies) where the absolute difference between the current reading and the *immediately preceding valid reading of S1* is strictly greater than `20.0`.
The very first reading of `S1` cannot be a changepoint since there is no previous reading to compare against.

The program must output a CSV file to `/home/user/anomalies.csv` with the header: `timestamp,sensor_id,value,diff` (where diff is the absolute difference, formatted to 1 decimal place, e.g., `34.0`).

**Orchestration**
Create a `/home/user/Makefile` with the following targets:
- `extractor`: Compiles `extractor.c` to an executable named `extractor`.
- `detector`: Compiles `detector.c` to an executable named `detector`.
- `all`: Compiles both executables.
- `run`: A DAG target that ensures `all` is built, then runs `./extractor`, and finally runs `./detector`.

Once you have created `extractor.c`, `detector.c`, and the `Makefile`, execute `make run` so the output files are generated.