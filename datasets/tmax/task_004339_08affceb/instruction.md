You are an automation specialist creating a data ingestion pipeline for an international sensor network. 

You have been provided with a raw CSV file at `/home/user/raw_sensors.csv`. This file contains periodic snapshots from two distinct weather stations (StationA and StationB) in a "wide" format. The data contains missing gaps, uneven time intervals, and multilingual status messages (UTF-8 encoded).

Here is a sample of the data format:
```csv
Hour,StationA_Temp,StationA_Status,StationB_Temp,StationB_Status
8,15.5,En_línea,22.1,正常
11,,Error_🔥,23.0,警告
14,16.2,En_línea,,正常
```
(Note: An empty value means the sensor failed to report that specific field at that hour).

Your task is to write a C program that processes this data.
1. Create your C source file at `/home/user/processor.c`.
2. The program must read `/home/user/raw_sensors.csv`.
3. **Reshape:** Convert the data from the wide format to a long format with columns: `Hour,Station,Temp,Status`.
4. **Resample & Gap-Fill:** The output must have continuous, hourly data from the minimum hour to the maximum hour present in the input file (e.g., every hour from 8 to 14). 
    - If a specific hour is missing entirely from the input file, you must create a row for it.
    - If a value (`Temp` or `Status`) is missing or an entirely new hour is being generated, apply **Forward Fill** (carry over the last known good value for that specific station).
5. **Unicode correctness:** Ensure the UTF-8 status strings are perfectly preserved and copied during gap-filling.
6. The program must output the processed data to `/home/user/output.csv` sorted by `Hour` (ascending), and then by `Station` (alphabetically: A then B). Format `Temp` to exactly one decimal place.
7. Compile your program to `/home/user/processor` and run it to generate the output file.

Your final output file `/home/user/output.csv` should look like this (header included):
```csv
Hour,Station,Temp,Status
8,A,15.5,En_línea
8,B,22.1,正常
9,A,15.5,En_línea
...
```