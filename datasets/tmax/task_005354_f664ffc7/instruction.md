You are a data analyst tasked with processing a large CSV file of system metrics to generate an alert report.

A file is located at `/home/user/metrics.csv` with the following header and format:
`server_id,timestamp,response_time`

You need to write a C++ program at `/home/user/analyze.cpp` that processes this CSV without using any external libraries (only the C++ standard library is allowed). Compile and run this program to produce the desired output.

Your C++ program must perform the following pipeline:
1. **Stratification & Sampling:** Read the CSV and filter ONLY the rows where `server_id` is exactly `web-01`. Keep chronological order. From this filtered subset, perform systematic sampling by keeping only the 1st, 6th, 11th, 16th, etc., records (i.e., index 0, 5, 10, 15... if zero-indexed).
2. **Changepoint/Anomaly Detection:** Analyze the *sampled* records chronologically. An anomaly occurs when the `response_time` of the current sampled record is strictly greater than the `response_time` of the *immediately preceding sampled record* by more than 100. (The very first sampled record cannot be an anomaly).
3. **Template Generation:** For each anomaly detected, generate an alert string using the following exact template:
`[ALERT] web-01 spike at <timestamp>: +<delta>ms`
(where `<delta>` is the difference in `response_time` between the current sampled record and the previous sampled record).

Your program must write these alert strings, one per line, to `/home/user/alerts.log`.

Requirements:
- Ensure the program compiles cleanly with `g++ -std=c++17 /home/user/analyze.cpp -o /home/user/analyze`.
- Execute the program so `/home/user/alerts.log` is generated.
- `timestamp` is a string (or integer), `response_time` is an integer.