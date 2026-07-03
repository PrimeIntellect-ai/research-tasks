You are a log analyst investigating intermittent performance issues and errors on a web server. You have a large log file located at `/home/user/server_logs.txt`. You need to process this file to extract features, stratify the data, and find the most anomalous requests for each HTTP status code.

Because the production log files are typically massive, you must write a highly efficient C++ program to process the logs using a streaming approach (reading line-by-line rather than loading the whole file into memory), and wrap it in a multi-stage shell pipeline.

The log file has the following space-separated format:
`[YYYY-MM-DD HH:MM:SS] IP_ADDRESS HTTP_METHOD ENDPOINT STATUS_CODE RESPONSE_TIME_MS USER_AGENT`

Example:
`[2023-10-25 10:00:00] 192.168.1.15 GET /api/v1/users 200 45 Mozilla/5.0`

Your task is to:
1. Write a C++ program at `/home/user/log_analyzer.cpp`.
2. The program must stream the log file from standard input or a file path.
3. For each line, extract the `STATUS_CODE` (integer) and `RESPONSE_TIME_MS` (integer).
4. Calculate an `AnomalyScore` for each request. The formula is:
   `AnomalyScore = RESPONSE_TIME_MS * (STATUS_CODE >= 400 ? 2 : 1)`
5. Perform stratified sampling: For *each distinct* `STATUS_CODE` found in the file, keep track of exactly the top 5 log lines with the highest `AnomalyScore`. (If a status code has fewer than 5 entries, keep all of them).
6. Output a CSV to `/home/user/anomaly_samples.csv` with the header `StatusCode,AnomalyScore,OriginalLogLine`. 
7. The output must be sorted first by `StatusCode` in ascending order, and then by `AnomalyScore` in descending order.
8. Create a bash script at `/home/user/pipeline.sh` that compiles your C++ program (using `g++` with `-O3`), runs it against `/home/user/server_logs.txt`, and produces the final `/home/user/anomaly_samples.csv` output.

Make sure your C++ code correctly handles standard parsing and edge cases, and that `/home/user/pipeline.sh` is executable and can be run to complete the entire pipeline.