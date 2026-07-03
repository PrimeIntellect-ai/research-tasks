You are a log analyst investigating performance patterns on our main server. 

We have a raw, unstructured log file located at `/home/user/server_logs.txt`. 
The log file contains entries that look like this:
`TIMESTAMP=2023-10-14T08:15:01Z | MSG: Request processed. [latency: 120ms] | USER: ALICE`

Your task is to write a C++ program that reads this file, parses the timestamps and latencies, and calculates the average latency per hour.

Specifically, you must:
1. Write a C++ program at `/home/user/process_logs.cpp`.
2. Extract the hour component from the `TIMESTAMP` field (e.g., `08` from `2023-10-14T08:15:01Z`).
3. Extract the integer latency value from the `MSG` field (e.g., `120` from `[latency: 120ms]`).
4. Stratify (group) the data by the extracted hour (00 through 23).
5. Calculate the mathematical mean (average) latency for each hour present in the logs.
6. Write the aggregated results to a CSV file located at `/home/user/hourly_stats.csv`.

Requirements for `/home/user/hourly_stats.csv`:
- The first line must be the exact header: `Hour,Avg_Latency`
- Following lines must contain the hour (2 digits, e.g., `08`) and the average latency formatted to exactly 2 decimal places (e.g., `125.00`).
- The rows must be sorted by `Hour` in ascending order.
- Do not include hours that have no log entries.

Compile your program using `g++ -O2 /home/user/process_logs.cpp -o /home/user/process_logs` and execute it to generate the CSV.